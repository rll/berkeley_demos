#!/usr/bin/env python
import roslib
roslib.load_manifest("unfolding_smach")
import rospy
import StanceUtils
import PrimitiveUtils
import GripUtils
from image_processor.srv import *
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped
from numpy import *
import sys
from smach import State, StateMachine
import smach_ros
from SmachUtils import *
import tf
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pr2_simple_motions_srvs.srv import MoveBase, RotateBase
import math
from nav_msgs.srv import *

#Initial params. Note that triangle_length, towel_width, and towel_height will be overridden once it has detected the towel
TABLE_HEIGHT = 0.77 #was 0.77
TABLE_WIDTH = 0.98
STRETCH_FACTOR = 1.00
TOWEL_STRETCH_FACTOR = 0.95
triangle_length = 0.8
towel_width = 0.6
towel_height = 0.2
MAX_FLIPS = 1

(TWITTER,CONSOLE) = range(2)
MODE = CONSOLE

"""
Utility functions
"""
def opp_arm(arm):
    if arm == "l":
        return "r"
    else:
        return "l"
"""
Defining States. Four main sections: Initialize, ClumpToTriangle,TriangleToRectangle,FoldTowel
"""

class Reset(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["arm"])
    def execute(self,userdata):
        arm = userdata.arm
        multiplier = 1 if arm == 'r' else -1
        if not GripUtils.go_to(x=0.4,y=0,z=0.35,roll=0,yaw=pi/2*multiplier,pitch=pi/4,arm=arm,grip=True,frame="table_height",dur=3.0):
            return FAILURE
        GripUtils.open_gripper(arm)
        GripUtils.recall_arm("b")
        return SUCCESS

