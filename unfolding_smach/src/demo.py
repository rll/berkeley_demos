#!/usr/bin/env python
import roslib
roslib.load_manifest("unfolding_smach")
import rospy
import StanceUtils
import PrimitiveUtils
from pr2_simple_arm_motions import GripUtils
from image_processor.srv import *
from geometry_msgs.msg import PointStamped
from numpy import *
import sys
from smach import State, StateMachine
import smach_ros
from smach_utils.SmachUtils import *

#Initial params. Note that triangle_length, towel_width, and towel_height will be overridden once it has detected the towel
TABLE_WIDTH = 0.98      #Width of the table used. Can (and should) be inferred visually, but as we only have one table
                        #we keep it as is.
towel_width = 0.6       #An arbitrary guess at the width of the towel. Just used as a seed -- no need to be correct
towel_height = 0.35      #Same for height
MAX_FLIPS = 1           #Number of times to flip the towel

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
        if not GripUtils.go_to(x=0.4,y=0,z=0.35,roll=0,yaw=pi/2*multiplier,pitch=pi/4,arm=arm,grip=True,frame="table_height",dur=5.0):
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
            print "Z_offset = %f"%z_offset
            z_offset -= 0.02
            if(z_offset < -0.02):
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
            x_offset = -0.01
            y_offset = -0.02
        else:
            x_offset = -0.005
            y_offset = 0.02
        if not GripUtils.grab_point(pt,roll=-pi/2,yaw=yaw,arm=arm,x_offset=x_offset,y_offset=y_offset):
            return FAILURE
        else:
            if self.let_go:
                GripUtils.open_gripper(opp_arm(arm))
            return SUCCESS


### Phase 1: Initialize ###
class Initialize(NestedStateMachine):
    def __init__(self, title=None, transitions=None):
        NestedStateMachine.__init__(self, title, transitions=transitions,outcomes=DEFAULT_OUTCOMES)
        self.add('Arms_Up', ArmsUp(grip=False), {SUCCESS:'Look_Down', FAILURE:FAILURE})
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
        self.add('Smooth_0', SmoothOnTable(arm="b",smooth_x=0.5,distance=TABLE_WIDTH*0.9),
                 {SUCCESS:'Detect_Towel_0',FAILURE:'Detect_Towel_0'})
        self.add('Detect_Towel_0', DetectTowel(), {SUCCESS:'Flip_Towel',FAILURE:'Flip_Towel'})
        #self.add('Flip_Towel', FlipTowel(), {SUCCESS:'Smooth_1',FAILURE:'Flip_Towel'})
        self.add('Flip_Towel', FlipTowel(), {SUCCESS:'Detect_Towel_1',FAILURE:'Flip_Towel'})
        # removing step below to save time on demo
        #self.add('Smooth_1', SmoothOnTable(arm="b",smooth_x=0.5,distance=TABLE_WIDTH*0.9),
        #         {SUCCESS:'Detect_Towel_1',FAILURE:'Detect_Towel_1'})
        self.add('Detect_Towel_1', DetectTowel(), {SUCCESS:'Execute_Fold',FAILURE:'Execute_Fold'})
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
        # to_flip = False
        # if abs(score) < 0.00003 or self.flip_count >= MAX_FLIPS:
        #     to_flip = False
        #     print "Decided not to flip"
        # else:
        #     self.flip_count += 1
        #     to_flip = True
        #     print "Decided to flip"
        
        # print "Flip?"
        # flip = raw_input()
        # if(flip[0] == "t" or flip[0] == "T" or flip[0] == "y" or flip[0] == "Y"):
        #     to_flip = True
        # else:
        #     to_flip = False
        # return FAILURE if to_flip else SUCCESS
        return SUCCESS
        
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
        #if not GripUtils.grab_point(bl,roll=pi/2,yaw=-pi/2,pitch=pi/4,arm="l",x_offset=0.01,INIT_SCOOT_AMT = 0.01):
        #    return FAILURE
        #if not GripUtils.grab_point(br,roll=-pi/2,yaw=pi/2,pitch=pi/4,arm="r",x_offset=0.01,INIT_SCOOT_AMT = 0.01):
        #    return FAILURE
        if not GripUtils.grab_points(point_l=bl,roll_l=pi/2,yaw_l=-pi/2,pitch_l=pi/4,x_offset_l=0.02
                                    ,point_r=br,roll_r=-pi/2,yaw_r=pi/2,pitch_r=pi/4,x_offset_r=0.02, y_offset_r=0.01,
                                    INIT_SCOOT_AMT = 0.01):
            return FAILURE

        return SUCCESS
        