class PickupClump(SuccessFailureState):

    def execute(self, userdata):
       
        process_mono = rospy.ServiceProxy("clump_center_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        z_offset = 0.06
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
        GripUtils.close_gripper("l")
        while not GripUtils.has_object("l") and not rospy.is_shutdown():
            z_offset -= 0.02
            if(z_offset < 0):
                return FAILURE
            GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
            GripUtils.close_gripper("l")
        return SUCCESS

class PickupClumpWhite(SuccessFailureState):

    def execute(self, userdata):
       
        process_mono = rospy.ServiceProxy("clump_center_node_white/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        z_offset = 0.06
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
        GripUtils.close_gripper("l")
        while not GripUtils.has_object("l") and not rospy.is_shutdown():
            z_offset -= 0.02
            if(z_offset < 0):
                return FAILURE
            GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
            GripUtils.close_gripper("l")
        return SUCCESS


class PickupCorner(SuccessFailureState):
    def __init__(self,side,let_go=False):
        SuccessFailureState.__init__(self,output_keys=["cloth_width","cloth_height","arm"])
        self.side = side
        self.let_go = let_go

    def execute(self, userdata):
        if self.side == 'l':
            arm = 'l'
            processor = 'far_left_finder_node'
            yaw = -pi/2
        else:
            arm = 'r'
            processor = 'far_right_finder_node'
            yaw = pi/2
        process_mono = rospy.ServiceProxy("%s/process_mono"%processor,ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        pt_opp = resp.pts3d[1]
        userdata.arm = 'l' if arm == 'r' else 'r' #Arm returns the arm which is currently gripping
        homogeneity = resp.params[resp.param_names.index("homogeneity")]
        if homogeneity > 0.13:
            print "Too homogeneous: %f"%homogeneity
            return FAILURE 
        userdata.cloth_width = sqrt( (pt_opp.point.x - pt.point.x)**2 + (pt_opp.point.y - pt.point.y)**2 )
        #userdata.cloth_width = abs(pt_opp.point.y - pt.point.y)
        userdata.cloth_height = None
        
        if arm == "l":
            x_offset = -0.02 #was -0.01
        else:
            x_offset = -0.01
        if not GripUtils.grab_point(pt,roll=-pi/2,yaw=yaw,arm=arm,x_offset=x_offset):
            return FAILURE
        else:
            if self.let_go:
                GripUtils.open_gripper(opp_arm(arm))
            return SUCCESS


### Phase 1: Initialize ###
class Initialize(NestedStateMachine):
    def __init__(self, title=None, transitions=None):
        NestedStateMachine.__init__(self, title, transitions=transitions,outcomes=DEFAULT_OUTCOMES) 
        self.add('Arms_Up', ArmsUp(grip=True), {SUCCESS:'Look_Down', FAILURE:FAILURE})
        self.add('Look_Down', StanceState('look_down'), {SUCCESS:SUCCESS, FAILURE:FAILURE})
        
### Phase 2: ClumpToTriangle ###
## PickUpClump -> SpreadOutRight -> PickupLeft -> SpreadOutLeft -> PickupRight -> LayoutTriangle ##



class ClumpToTriangle(NestedStateMachine):
    def __init__(self, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES)
        self.add('Pick_Up_Clump', PickupClump(), {SUCCESS:'Spread_Out_Left', FAILURE: 'Pick_Up_Clump'})
        self.add('Spread_Out_Left', SpreadAcross('l',TABLE_WIDTH,towel_width),{SUCCESS:'Pickup_Right',FAILURE:FAILURE})
        self.add('Pickup_Right', PickupCorner('r',let_go=True),{SUCCESS:'Recall_Left',FAILURE:'Reset'})
        self.add('Recall_Left', RecallArm('l'),{SUCCESS:'Spread_Out_Right',FAILURE:FAILURE})
        self.add('Spread_Out_Right', SpreadAcross('r',TABLE_WIDTH,towel_width),{SUCCESS:'Pickup_Left',FAILURE:FAILURE})
        self.add('Pickup_Left', PickupCorner('l',let_go=False),{SUCCESS:'Shake_Triangle',FAILURE:'Reset'})
        self.add('Shake_Triangle',ShakeBothArms(2,violent=False),{SUCCESS:'Layout_Triangle',FAILURE:'Layout_Triangle'})
        self.add('Layout_Triangle', SpreadOut(0.48),{SUCCESS:SUCCESS,FAILURE:FAILURE})
        self.add('Reset',Reset(),{SUCCESS:'Pick_Up_Clump',FAILURE:FAILURE})

### Phase 3: TriangleToRectangle ###

class TriangleToRectangle(NestedStateMachine):
    def __init__(self, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES)
        self.add('Grab_Triangle', GrabTriangle(), {SUCCESS:'Shake_Towel', FAILURE: FAILURE})
        self.add('Shake_Towel',ShakeBothArms(1,violent=False),{SUCCESS:'Layout_Towel',FAILURE:'Layout_Towel'})
        self.add('Layout_Towel',SpreadOut(0.40),{SUCCESS:SUCCESS,FAILURE:FAILURE}) #was 0.43

class GrabTriangle(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,output_keys=["cloth_width","cloth_height"])
        

    def execute(self, userdata):
        process_mono = rospy.ServiceProxy("triangle_fitter_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt_l = resp.pts3d[0]
        pt_r = resp.pts3d[1]
        pt_tl = resp.pts3d[2]
        pt_tr = resp.pts3d[3]
        #Compute approximate widths
        towel_width = sqrt( (pt_l.point.x - pt_tr.point.x)**2 + (pt_l.point.y - pt_tr.point.y)**2 )
        towel_height = sqrt( (pt_l.point.x - pt_tl.point.x)**2 + (pt_l.point.y - pt_tl.point.y)**2 )
        userdata.cloth_width = towel_width
        userdata.cloth_height = towel_height
        if resp.params[resp.param_names.index("left")] == 0:
            left = False
        else:
            left = True
        print "Correct?"
        tf = raw_input()
        if len(tf) > 0 and (tf[0] == 'n' or tf[0] == 'f'):
            left = not left
        if left:
            GripUtils.recall_arm("l")
            if GripUtils.grab_point(pt_l,roll=pi/2,yaw=-pi/3,pitch=pi/4,arm="l",x_offset=0.005):
                return SUCCESS
            else:
                return FAILURE
        else:
            
            GripUtils.recall_arm("r")
            if GripUtils.grab_point(pt_r,roll=-pi/2,yaw=pi/3,pitch=pi/4,arm="r",x_offset=0.005):
                return SUCCESS
            else:
                return FAILURE

### Phase 4: FoldTowel ###

class FoldTowel(NestedStateMachine):
    def __init__ (self,title=None,transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES)
        self.add('Arms_Up', ArmsUp(grip=False), {SUCCESS:'Smooth_0', FAILURE:FAILURE})
        self.add('Smooth_0', SmoothOnTable(arm="b",smooth_x=0.5,distance=TABLE_WIDTH), {SUCCESS:'Detect_Towel',FAILURE:'Detect_Towel'})
        self.add('Detect_Towel', DetectTowel(), {SUCCESS:'Execute_Fold',FAILURE:'Flip_Towel'})
        self.add('Flip_Towel', FlipTowel(), {SUCCESS:'Smooth_0',FAILURE:'Flip_Towel'})
        self.add('Execute_Fold', ExecuteFold(), {SUCCESS:SUCCESS, FAILURE:'Arms_Up'})
        
class FlipTowel(NestedStateMachine):
    def __init__ (self,title=None,transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=["bl","tl","tr","br"])
        #self.add('Detect_Towel', DetectTowel(), {SUCCESS:'Pickup_Towel', FAILURE:FAILURE})
        self.add('Pickup_Towel', PickupTowel(), {SUCCESS:'Layout_Towel', FAILURE:FAILURE})
        self.add('Layout_Towel', SpreadOut(0.42,recall=True),{SUCCESS:SUCCESS,FAILURE:FAILURE})
        

        
class DetectTowel(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,output_keys=["bl","tl","tr","br"])
        self.flip_count = 0
        
    def execute(self,userdata):
        process_mono = rospy.ServiceProxy("towel_fitter_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        userdata.bl = resp.pts3d[0]
        userdata.tl = resp.pts3d[1]
        userdata.tr = resp.pts3d[2]
        userdata.br = resp.pts3d[3]
        score = resp.params[resp.param_names.index("score")]
        to_flip = False
        if abs(score) < 0.00003 or self.flip_count >= MAX_FLIPS:
            to_flip = False
            print "Decided not to flip"
        else:
            self.flip_count += 1
            to_flip = True
            print "Decided to flip"
        print "Flip?"
        flip = raw_input()
        if(flip[0] == "t" or flip[0] == "T" or flip[0] == "y" or flip[0] == "Y"):
            to_flip = True
        else:
            to_flip = False
        return FAILURE if to_flip else SUCCESS
        
class PickupTowel(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["bl","tl","tr","br"],output_keys=["cloth_width","cloth_height"])
        
    def execute(self,userdata):
        bl = userdata.bl
        br = userdata.br
        tl = userdata.tl
        tr = userdata.tr
        userdata.cloth_width = sqrt( (bl.point.x-br.point.x)**2 + (bl.point.y - br.point.y)**2)*1.075
        userdata.cloth_height = max([abs(tl.point.x-bl.point.x),abs(tr.point.x-br.point.x)])
        if not GripUtils.grab_point(bl,roll=pi/2,yaw=-pi/2,pitch=pi/4,arm="l",x_offset=0.01,INIT_SCOOT_AMT = 0.01):
            return FAILURE
        if not GripUtils.grab_point(br,roll=-pi/2,yaw=pi/2,pitch=pi/4,arm="r",x_offset=0.01,INIT_SCOOT_AMT = 0.01):
            return FAILURE
        return SUCCESS
        
class ExecuteFold(NestedStateMachine):
    def __init__(self,title=None,transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=["bl","tl","tr","br"])
        self.add('Fold_1', Fold1(), {SUCCESS:'Smooth_1',FAILURE:FAILURE})
        self.add('Smooth_1', SmoothOnTable(arm="b",smooth_x=0.45,distance=TABLE_WIDTH), {SUCCESS:'Fold_2',FAILURE:'Fold_2'})
        self.add('Fold_2', Fold2(), {SUCCESS:'Smooth_2',FAILURE:FAILURE})
        self.add('Smooth_2', SmoothOnTable(arm="b",smooth_x=0.45,distance=TABLE_WIDTH/2.0), {SUCCESS:SUCCESS,FAILURE:SUCCESS})
        
class Fold1(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["bl","tl","tr","br"])
        
    def execute(self,userdata):
        pt_bl = userdata.bl
        pt_tl = userdata.tl
        pt_br = userdata.br
        pt_tr = userdata.tr
        #FIXME Hard-coded X offsets to compensate for poor calibration. Re-calibrate and REMOVE
        if not GripUtils.grab_point(pt_tl,roll=-pi/2,yaw=-pi/3,pitch=pi/4,arm="l",x_offset=-0.08):
            return FAILURE
        if not GripUtils.grab_point(pt_tr,roll=pi/2,yaw= pi/3,pitch=pi/4,arm="r",x_offset=-0.08):
            return FAILURE
        (bl_x,bl_y,bl_z) = (pt_bl.point.x,pt_bl.point.y,pt_bl.point.z)
        (tl_x,tl_y,tl_z) = (pt_tl.point.x,pt_tl.point.y,pt_tl.point.z)
        (br_x,br_y,br_z) = (pt_br.point.x,pt_br.point.y,pt_br.point.z)
        (tr_x,tr_y,tr_z) = (pt_tr.point.x,pt_tr.point.y,pt_tr.point.z)
        x_l = (tl_x+bl_x)/2.0
        y_l = (tl_y+bl_y)/2.0
        z_l = bl_z + sqrt( (bl_x-tl_x)**2 + (bl_y-tl_y)**2 )/2.0
        x_r = (tr_x+br_x)/2.0
        y_r = (tr_y+br_y)/2.0
        z_r = br_z + sqrt( (br_x-tr_x)**2 + (br_y-tr_y)**2 )/2.0
        pitch_l = pitch_r = pi/4
        roll_l = 0
        roll_r = 0
        yaw_l=-pi/2
        yaw_r= pi/2
        grip_l=grip_r=True
        frame_l=frame_r = pt_bl.header.frame_id
        if not GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                        ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                        ,dur=7.5):
            return_val = FAILURE
        print "Folding down!"
        x_l = bl_x-0.015
        y_l = bl_y+0.025
        z_l = z_r = bl_z + 0.02
        x_r = br_x-0.015
        y_r = br_y-0.025
        yaw_l = -3*pi/4
        yaw_r = 3*pi/4
        pitch_l=pitch_r = pi/4
        roll_l = pi/2
        roll_r = -pi/2
        GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                        ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                        ,dur=7.5)
        GripUtils.recall_arm("b")
        return SUCCESS

class Fold2(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["bl","tl","tr","br"])
        
    def execute(self,userdata):
        pt_bl = userdata.bl
        pt_tl = userdata.tl
        pt_br = userdata.br
        pt_tr = userdata.tr
        (bl_x,bl_y,bl_z) = (pt_bl.point.x,pt_bl.point.y,pt_bl.point.z)
        (tl_x,tl_y,tl_z) = (pt_tl.point.x,pt_tl.point.y,pt_tl.point.z)
        (br_x,br_y,br_z) = (pt_br.point.x,pt_br.point.y,pt_br.point.z)
        (tr_x,tr_y,tr_z) = (pt_tr.point.x,pt_tr.point.y,pt_tr.point.z)
        
        ctr_l_x = .75*bl_x + .25*tl_x
        #Make more centered
        ctr_l_x -= 0.01
        ctr_l_y = .75*bl_y + .25*tl_y
        z = bl_z
        yaw = -pi/2
        roll = -pi/2
        pitch = pi/4
        frame = pt_bl.header.frame_id
        if not GripUtils.grab(x=ctr_l_x,y=ctr_l_y,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame):
            return FAILURE
        ctr_r_x = .75*br_x + .25*tr_x
        #Make more centered
        ctr_r_x -= 0.01
        ctr_r_y = .75*br_y + .25*tr_y
        alpha = 0.333
        ctr_ml_x = (1-alpha)*ctr_l_x + alpha*ctr_r_x
        ctr_ml_y = (1-alpha)*ctr_l_y + alpha*ctr_r_y
        ctr_mr_x = (1-alpha)*ctr_r_x + alpha*ctr_l_x
        ctr_mr_y = (1-alpha)*ctr_r_y + alpha*ctr_l_y
        up_z = z+sqrt( (ctr_l_x - ctr_r_x)**2 + (ctr_l_y - ctr_r_y)**2) / 3.0
        pitch = pi/2
        if not GripUtils.go_to(x=ctr_ml_x,y=ctr_ml_y,z=up_z,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=True,dur=5.0):
            return FAILURE
        if not GripUtils.go_to(x=(ctr_ml_x+ctr_mr_x)/2.0,y=(ctr_ml_y+ctr_mr_y+0.02)/2.0,z=(up_z+bl_z)/2.0,roll=roll,yaw=yaw,pitch=(pitch+3*pi/4)/2.0,arm="l",frame=frame,grip=True,dur=5.0):
            return FAILURE
        z = bl_z
        pitch = 3*pi/4
        
        if not GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y+0.02,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=True,dur=5.0):
            return FAILURE
        yaw = pi/2
        roll = pi/2
        pitch = pi/4
        GripUtils.open_gripper("l")
        if not GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y-0.05,z=z+0.02,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=False,dur=1.0):
            return FAILURE
        GripUtils.recall_arm("l")
        if not GripUtils.grab(x=ctr_r_x,y=ctr_r_y-0.01,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame):
            return FAILURE
        pitch = pi/2
        if not GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y-0.02,z=up_z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame,grip=True,dur=5.0):
            return FAILURE

        if not GripUtils.go_to(x=(ctr_mr_x+ctr_ml_x)/2.0,y=(ctr_mr_y-0.02+ctr_ml_y-0.02)/2.0,z=(up_z+bl_z+0.01)/2.0,roll=roll,yaw=yaw,pitch=(pitch+3*pi/4)/2.0,arm="r",frame=frame,grip=True,dur=5.0):
            return FAILURE
        z = bl_z+0.01
        pitch = 3*pi/4
        
        if not GripUtils.go_to(x=ctr_ml_x,y=ctr_ml_y-0.02,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame,grip=True,dur=5.0):
            return FAILURE
        GripUtils.open_gripper("r")
        if not GripUtils.go_to(x=ctr_ml_x,y=ctr_ml_y+0.05,z=z+0.02,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame,grip=False,dur=1.0):
            return FAILURE
        GripUtils.recall_arm("r")
        
        """
        if not GripUtils.go_to_multi (x_l=ctr_ml_x+0.03,y_l=ctr_ml_y+0.06,z_l=z+0.01,roll_l=-pi/2,pitch_l=pi/4,yaw_l=-pi/2,grip_l=False,frame_l=frame
                                        ,x_r=ctr_mr_x+0.03,y_r=ctr_mr_y-0.03,z_r=z+0.01,roll_r= pi/2,pitch_r=pi/4,yaw_r= pi/2,grip_r=False,frame_r=frame
                                        ,dur=3.0):
            return FAILURE
        if not GripUtils.go_to_multi (x_l=ctr_ml_x+0.03,y_l=ctr_ml_y-0.05,z_l=z+0.01,roll_l=-pi/2,pitch_l=pi/4,yaw_l=-pi/2,grip_l=False,frame_l=frame
                                        ,x_r=ctr_mr_x+0.03,y_r=ctr_mr_y+0.05,z_r=z+0.01,roll_r= pi/2,pitch_r=pi/4,yaw_r= pi/2,grip_r=False,frame_r=frame
                                        ,dur=3.0):
            return FAILURE
        GripUtils.close_gripper("b")
        if not GripUtils.go_to_multi (x_l=ctr_ml_x+0.03,y_l=ctr_ml_y-0.05,z_l=z+0.1,roll_l=-pi/2,pitch_l=pi/4,yaw_l=-pi/2,grip_l=True,frame_l=frame
                                        ,x_r=ctr_mr_x+0.03,y_r=ctr_mr_y+0.05,z_r=z+0.1,roll_r= pi/2,pitch_r=pi/4,yaw_r= pi/2,grip_r=True,frame_r=frame
                                        ,dur=3.0):
            return FAILURE
        """
        return SUCCESS

class GenericUserData:
    def __init__(self):
        pass

### Michael Phase 1: SaveMarkLocation ###

class SaveMarkLocation(NestedStateMachine):
    def __init__(self, listener, title=None, transitions=None):
        self.listener = listener
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,output_keys=['locations'])
        self.add('Userdata_Initializer',UserdataInitializer(), {SUCCESS:'Save_Mark_Position',FAILURE: FAILURE})
        self.add('Save_Mark_Position',SavePosition('location', listener), {SUCCESS:SUCCESS, FAILURE: FAILURE})

class UserdataInitializer(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,output_keys=['locations'])
        
    def execute(self,userdata):
        userdata.locations = {}
        return SUCCESS

class SavePosition(SuccessFailureState):
    def __init__(self, positionName, listener):
        SuccessFailureState.__init__(self,input_keys=['locations'],output_keys=['locations'])
        self.positionName = positionName
        self.listener = listener

    def execute(self, userdata):

        print "Please move Brett to", self.positionName, "location."
        print "Is Brett ready?"
        waitForInput = raw_input()

        pt = PoseStamped()
        pt.header.stamp = rospy.Time.now()
        pt.header.frame_id = "/base_footprint"

        now = rospy.Time()
        self.listener.waitForTransform("/map", "/base_footprint", now, rospy.Duration(15.0))
        pt.header.stamp = now
        trans = self.listener.transformPose("/map", pt)

        userdata.locations[self.positionName] = trans
        print "Saving location", self.positionName, "as: "
        print trans
        return SUCCESS