class ExecuteFold(NestedStateMachine):
    def __init__(self,title=None,transitions=None):
        NestedStateMachine.__init__(self,title,transitions=transitions,outcomes=DEFAULT_OUTCOMES,input_keys=["bl","tl","tr","br"])
        self.add('Fold_1', Fold1(), {SUCCESS:'Smooth_1',FAILURE:FAILURE})
        self.add('Smooth_1', SmoothOnTable(arm="b",smooth_x=0.5,distance=TABLE_WIDTH*0.9), {SUCCESS:'Fold_2',FAILURE:'Fold_2'})
        #self.add('Fold_2', Fold2(), {SUCCESS:'Smooth_2',FAILURE:FAILURE})
        self.add('Fold_2', Fold2(), {SUCCESS:'Smooth_2',FAILURE:FAILURE})
        # Reenabling #disabling smooth below to save time on demo
        self.add('Smooth_2', SmoothOnTable(arm="b",smooth_x=0.5,distance=TABLE_WIDTH*0.9), {SUCCESS:SUCCESS,FAILURE:SUCCESS})
        
class Fold1(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["bl","tl","tr","br"])
        
    def execute(self,userdata):
        pt_bl = userdata.bl
        pt_tl = userdata.tl
        pt_br = userdata.br
        pt_tr = userdata.tr
        #if not GripUtils.go_to_pts(pt_tl, -pi/2, -pi/3, pi/4, pt_tr, pi/2, pi/3, pi/4, x_offset_l=-0.04,\
        #        x_offset_r=-0.04):
        #    return FAILURE
        #FIXME Hard-coded X offsets to compensate for poor calibration. Re-calibrate and REMOVE
        '''
        if not GripUtils.grab_point(pt_tl,roll=-pi/2,yaw=-pi/3,pitch=pi/4,arm="l",x_offset=-0.04):
            return FAILURE
        if not GripUtils.grab_point(pt_tr,roll=pi/2,yaw= pi/3,pitch=pi/4,arm="r",x_offset=-0.04):
            return FAILURE
        '''
        if not GripUtils.grab_points(pt_tl,roll_l=-pi/2,yaw_l=-pi/3,pitch_l=pi/4,x_offset_l=-0.01, z_offset_l=0.02
                                    ,point_r=pt_tr,roll_r=pi/2,yaw_r= pi/3,pitch_r=pi/4,x_offset_r=-0.01, y_offset_r=0.01,z_offset_r=0.01):
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
        x_l = bl_x
        y_l = bl_y+0.005 # bit too tight
        z_l = z_r = bl_z + 0.02
        x_r = br_x
        y_r = br_y-0.005 # bit too tight
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
        z = bl_z + 0.01 # bit too low
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
        z = bl_z + 0.01 # bit too low
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
        
        return SUCCESS

class GenericUserData:
    def __init__(self):
        pass

def main(args):
    rospy.init_node("unfolding_smach_demo_node")
   
    sm = OuterStateMachine(DEFAULT_OUTCOMES)
    START_STATE = 'Clump_To_Triangle'
    #START_STATE = 'Triangle_To_Rectangle'
    #START_STATE = 'Fold_Towel'

    with sm:
         OuterStateMachine.add('Initialize',Initialize(),{SUCCESS:START_STATE,FAILURE:FAILURE})
         OuterStateMachine.add('Clump_To_Triangle',ClumpToTriangle(),{SUCCESS:'Triangle_To_Rectangle',FAILURE:'Initialize'})
         OuterStateMachine.add('Triangle_To_Rectangle',TriangleToRectangle(),{SUCCESS:'Fold_Towel',FAILURE:FAILURE})
         OuterStateMachine.add('Fold_Towel',FoldTowel(),{SUCCESS:SUCCESS,FAILURE:FAILURE})
    
    sis = smach_ros.IntrospectionServer('demo_smach_server', sm, '/SM_ROOT')
    sis.start()
    outcome = sm.execute()
    return outcome
    
if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