### Michael Phase 2: MakeMark ###

class MakeMark(NestedStateMachine):
    def __init__(self, listener, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=['locations'],output_keys=['locations'])
        self.listener = listener
        self.add('Mark', MarkCenter(listener), {SUCCESS:SUCCESS, FAILURE: FAILURE})


class MarkCenter(SuccessFailureState):
    def __init__(self, listener):
        SuccessFailureState.__init__(self,input_keys=['locations'],output_keys=['locations'])
        self.listener = listener
    def execute(self, userdata):
        process_mono = rospy.ServiceProxy("clump_center_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        pt.point.z += 0.05
        
        self.listener.waitForTransform("/map", pt.header.frame_id, pt.header.stamp, rospy.Duration(15.0))
        transpt = self.listener.transformPoint("/map", pt)

        GripUtils.go_to_pt(transpt,roll=0,yaw=0,pitch=pi/2,arm="l",grip=True,dur=5.0)
        userdata.locations['mark'] = transpt
        return SUCCESS

class RepeatMark(NestedStateMachine):
    def __init__(self, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=['locations'])
        self.add('MarkAgain', RedoMark(), {SUCCESS:SUCCESS, FAILURE: FAILURE})

class RedoMark(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=['locations'])
    def execute(self, userdata):
        pt = userdata.locations['mark']
        GripUtils.go_to_pt(pt,roll=0,yaw=0,pitch=pi/2,arm="l",z_offset=0,grip=True,dur=5.0)
        return SUCCESS

class FreeRun(NestedStateMachine):
    def __init__(self, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES)
        self.add('Free_Run',WaitForInput(), {SUCCESS:SUCCESS, FAILURE: FAILURE})

class WaitForInput(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self)

    def execute(self, userdata):
        print "Tell me when to go!"
        waitForInput = raw_input()
        return SUCCESS

class LoadPosition(NestedStateMachine):
    def __init__(self, listener, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=['locations'])
        self.add('Go_To_Mark_Location',GoToLocation('location', listener), {SUCCESS:SUCCESS, FAILURE: FAILURE})

class Cycle(NestedStateMachine):
    def __init__(self, listener, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=['locations'])
        self.add('Go_To_Pickup_Location',GoToLocation('pickup', listener), {SUCCESS:'Go_To_Folding_Location', FAILURE: FAILURE})
        self.add('Go_To_Folding_Location',GoToLocation('folding', listener), {SUCCESS:'Go_To_Dropoff_Location', FAILURE: FAILURE})
        self.add('Go_To_Dropoff_Location',GoToLocation('dropoff', listener), {SUCCESS:SUCCESS, FAILURE: FAILURE})

class Pickup(NestedStateMachine):
    def __init__(self, listener, title=None, transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=['locations'])
        self.add('Go_To_Pickup_Location',GoToLocation('pickup', listener), {SUCCESS:'Grab_Towel', FAILURE: FAILURE})
        self.add('Grab_Towel',PickupClumpWhite(), {SUCCESS:'Lift_Up', FAILURE: FAILURE})
        self.add('Lift_Up', LiftUp(),{SUCCESS:'Go_To_Folding_Location',FAILURE:FAILURE})
        self.add('Go_To_Folding_Location',GoToLocation('folding', listener), {SUCCESS:'Put_Down_Clump', FAILURE: FAILURE})
        self.add('Put_Down_Clump',PutdownClump(), {SUCCESS:SUCCESS, FAILURE: FAILURE})

class LiftUp(SuccessFailureState):

    def execute(self, userdata):
        GripUtils.go_to(0.3,0.65,0.35,0,0,0,True,"torso_lift_link","l")
        return SUCCESS

### Michael Phase 4: LoadPosition ###

class GoToLocation(SuccessFailureState):
    def __init__(self, positionName, listener):
        SuccessFailureState.__init__(self,input_keys=['locations'])
        self.positionName = positionName
        self.listener = listener

    def execute(self, userdata):
        print "Trying to go"
        location = userdata.locations[self.positionName]
        print "Going to location:", location
        go_to(location, self.listener)
        return SUCCESS

class PutdownClump(SuccessFailureState):

    def execute(self, userdata):
       
        process_mono = rospy.ServiceProxy("clump_center_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        z_offset = 0.16
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
        GripUtils.open_gripper("l")
        return SUCCESS

def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

#make go_to have 3 phases:
#1) adjust x-y position (which consists of backing out from the table and going across to a position behind the target)
#2) correct angle (since Brett likes to twist)
#3) adjust x-y position again (which slides him into the table)
def go_to(location, listener):
    point = PoseStamped()
    #phase 1 linear movement

    rospy.wait_for_service('move_base')

    try:
        move = rospy.ServiceProxy('move_base', MoveBase)
        resp1 = move(-0.5, 0, False, 0)    
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    rospy.loginfo("Now attempting to transform 1st displacement error.")
    now = rospy.Time()
    location.header.stamp = now

    listener.waitForTransform("/map", "/base_footprint", now, rospy.Duration(20.0))
   
    try:
        point = listener.transformPose("/base_footprint", location)
    except Exception, e:
        print e

    rospy.wait_for_service('move_base')
    try:
        move = rospy.ServiceProxy('move_base', MoveBase)
        rospy.loginfo("Moving to dx=%s, dy=%s.", point.pose.position.x - 0.5, point.pose.position.y)
        resp1 = move(point.pose.position.x - 0.5, point.pose.position.y, False, 0)    
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    rospy.loginfo("Now attempting to transform rotational error.")
    #phase 2 angular adjustment
    rospy.wait_for_service('rotate_base')
    now = rospy.Time()
    location.header.stamp = now
    listener.waitForTransform("/map", "/base_footprint", now, rospy.Duration(20.0))
    try:
        point = listener.transformPose("/base_footprint", location)
    except Exception, e:
        print e

    rospy.loginfo("Rotational transform complete.")
    try:
        rotate = rospy.ServiceProxy('rotate_base', RotateBase)
        angle = sign(point.pose.orientation.z)*2*math.acos(point.pose.orientation.w)
        rospy.loginfo("Rotating by: %s.", angle)
        resp1 = rotate(angle)    
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


    rospy.loginfo("Time for the linear correction!")
    #phase 3 linear correction
    rospy.wait_for_service('move_base')
    now = rospy.Time()
    location.header.stamp = now

    listener.waitForTransform("/map", "/base_footprint", now, rospy.Duration(4.0))
   
    try:
        point = listener.transformPose("/base_footprint", location)
    except Exception, e:
        print e

    try:
        move = rospy.ServiceProxy('move_base', MoveBase)
        rospy.loginfo("Moving to dx=%s, dy=%s.", point.pose.position.x, point.pose.position.y)
        resp1 = move(point.pose.position.x, point.pose.position.y, False, 0)    
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def main(args):
    rospy.init_node("unfolding_smach_demo_node")

    listener = tf.TransformListener()

    sm = OuterStateMachine(DEFAULT_OUTCOMES)
    START_STATE = 'Save_Position'
    with sm:
         
         OuterStateMachine.add('Initialize1',Initialize(),{SUCCESS:START_STATE,FAILURE:FAILURE})
         OuterStateMachine.add('Save_Position',SaveMarkLocation(listener),{SUCCESS:'Mark1',FAILURE:FAILURE})
         OuterStateMachine.add('Mark1',MakeMark(listener),{SUCCESS:'Initialize2',FAILURE:FAILURE})
        
         OuterStateMachine.add('Initialize2',Initialize(),{SUCCESS:'Free_Run',FAILURE:FAILURE})

         OuterStateMachine.add('Free_Run',FreeRun(),{SUCCESS:'Load_Position',FAILURE:FAILURE})
         OuterStateMachine.add('Load_Position',LoadPosition(listener),{SUCCESS:'Mark2',FAILURE:FAILURE})
         OuterStateMachine.add('Mark2',RepeatMark(),{SUCCESS:'Initialize3',FAILURE:FAILURE})
         OuterStateMachine.add('Initialize3',Initialize(),{SUCCESS:SUCCESS,FAILURE:FAILURE})
    
    sis = smach_ros.IntrospectionServer('demo_smach_server', sm, '/SM_ROOT')
    sis.start()
    outcome = sm.execute()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
