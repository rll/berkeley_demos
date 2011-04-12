#!/usr/bin/env python
import roslib
roslib.load_manifest("unfolding")
import rospy
import StanceUtils
import PrimitiveUtils
import GripUtils
from image_processor.srv import *
from geometry_msgs.msg import PointStamped
from numpy import *
import sys
from dynamic_reconfigure.client import Client as ReconfigureClient
from smach import State, StateMachine
import smach_ros
from ArmMotionStates import Sweep,DEFAULT_OUTCOMES,SUCCESS,FAILURE,StateMachineAddition,NestedStateMachine,SuccessFailureState

TABLE_HEIGHT = 0.770 #was 0.78
TABLE_WIDTH = 0.98
DOWEL_X = 0.695
DOWEL_Y = 0
DOWEL_HEIGHT = 0.40

(HUMAN,AUTO) = range(2)
DETECT_MODE = AUTO
RUN_MODE = AUTO

THICK_SOCK_INCREMENT = pi/15
THIN_SOCK_INCREMENT = pi/15
(THIN_SOCK,THICK_SOCK) = range(2)
MODE = THICK_SOCK
if MODE == THIN_SOCK:
    ANGLE_INCREMENT = THIN_SOCK_INCREMENT
else:
    ANGLE_INCREMENT = THICK_SOCK_INCREMENT
    
LAYOUT_PT = PointStamped()
LAYOUT_PT.header.frame_id = "base_footprint"
LAYOUT_PT.point.x = 0.40
LAYOUT_PT.point.y = 0.0
LAYOUT_PT.point.z = TABLE_HEIGHT

TEST_LAYOUT_PT = PointStamped()
TEST_LAYOUT_PT.header.frame_id = "base_footprint"
TEST_LAYOUT_PT.point.x = 0.4
TEST_LAYOUT_PT.point.y = 0.0
TEST_LAYOUT_PT.point.z = TABLE_HEIGHT

NUM_SOCKS = 5

sock_pos = None
class GenericUserData:
    def __init__(self):
        pass
        
class SockState:
    def __init__(self,grasp_point,grasp_angle,inside_out,thick):
        self.grasp_point = grasp_point
        self.initial_grasp_point = grasp_point
        self.grasp_angle = grasp_angle
        self.inside_out = inside_out
        self.thick = thick

def configure_prosilica():
    print "Configuring prosilica"
    client = ReconfigureClient("prosilica_driver")
    client.update_configuration ({'auto_exposure':False,'exposure':0.4,'auto_gain':False,'gain':0.0,
        'auto_whitebalance':False,'whitebalance_red':114,'whitebalance_blue':300})

def failure():
    sys.exit("Hit a failure I couldn't recover from.")

def add_sock_to_match():
    if DETECT_MODE==AUTO:
        process_mono = rospy.ServiceProxy("add_sock_to_match_node/process_mono",ProcessMono)
        resp = process_mono("prosilica")
    else:
        print "Press any key to pretend to take a picture"
        raw_input()
    
def clear_matches():
    if DETECT_MODE==AUTO:
        clear_matches = rospy.ServiceProxy("clear_matches",ClearMatches)
        resp = clear_matches()
    else:
        print "Press any key to pretend to clear the matches"
        raw_input()
    
def get_matches():
    if DETECT_MODE==AUTO:
        get_matches = rospy.ServiceProxy("get_matches",GetMatches)
        resp = get_matches()
        return resp.matches
    else:
        print "Give me the list of matches as a string"
        match_str = raw_input()
        return eval(match_str)

def get_avg_hue():
    process_mono = rospy.ServiceProxy("dowel_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    return resp.params[0]

def get_states():
    if DETECT_MODE == AUTO:
        process_mono = rospy.ServiceProxy("sock_state_node/process_mono",ProcessMono)
        resp = process_mono("prosilica")
        params = {}
        for i in range(len(resp.params)):
            params[resp.param_names[i]] = resp.params[i]
        for key in ("inside_out_l","inside_out_r","thick_l","thick_r"):
            if params[key] < 0:
                params[key] = False
            else:
                params[key] = True
        grasp_points = resp.pts3d
        grasp_point_l = grasp_points[0]
        grasp_point_r = grasp_points[1]
        grasp_angle_l = -1*params["grasp_angle_l"]
        grasp_angle_r = -1*params["grasp_angle_r"]
        #Added
        if abs(grasp_angle_l) > pi/2:
            print "FAILED TO GET THE RIGHT POINT"
            (grasp_point_l,grasp_angle_l) = get_grip_point_click("l")
        inside_out_l = params["inside_out_l"]
        inside_out_r = params["inside_out_r"]
        #thick_l = params["thick_l"]
        #thick_r = params["thick_r"]
        thick_l = False
        thick_r = False
        left_sock_state = SockState(grasp_point=grasp_point_l,grasp_angle=grasp_angle_l,inside_out=inside_out_l,thick=thick_l)
        right_sock_state = SockState(grasp_point=grasp_point_r,grasp_angle=grasp_angle_r,inside_out=inside_out_r,thick=thick_r)
        
        
        return (left_sock_state,right_sock_state)
    else:
        (pt,angle) = get_grip_point_click("l")
        print "Is it flipped?"
        flipped = (raw_input()[0]=='y')
        print "Is it a thick?"
        thick = (raw_input()[0]=='y')
        left_sock_state = SockState(grasp_point=pt,grasp_angle=angle,inside_out=flipped,thick=thick)
        right_sock_state = SockState(grasp_point=pt,grasp_angle=angle,inside_out=flipped,thick=thick)
        return (left_sock_state,right_sock_state)
    

def is_inside_out():
    process_mono = rospy.ServiceProxy("is_inside_out_node/process_mono",ProcessMono)
    resp = process_mono("prosilica")
    output = {}
    for i,val in enumerate(resp.params):
        if val < 0:
            output[resp.param_names[i]] = False
        else:
            output[resp.param_names[i]] = True
    for i,sock in enumerate(("l","r")):
        print "Is %s sock inside_out? %s"%(sock,output[sock])
    return (output["l"],output["r"] )
    
def is_thick():
    process_mono = rospy.ServiceProxy("is_thick_node/process_mono",ProcessMono)
    resp = process_mono("prosilica")
    output = {}
    for i,val in enumerate(resp.params):
        if val < 0:
            output[resp.param_names[i]] = False
        else:
            output[resp.param_names[i]] = True
    for i,sock in enumerate(("l","r")):
        print "Is %s sock thick? %s"%(sock,output[sock])
    return (output["l"],output["r"] )


def get_grip_point_click(sock):
    print "Give me the grip point"
    process_mono = rospy.ServiceProxy("click_point_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    output = {}
    #for i,val in enumerate(resp.params):
    #    output[resp.param_names[i]] = val
    output["l"] = 0
    output["r"] = 0
    if sock == "l":
        pt = resp.pts3d[0]
        angle = -1*output["l"]
    else:
        pt = resp.pts3d[1]
        angle = -1*output["r"]
    return (pt,angle)
    
def get_grip_point_auto(sock):
    #StanceUtils.call_stance("look_down",5.0)
    #rospy.sleep(2.5)
    print "Give me the grip point"
    process_mono = rospy.ServiceProxy("grab_point_node/process_mono",ProcessMono)
    resp = process_mono("prosilica")
    output = {}
    for i,val in enumerate(resp.params):
        output[resp.param_names[i]] = val
    if sock == "l":
        pt = resp.pts3d[0]
        angle = -1*output["l"]
    else:
        pt = resp.pts3d[1]
        angle = -1*output["r"]
    return (pt,angle)

class ArmsUp(SuccessFailureState):
    def execute(self,userdata):
        GripUtils.open_grippers()
        StanceUtils.call_stance("arms_up",dur=5.0)
        return SUCCESS

"""    
class PickupSock(SuccessFailureState):
    def __init__(self,sock="l"):
        SuccessFailureState.__init__(self,output_keys=['grip_point'])
        self.sock = sock
        
    def execute(self,userdata):
        z_off = 0.0
        (grip_pt,angle) = get_grip_point(sock)
        if MODE==THICK_SOCK:
            OFFSET = 0.02
        else:
            OFFSET = 0.025
        
        y_offset = OFFSET*cos(angle)
        x_offset = OFFSET*sin(angle)
        #x_offset += 0.005
        z_offset = 0.02
        pitch = pi/2
        roll = pi/2
        yaw = pi/2-angle
        GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
        z_offset = -0.02
        z_offset -= 0.001
        GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
        #Drag thin socks
        if MODE == THIN_SOCK:
            y_offset += 0.02*cos(angle)
            GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
        while not GripUtils.has_object("r"):
            GripUtils.open_gripper("r")
            pitch -= ANGLE_INCREMENT
            y_offset -= 0.005*cos(angle)
            x_offset -= 0.005*sin(angle)
            z_offset += 0.0015
            GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
            GripUtils.close_gripper("r",extra_tight=True)
            break
        userdata.grip_point = grip_point
        return SUCCESS
"""

def pt3d_distance(pt1,pt2):
    return sqrt( (pt1.point.x - pt2.point.x)**2 + (pt1.point.y - pt2.point.y)**2 + (pt2.point.z - pt2.point.z) **2 )


        


"""
REAL CODE STARTS HERE
"""
           

class CollectSocks(NestedStateMachine):
    def __init__(self,title,transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["sock_locations"],output_keys=["sock_locations"])

        self.add_state('Watcher',Watcher(), {'EMPTY':SUCCESS,'NOT_EMPTY':'Pile_To_Smooth'})
        self.add_state_machine(PileToSmooth('Pile_To_Smooth', {SUCCESS:'Fix_Sock',FAILURE:'Pile_To_Smooth'}))
        self.add_state_machine(FixSock('Fix_Sock',{SUCCESS:'Store_Sock',FAILURE:'Pile_To_Smooth'}))
        #self.add_state('Pickup_Sock_For_Storing',Grab("l"),{SUCCESS:'Store_Sock',FAILURE:'Pickup_Sock_For_Storing'})
        self.add_state('Store_Sock',StoreSock(),{SUCCESS:'Watcher',FAILURE:'Recover_Sock'})
        self.add_state('Recover_Sock',RecoverSock(),{SUCCESS:'Store_Sock',FAILURE:'Pile_To_Smooth'})
        
        
class Watcher(State):
    def __init__(self):
        self.sock_num = 0
        State.__init__(self,['EMPTY','NOT_EMPTY'],input_keys=[],output_keys=["sock_num"])

    def execute(self,userdata):
        #Update my tally
    
        #Check if there is a sock. 
        #if more_socks():
        if NUM_SOCKS > self.sock_num:
            userdata.sock_num = self.sock_num
            self.sock_num += 1
            return 'NOT_EMPTY'
        else:
            return 'EMPTY'
            

def more_socks():
    print "Are there more socks?"
    yn = raw_input()
    return yn[0] == 'y' or yn[0] == 'Y'

class HumanInput(SuccessFailureState):
    def __init__(self,input_text):
        self.input_text = input_text
        SuccessFailureState.__init__(self)
        
        
    def execute(self,userdata):
        print self.input_text
        raw_input()
        return SUCCESS
    
class PileToSmooth(NestedStateMachine):
    #Takes no input and returns no output
    def __init__(self, title, transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["sock_num"],output_keys=[])
        """
        pile_to_clump = StateMachineAddition('Pile_To_Clump',PileToClump(),{SUCCESS:'Clump_To_Smooth',FAILURE:FAILURE})
        clump_to_smooth = StateMachineAddition('Clump_To_Smooth',ClumpToSmooth(),{SUCCESS:SUCCESS,FAILURE:FAILURE})
        """
        self.add_state('Pile_To_Clump',PileToClump(),{SUCCESS:'Clump_To_Smooth',FAILURE:FAILURE})
        self.add_state_machine(ClumpToSmooth('Clump_To_Smooth',{SUCCESS:SUCCESS,FAILURE:FAILURE}))
        
class PileToClump(SuccessFailureState):
    
    def __init__(self):
        self.sock_count = 0
        SuccessFailureState.__init__(self,input_keys=["sock_num"])

    def execute(self,userdata):
        
        if RUN_MODE==HUMAN:
            print "Put the sock flat on the table"
            raw_input() #FIXME
        else:
            StanceUtils.call_stance("arms_up",3.0)
            arm = retrieve_sock(userdata.sock_num)
            layout_sock(LAYOUT_PT,direction=arm)
            if arm == "r":
                StanceUtils.call_stance("arms_up",5.0)
                Grab("l").execute(userdata)
                layout_sock(LAYOUT_PT,direction="l")
            #StanceUtils.call_stance("arms_up",5.0)
            self.sock_count += 1
        return SUCCESS        

class FixSock(NestedStateMachine):

    #Fixes the sock, and is holding it at the end of the process
    def __init__(self,title,transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["sock_locations"],output_keys=["sock_locations"])
        """
        inside_out_checker = StateMachineAddition('Inside_Out_Checker',InsideOutChecker(),{"TRUE":'Pickup_Sock',"FALSE":'Flip_Sock'})
        #If we fail to pick up the sock, we look for its grasp points again
        pickup_sock_flat = StateMachineAddition('Pickup_Sock_Flat',PickupSockFlat(),{SUCCESS:SUCCESS,FAILURE:'Inside_Out_Checker'}) 
        flip_sock = StateMachineAddition('Flip Sock',FlipSock(),{SUCCESS:SUCCESS,FAILURE:FAILURE})
        """
        self.add_state('Inside_Out_Checker',InsideOutChecker(),{"FALSE":'Picture_Taker',"TRUE":'Flip_Sock'})
        self.add_state('Picture_Taker',PictureTaker(),{SUCCESS:'Pickup_Sock_Flat',FAILURE:FAILURE})
        self.add_state('Pickup_Sock_Flat',PickupSockFlat(),{SUCCESS:SUCCESS,FAILURE:'Inside_Out_Checker'})
        self.add_state_machine(FlipSock('Flip_Sock',{SUCCESS:'Picture_Taker',FAILURE:FAILURE}))

class PictureTaker(SuccessFailureState):
    def execute(self,userdata):
        StanceUtils.call_stance("arms_up",5.0)
        add_sock_to_match()
        return SUCCESS

class InsideOutChecker(State):
    def __init__(self):
        State.__init__(self,["TRUE","FALSE"],input_keys=[],output_keys=["sock_state"])
        
    def execute(self,userdata):
        (l_state,r_state) = get_states()
        #For now, we only look at the left sock.
        userdata.sock_state = l_state
        if l_state.inside_out:
            return "TRUE"
        else:
            return "FALSE"

class PickupSockFlat(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["sock_state"],output_keys=[])
        
    def execute(self,userdata):
        #grip_pt = userdata.sock_state.grasp_point
        #angle = userdata.sock_state.grasp_angle
        #Pick up sock in a flat configuration

        pass
        return SUCCESS
        
class RecoverSock(SuccessFailureState):

    def execute(self,userdata):
        pass
        return SUCCESS
        
       
class FlipSock(NestedStateMachine):
    #Flips the sock, and ends with it laying in a flat configuration
    def __init__(self,title,transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["sock_state"])
        if RUN_MODE==AUTO:
            self.add_state('Pickup_Sock_To_Flip',PickupSockToFlip(),{SUCCESS:'Shimmy_Down_Dowel',FAILURE:FAILURE})
            self.add_state('Shimmy_Down_Dowel',ShimmyDownDowel(),{SUCCESS:'Spread_Out_Held_Sock',FAILURE:FAILURE})
            self.add_state_machine(SpreadOutHeldSock('Spread_Out_Held_Sock',{SUCCESS:SUCCESS,FAILURE:FAILURE}))
        else:
            self.add_state('Flip_Sock_Placeholder',HumanInput("Flip the sock"),{SUCCESS:SUCCESS,FAILURE:FAILURE})
        
class PickupSockToFlip(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["sock_state"],output_keys=["sock_state"])
        
    def execute(self,userdata):
        if RUN_MODE==AUTO:
            grip_pt = userdata.sock_state.grasp_point
            angle = userdata.sock_state.grasp_angle
            if userdata.sock_state.thick:
                mode = THICK_SOCK
            else:
                mode = THIN_SOCK
            pickup_sock(mode=mode,grip_pt=grip_pt,angle=angle)
            open_sock()
        else:
            print "Pickup Sock for flipping"
            raw_input()
        return SUCCESS
        
        
class ShimmyDownDowel(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["sock_state"],output_keys=["sock_state"])
        
    def execute(self,userdata):
        #Flips the sock, very suggestively
        sock_width = DOWEL_HEIGHT*0.7
        userdata.sock_state.width = sock_width*0.7
        go_down_dowel(depth=sock_width)
        take_off_dowel(arm="r")
        #Then returns nothing
        return SUCCESS
        
class SpreadOutHeldSock(NestedStateMachine):
    #Flips the sock, and ends with it laying in a flat configuration
    def __init__(self,title,transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["sock_state"],output_keys=["sock_state"])
        self.add_state('Layout_Sock',LayoutSock('r'),{SUCCESS:'Smooth_Sock',FAILURE:FAILURE})
        self.add_state('Smooth_Sock',Smooth('b'),{SUCCESS:SUCCESS,FAILURE:SUCCESS})
        
class LayoutSock(SuccessFailureState):
    def __init__(self,direction,clump=False):
        SuccessFailureState.__init__(self,input_keys=["sock_state"],output_keys=["sock_state",'location','distance'])
        self.direction = direction
        self.clump = clump
        
    def execute(self,userdata):
        #location = userdata.sock_state.grasp_point
        location = LAYOUT_PT
        width = userdata.sock_state.width
        userdata.location = location
        userdata.distance = width*0.6
        if self.clump:
            width *= 2
        if self.direction == "l":
            drag_yaw = -pi/2
            drag_amount = width*1.2
            drag_arm = "l"
        else:
            drag_yaw = pi/2
            drag_amount = width*-1.2
            drag_arm = "r"
        
        lift_height = abs(drag_amount)
        init_offset = drag_amount * -0.5
        if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,y_offset = 2*init_offset, z_offset = lift_height,dur=3.0):
            return FAILURE
        if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,y_offset = 2*init_offset, z_offset = lift_height/1.5,dur=3.0):
            return FAILURE
        if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,z_offset = 0.01,y_offset=drag_amount+init_offset,dur=5.0):
            return FAILURE
        if not StanceUtils.call_stance("open_both",1.0):
            return FAILURE
        return SUCCESS
        
class LayoutSockUnkown(SuccessFailureState):
    def __init__(self,direction,clump=False):
        SuccessFailureState.__init__(self,input_keys=["location","sock_width"],output_keys=['location','distance'])
        self.direction = direction
        self.clump = clump
        
    def execute(self,userdata):
        location = userdata.location
        width = userdata.sock_width
        userdata.distance = width
        if self.clump:
            width *= 2
        if self.direction == "l":
            drag_yaw = -pi/2
            drag_amount = width*1.5
            drag_arm = "l"
        else:
            drag_yaw = pi/2
            drag_amount = width*-1.5
            drag_arm = "r"
        
        lift_height = abs(drag_amount)
        init_offset = drag_amount * -0.5
        if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,y_offset = 2*init_offset, z_offset = lift_height,dur=3.0):
            return FAILURE
        if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,y_offset = 2*init_offset, z_offset = lift_height/1.5,dur=3.0):
            return FAILURE
        if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,z_offset = 0.01,y_offset=drag_amount+init_offset,dur=5.0):
            return FAILURE
        return SUCCESS
     
class Grab(SuccessFailureState):
    def __init__(self,side):
        SuccessFailureState.__init__(self,input_keys=[],output_keys=["init_location","width_guess"])
        self.side = side
        
    def execute(self,userdata):
        if RUN_MODE==AUTO:
            if self.side == "l":
                finder = "far_left_finder_node" 
                approach_yaw = -pi/2
                pickup_arm = "l"
            else:
                finder = "far_right_finder_node"
                approach_yaw = pi/2
                pickup_arm = "r"
    
            process_mono = rospy.ServiceProxy("%s/process_mono"%finder,ProcessMono)
            resp = process_mono("wide_stereo/left")
            pt = resp.pts3d[0]
            pt_opp = resp.pts3d[1]
            userdata.width_guess = pt3d_distance(pt,pt_opp)


            if self.side == "l":
                userdata.init_location = pt
            else:
                userdata.init_location = pt_opp
            if not GripUtils.grab_point(pt,roll=pi/2,yaw=approach_yaw,pitch=pi/4,arm=pickup_arm,z_offset = 0.02,x_offset = -0.0125):
                return FAILURE
            return SUCCESS
        else:
            userdata.init_location = PointStamped()
            print "Grab the sock"
            raw_input()
            return SUCCESS

class Smooth(SuccessFailureState):
    def __init__(self, arm="b", input_keys=[]):
        SuccessFailureState.__init__(self, input_keys=input_keys)
        self.arm = arm
    def execute(self, userdata):
        StanceUtils.call_stance("arms_up",3.0)
        StanceUtils.call_stance("smooth1",5.0)
        StanceUtils.call_stance("smooth2",2.5)
        StanceUtils.call_stance("smooth3",3.0)
        StanceUtils.call_stance("arms_up",3.0)
        return SUCCESS
        """
        self.location = userdata.location
        self.distance = userdata.distance
        initial_separation = 0.11
        StanceUtils.call_stance("arms_up",3.0)
        #return SUCCESS #FIXME
        result = SUCCESS
        if self.arm=="b":
            #Put arms together, with a gap of initial_separation between grippers
            if not GripUtils.go_to_pts(point_l=self.location,grip_r=True, grip_l=True, point_r=self.location,
                    roll_l=0,yaw_l=-pi/2,pitch_l=-pi/2,y_offset_l=initial_separation/2.0,z_offset_l=0.05
                    ,link_frame_l="l_wrist_back_frame",
                    roll_r=0,yaw_r=pi/2,pitch_r=-pi/2,y_offset_r=-1*initial_separation/2.0,z_offset_r=0.05
                    ,link_frame_r="r_wrist_back_frame",dur=4.0):
                result = FAILURE
            if not GripUtils.go_to_pts(point_l=self.location,grip_r=True, grip_l=True, point_r=self.location,
                    roll_l=0,yaw_l=-pi/2,pitch_l=-pi/2,y_offset_l=initial_separation/2.0,z_offset_l=-0.01, 
                    link_frame_l="l_wrist_back_frame",
                    roll_r=0,yaw_r=pi/2,pitch_r=-pi/2,y_offset_r=-1*initial_separation/2.0,z_offset_r=-0.01, 
                    link_frame_r="r_wrist_back_frame",dur=2.0):
                result = FAILURE
            if not GripUtils.go_to_pts(point_l=self.location,grip_r=True, grip_l=True, point_r=self.location,
                    roll_l=0,yaw_l=-pi/2,pitch_l=-pi/2,y_offset_l=initial_separation/2.0,z_offset_l=0.05
                    ,link_frame_l="l_wrist_back_frame",
                    roll_r=0,yaw_r=pi/2,pitch_r=-pi/2,y_offset_r=-1*initial_separation/2.0,z_offset_r=0.05
                    ,link_frame_r="r_wrist_back_frame",dur=4.0):
                result = FAILURE
            #pat only
        
            if not GripUtils.go_to_pts(point_l=self.location,grip_r=True, grip_l=True, point_r=self.location,
                    roll_l=0,yaw_l=-pi/2,pitch_l=-pi/2,
                    y_offset_l=(self.distance+initial_separation)/2.0, z_offset_l=-0.00,
                    link_frame_l="l_wrist_back_frame",
                    roll_r=0,yaw_r=pi/2,pitch_r=-pi/2,
                    y_offset_r=-1*(self.distance+initial_separation)/2.0, z_offset_r=-0.00,
                    link_frame_r="r_wrist_back_frame",dur=2.0):
                result = FAILURE
         
        else:
            #Right is negative in the y axis
            if self.arm=="r":
                y_multiplier = -1
            else:
                y_multiplier = 1
            if not GripUtils.go_to_pt(point=self.location,grip=True,roll=pi/2,yaw=0,pitch=-pi/2,
                    z_offset=0.05,arm=self.arm,
                    link_frame="%s_wrist_back_frame"%self.arm,dur=4.0):
                result = FAILURE
            if not GripUtils.go_to_pt(point=self.location,grip=True,roll=pi/2,yaw=0,pitch=-pi/2,
                    z_offset=-0.01,arm=self.arm,
                    link_frame="%s_wrist_back_frame"%self.arm,dur=2.0):
                result = FAILURE
            if not GripUtils.go_to_pt(point=self.location,grip=True,roll=pi/2,yaw=0,pitch=-pi/2,
                    y_offset=y_multiplier*self.distance,z_offset=-0.01,arm=self.arm,
                    link_frame="%s_wrist_back_frame"%self.arm,dur=2.0):
                result = FAILURE
        StanceUtils.call_stance("arms_up",5.0)
        return result
    """
        
class StretchSock(SuccessFailureState):
    def __init__(self,final_location=None):
        SuccessFailureState.__init__(self,input_keys=["sock_width"],output_keys=["location","distance"])
        if not final_location:
            """
            self.final_location = PointStamped()
            self.final_location.point.x = 0.35
            self.final_location.point.y = 0.0
            self.final_location.point.z = TABLE_HEIGHT
            self.final_location.header.frame_id = 'base_footprint'
            """
            self.final_location = LAYOUT_PT
        else:
            self.final_location = final_location
        
    def execute(self,userdata):
        lift_height = 0.25
        location = self.final_location
        width = userdata.sock_width
        left_offset = width/2.0
        right_offset = -1*width/2.0
        stretch_factor = 1.0
        userdata.location = location
        userdata.distance=width*0.6
        x_off = 0.0
        print "Moving to (%f,%f,%f)"%(location.point.x,location.point.y,location.point.z)
        print "Width is %f"%(width)
        if not GripUtils.go_to_pts(point_l=location,grip_r=True, grip_l=True, point_r=location,
                    roll_l=pi/2,yaw_l=-pi/2,pitch_l=pi/4,x_offset_l=x_off,y_offset_l=left_offset,z_offset_l=lift_height,
                    roll_r=pi/2,yaw_r=pi/2,pitch_r=pi/4,x_offset_r=x_off,y_offset_r=right_offset,z_offset_r=lift_height
                    ,dur=4.0):
                return FAILURE
        if not GripUtils.go_to_pts(point_l=location,grip_r=True, grip_l=True, point_r=location,
                    roll_l=pi/2,yaw_l=-pi/2,pitch_l=pi/4,x_offset_l=x_off,y_offset_l=left_offset*stretch_factor,z_offset_l=lift_height,
                    roll_r=pi/2,yaw_r=pi/2,pitch_r=pi/4,x_offset_r=x_off,y_offset_r=right_offset*stretch_factor,z_offset_r=lift_height
                    ,dur=4.0):
                return FAILURE
        if not GripUtils.go_to_pts(point_l=location,grip_r=True, grip_l=True, point_r=location,
                    roll_l=pi/2,yaw_l=-pi/2,pitch_l=pi/4,y_offset_l=left_offset*stretch_factor,z_offset_l=0.02,
                    roll_r=pi/2,yaw_r=pi/2,pitch_r=pi/4,y_offset_r=right_offset*stretch_factor,z_offset_r=0.02
                    ,dur=4.0):
                return FAILURE
        StanceUtils.call_stance("arms_up",5.0)
        
        return SUCCESS


class StoreSock(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["sock_locations"],output_keys=["sock_location"])
        self.sock_count = 0
        
    def execute(self,userdata):
        if RUN_MODE==AUTO:
            #Places the sock in a location, depending on its current sock count.
            store_sock(self.sock_count,pickup=True)
            self.sock_count += 1
            userdata.sock_locations.append(self.location_of_sock_num(self.sock_count))
            return SUCCESS
        else:
            print "Store the sock in bin %d"%self.sock_count
            raw_input()
            self.sock_count += 1
            userdata.sock_locations.append(self.location_of_sock_num(self.sock_count))
            return SUCCESS
        
    def location_of_sock_num(self,i):
        #Location as some function of the number. For now
        return PointStamped() #FIXME
            
def store_sock(i,pickup=False):
    num_per_side = 3
    if i < num_per_side:
        arm = "l"
        y_dir = 1
    else:
        arm = "r"
        y_dir = -1
    if pickup:
        StanceUtils.call_stance("arms_up",5.0)
        #hack
        userdata = GenericUserData()
        userdata.width_guess = 0
        Grab(arm).execute(userdata)
    StanceUtils.call_stance("arms_up_grip",5.0)
    #Save, for now
    if i>= 3:
        i += 1 
    i = i%num_per_side
    x = 0.36 + 0.12*i 
    y = y_dir * TABLE_WIDTH / 2.0 + y_dir * 0.02
    z = TABLE_HEIGHT + 0.05
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,pitch=pi/4,yaw=y_dir*pi/2,grip=True,frame="base_footprint",arm=arm,dur=5.0)
    z = TABLE_HEIGHT+0.01
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,pitch=pi/4,yaw=y_dir*pi/2,grip=True,frame="base_footprint",arm=arm,dur=2.0)
    y = y_dir * TABLE_WIDTH / 2.0 - y_dir * 0.12
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,pitch=pi/4,yaw=y_dir*pi/2,grip=True,frame="base_footprint",arm=arm,dur=2.0)
    GripUtils.open_gripper(arm)
    StanceUtils.call_stance("arms_up",5.0)
    
def retrieve_sock(i):
    num_per_side = 3
    if i < num_per_side:
        arm = "l"
        y_dir = 1
    else:
        arm = "r"
        y_dir = -1
    if i >= 3:
        i += 1
    i = i%num_per_side
    x = 0.36 + 0.12*i 
    y = y_dir * TABLE_WIDTH / 2.0 - y_dir * 0.12 #was 0.08
    z = TABLE_HEIGHT + 0.05
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,pitch=pi/2,yaw=y_dir*pi/2,grip=False,frame="base_footprint",arm=arm,dur=5.0)
    z = TABLE_HEIGHT - 0.02
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,pitch=pi/2,yaw=y_dir*pi/2,grip=False,frame="base_footprint",arm=arm,dur=2.0)
    GripUtils.close_gripper(arm)
    z = TABLE_HEIGHT + 0.05
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,pitch=pi/2,yaw=y_dir*pi/2,grip=True,frame="base_footprint",arm=arm,dur=5.0)
    
    return arm

class ClumpToSmooth(NestedStateMachine):
    def __init__(self,title,transitions=None,final_location=None):
        
        NestedStateMachine.__init__(self,title,transitions,input_keys=[],output_keys=[])
        
        if RUN_MODE==AUTO:
            #self.add_state('Init', ArmsUp(), {SUCCESS:SUCCESS,FAILURE:FAILURE})
            #self.add_state('Init', ArmsUp(), {SUCCESS:'Grab_Clump',FAILURE:'Init'})
            #self.add_state('Grab_Clump', Grab("r"), {SUCCESS:'First_Layout', FAILURE:'Init'},{'init_location':'location','width_guess':'sock_width'})
            #self.add_state('First_Layout', LayoutSockUnkown("r"), {SUCCESS:'Let_Go',FAILURE:'Init'})
            #self.add_state('Let_Go', ArmsUp(), {SUCCESS: 'Grab_Left', FAILURE:'Init'})
            #self.add_state('Grab_Left', Grab("l"),{SUCCESS: 'Second_Layout', FAILURE:'Init'},{'init_location':'location','width_guess':'sock_width'})
            #self.add_state('Second_Layout', LayoutSockUnkown("l"), {SUCCESS: 'Grab_Right', FAILURE:'Let_Go'})
            #self.add_state('Grab_Right', Grab("r"), {SUCCESS:'Stretch_Sock',FAILURE:'Grab_Right'}, {'width_guess':'sock_width'})
            #self.add_state('Stretch_Sock', StretchSock(final_location), {SUCCESS:'Smooth_Sock',FAILURE:'Smooth_Sock'})
            self.add_state('Smooth_Sock', Smooth("b"), {SUCCESS:SUCCESS,FAILURE:SUCCESS})
            pass
        else:
        
            self.add_state('Clump_To_Smooth_Placeholder',HumanInput("Smooth the sock in front of me"), {SUCCESS:SUCCESS,FAILURE:FAILURE})
        

class PairSocks(NestedStateMachine):
    def __init__(self,title,transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["sock_locations"],output_keys=[])
        self.add_state('Pair_Computer',PairComputer(),{SUCCESS:'Pair_Watcher',FAILURE:FAILURE})
        self.add_state('Pair_Watcher',PairWatcher(),{'NOT_EMPTY':'Pair_Two_Socks','EMPTY':SUCCESS})
        self.add_state_machine(PairTwoSocks('Pair_Two_Socks',{SUCCESS:'Pair_Watcher',FAILURE:FAILURE}))
        
class PairComputer(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=[],output_keys=["pairs"])
        
    def execute(self,userdata):
        matches = get_matches()
        pairs = []
        for i,j in enumerate(matches):
            if i < j:
                pairs.append([i,j])
        userdata.pairs = pairs
        return SUCCESS

class PairWatcher(State):
    def __init__(self):
        self.i = 0
        State.__init__(self,['EMPTY','NOT_EMPTY'],input_keys=["pairs"],output_keys=["pair"])

    def execute(self,userdata):
        pairs = userdata.pairs
        if len(pairs) > self.i:
            pair = pairs[self.i]
            self.i += 1
            userdata.pair = pair
            print "Pairing socks %d and %d"%(pair[0],pair[1])
            return 'NOT_EMPTY'
        else:
            return 'EMPTY'
            
class PairIterator(State):
    def __init__(self):
        State.__init__(self,['EMPTY','NOT_EMPTY'],input_keys=["pair"],output_keys=["sock_num"])
        
    def execute(self,userdata):
        pair = userdata.pair
        if len(pair) > 0:
            sock_num = pair.pop(0)
            userdata.sock_num = sock_num
            return 'NOT_EMPTY'
        else:
            return 'EMPTY'

class PairTwoSocks(NestedStateMachine):
    def __init__(self,title,transitions=None):
        NestedStateMachine.__init__(self,title,transitions,input_keys=["pair"],output_keys=[])
        """
        self.add_state('Retrieve_Sock1',RetrieveSock(True),{SUCCESS:'Pickup_Sock1', FAILURE:FAILURE})
        self.add_state('Pickup_Sock1',PickupSockToFlip(),{SUCCESS:'Put_On_Dowel1',FAILURE:FAILURE})
        self.add_state('Put_On_Dowel1',PutOnDowel(),{SUCCESS:'Retrieve_Sock2',FAILURE:FAILURE})
        self.add_state('Retrieve_Sock2',RetrieveSock(False),{SUCCESS:'Pickup_Sock2', FAILURE:FAILURE})
        self.add_state('Pickup_Sock2',PickupSockToFlip(),{SUCCESS:'Put_On_Dowel2',FAILURE:FAILURE})
        self.add_state('Put_On_Dowel2',PutOnDowel(),{SUCCESS:'Take_Both_Off_Dowel',FAILURE:FAILURE})
        self.add_state('Take_Both_Off_Dowel',TakeOffDowel(),{SUCCESS:'Put_In_Pile',FAILURE:FAILURE})
        self.add_state('Put_In_Pile',PutInPile(),{SUCCESS:SUCCESS,FAILURE:FAILURE})
        """
        self.add_state('Pair_Iterator',PairIterator(),{'NOT_EMPTY':'Pile_To_Smooth_For_Pairing','EMPTY':'Take_Both_Off_Dowel'})
        self.add_state_machine(PileToSmooth('Pile_To_Smooth_For_Pairing', {SUCCESS:'Get_States',FAILURE:'Pile_To_Smooth_For_Pairing'}))
        self.add_state('Get_States',GetStates(),{SUCCESS:'Pickup_Sock',FAILURE:FAILURE})
        self.add_state('Pickup_Sock',PickupSockToFlip(),{SUCCESS:'Put_On_Dowel',FAILURE:'Pickup_Sock'})
        self.add_state('Put_On_Dowel',PutOnDowel(),{SUCCESS:'Pair_Iterator',FAILURE:'Pickup_Sock'})
        self.add_state('Take_Both_Off_Dowel',TakeOffDowel(),{SUCCESS:'Put_In_Pile',FAILURE:FAILURE})
        self.add_state('Put_In_Pile',PutInPile(),{SUCCESS:SUCCESS,FAILURE:FAILURE})

class RetrieveSock(SuccessFailureState):
    def __init__(self,first):
        self.first = first
        SuccessFailureState.__init__(self,input_keys=["pair"],output_keys=["sock_state"])
        
    def execute(self,userdata):
        if self.first:
            sock = userdata.pair[0]
        else:
            sock = userdata.pair[1]
        if RUN_MODE==AUTO:
            arm = retrieve_sock(sock)
            layout_sock(LAYOUT_PT,direction="l",arm=arm)
            data = GenericUserData()
            data.location = LAYOUT_PT
            data.distance = 0.2
            Smooth("b").execute(data)
            StanceUtils.call_stance("arms_up",5.0)
        else:
            print "Retrieve sock %i and lay it flat on the table"%sock
            raw_input()
        userdata.sock_state = get_states()[0]
        return SUCCESS

class GetStates(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=[],output_keys=["sock_state"])
    def execute(self,userdata):
        userdata.sock_state = get_states()[0]
        return SUCCESS

class PutOnDowel(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=[],output_keys=[])
        
    def execute(self,userdata):
        if RUN_MODE==AUTO:
            #Puts on Dowel
            sock_width = DOWEL_HEIGHT*0.7
            go_down_dowel(depth=sock_width,upside_down=True)
            #Then returns nothing
        else:
            print "Put on dowel"
            raw_input()
        return SUCCESS

class TakeOffDowel(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=[],output_keys=[])
    
    def execute(self,userdata):
        if RUN_MODE==AUTO:
            take_off_dowel(arm="r")
        else:
            print "Take off the dowel"
            raw_input()
        return SUCCESS
        
class PutInPile(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["pair"],output_keys=[])
        
    def execute(self,userdata):
        if RUN_MODE==AUTO:
            #store_sock(userdata.pair[0])
            StanceUtils.call_stance("put_in_bucket",5.0)
            GripUtils.open_gripper("r")
            StanceUtils.call_stance("arms_up",3.0)
        else:
            print "Put in the pile"
            raw_input()
        return SUCCESS
        
"""        
class PairSocks(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["sock_locations"],output_keys=[])
        pass
        
    def execute(self,userdata):
        matches = get_matches()
        for i,j in enumerate(matches):
            if i <= j:
                print "Pair: %d and %d"%(i,j)
        for i,j in enumerate(matches):
            if i < j:
                if RUN_MODE==AUTO:
                    retrieve_sock(i)
                    
                else:
                    print "Put sock %d in bin %d"%(i,j)
        return SUCCESS
"""
        
def run_demo():
    if DETECT_MODE==AUTO:
        configure_prosilica()
    StanceUtils.call_stance("look_down_more",2.0)
    clear_matches()
    assert len(get_matches()) == 0
    sm = StateMachine(DEFAULT_OUTCOMES)
    sm.userdata.sock_images = []
    sm.userdata.sock_locations = []
    with sm:
        #CollectSocks('Collect_Socks',{SUCCESS:'Pair_Socks',FAILURE:FAILURE}).add_states()
        #PairSocks('Pair_Socks',{SUCCESS:SUCCESS,FAILURE:FAILURE}).add_states()
        StateMachine.add('FixSock',FixSock(), transitions={SUCCESS:SUCCESS, FAILURE:FAILURE})
    

    sis = smach_ros.IntrospectionServer('demo_smach_server', sm, '/SM_ROOT')
    sis.start()
    outcome = sm.execute()

    
    return
    
def run_grasp():
    quit = False
    while not quit:
        print "d for dress mode, t for thick mode"
        val = raw_input()[0]
        StanceUtils.call_stance("open_both",3.0)
        StanceUtils.call_stance("arms_up",5.0)
        if val == 'd':
            pickup_sock(THIN_SOCK)
        else:
            pickup_sock(THICK_SOCK)
        open_sock()
        #StanceUtils.call_stance("open_left",3.0)
        
def pickup_sock(mode,grip_pt,angle):
    sock="l"
    z_off = -0.01

    #sock_state = get_states()[0]
    #grip_pt = sock_state.grasp_point
    #angle = sock_state.grasp_angle
    #if sock_state.thick:
    #    mode = THICK_SOCK
    #else:
    #    mode = THIN_SOCK
    if mode==THICK_SOCK:
        OFFSET = 0.035 #was 0.02
        angle_increment = pi/10
    else:
        angle_increment = pi/12
        OFFSET = 0.03
    
    y_offset = OFFSET*cos(angle)
    x_offset = OFFSET*sin(angle)
    #x_offset += 0.005
    z_offset = 0.02
    pitch = pi/2
    roll = pi/2
    yaw = pi/2-angle
    GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
    z_offset = -0.01
    z_offset -= 0.001
    GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
    #Drag thin socks
    if mode == THIN_SOCK:
        y_offset += 0.02*cos(angle)
        z_offset -= 0.007
        GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
        z_offset += 0.005 #Added in
    while not GripUtils.has_object("r"):
        StanceUtils.call_stance("open_right",2.0)
        pitch -= angle_increment
        y_offset -= 0.005*cos(angle)
        x_offset -= 0.005*sin(angle)
        z_offset += 0.0010
        GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)

        if mode == THIN_SOCK:
            GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset+0.007,grip=False,dur=5.0) #was .015
            GripUtils.close_gripper("r",extra_tight=True)

        else:
            GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
            if not GripUtils.close_gripper("r",extra_tight=True):
                return False
        break
    return True
    
def open_sock():
    x=0.5
    y=0.0
    z=TABLE_HEIGHT+0.4
    frame="base_footprint"
    ##Ensure I don't do a 360
    #GripUtils.go_to(x=x,y=y+0.007,z=z,roll=0,yaw=pi/2,pitch=-pi/8,grip=True,frame=frame,arm="r",dur=5.0)
    #old strategy
    GripUtils.go_to(x=x,y=y+0.007,z=z,roll=pi/2,yaw=pi/2,pitch=-pi/8,grip=True,frame=frame,arm="r",dur=2.0)
    """
    GripUtils.go_to(x=x,y=y+0.05,z=z,roll=pi/2,yaw=-pi/2,pitch=0,grip=False,frame=frame,arm="l",dur=5.0)
    GripUtils.go_to(x=x,y=y-0.004,z=z+0.01,roll=pi/2,yaw=-pi/2,pitch=pi/5,grip=False,frame=frame,arm="l",dur=5.0)
    GripUtils.go_to(x=x,y=y-0.0035,z=z+0.001,roll=pi/2,yaw=-pi/2,pitch=pi/5,grip=True,frame=frame,arm="l",dur=2.0) #changed from -0.007 to -0.0065
    """
    y_offset = 0.008 #Was 0.018
    z_offset = 0.00
    has_object = False
    num_iters = 0
    while not has_object:
        GripUtils.open_gripper("l")
        GripUtils.go_to(x=x,y=y+0.05,z=z+z_offset,roll=pi/2,yaw=-pi/2,pitch=0,grip=False,frame=frame,arm="l",dur=3.0)
        GripUtils.go_to(x=x,y=y+y_offset,z=z+0.01+z_offset,roll=pi/2,yaw=-pi/2,pitch=pi/5,grip=False,frame=frame,arm="l",dur=2.0) #was +0.01
        GripUtils.go_to(x=x,y=y+y_offset+0.003,z=z+0.001+z_offset,roll=pi/2,yaw=-pi/2,pitch=pi/5,grip=True,frame=frame,arm="l",dur=2.0) #changed from -0.007 to -0.0065
        GripUtils.close_gripper("l",extra_tight=True)
        has_object = GripUtils.has_object("l")
        num_iters += 1
        if num_iters >= 3:
            has_object = True
        #has_object = True
        z_offset -= 0.01
    #GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,yaw=pi/2,pitch=0,grip=True,frame=frame,arm="r",dur=5.0)
    #GripUtils.go_to(x=x,y=y+0.04,z=z+0.05,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=False,frame=frame,arm="l",dur=5.0)    
    #GripUtils.go_to(x=x,y=y+0.04,z=z+0.005,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=False,frame=frame,arm="l",dur=5.0)
    #GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,yaw=pi/2,pitch=-pi/16,grip=True,frame=frame,arm="r",dur=5.0)
    #GripUtils.go_to(x=x,y=y+0.06,z=z-0.025,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=False,frame=frame,arm="l",dur=5.0)
    #GripUtils.go_to(x=x,y=y+0.025,z=z-0.225,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=True,frame=frame,arm="l",dur=1.0)
    #GripUtils.go_to(x=x,y=y+0.025,z=z,roll=pi/2,yaw=-pi/2,pitch=0,grip=True,frame=frame,arm="l",dur=5.0)
    
    
    
    open_amt = 0.025
    GripUtils.go_to_multi   (x_l=x,y_l=y+open_amt,z_l=z+0.01,roll_l=pi/2,yaw_l=-pi/2,pitch_l=0,grip_l=True,frame_l=frame
                            ,x_r=x,y_r=y-open_amt,z_r=z+0.01,roll_r=pi/2,yaw_r=pi/2,pitch_r=0,grip_r=True,frame_r=frame
                            ,dur=2.0)
    
#Initial pickup of clump
def initial_pickup(arm):
    success = True

    """
    process_mono = rospy.ServiceProxy("clump_center_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    z_offset = 0.02
    GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm=arm,z_offset=z_offset,grip=False,dur=5.0)
    GripUtils.close_gripper(arm)
    while not GripUtils.has_object(arm):
        z_offset -= 0.005
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm=arm,z_offset=z_offset,grip=False,dur=5.0)
        GripUtils.close_gripper(arm)
    """
    pt = grab_far_right(arm)
    return pt
    
#Grab the far right point
def grab_far_right(arm):

    process_mono = rospy.ServiceProxy("far_right_finder_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    GripUtils.grab_point(pt,roll=-pi/2,yaw=pi/2,arm=arm,z_offset = 0.02,x_offset = -0.02)
    return pt

#Grab the far left point
def grab_far_left(arm):

    process_mono = rospy.ServiceProxy("far_left_finder_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    pt_opp = resp.pts3d[1]
    GripUtils.grab_point(pt,roll=-pi/2,yaw=-pi/2,arm=arm,z_offset = 0.02,x_offset = -0.02)
    return pt


                            
def flip_sock(pt,arm):
    wiggle_down_dowel()
    StanceUtils.call_stance("arms_up",5.0)
    take_off_dowel(pt,arm=arm)
    smooth(pt,arm)
    StanceUtils.call_stance("arms_up",5.0)
    
#Smooth at a place w/ grip point of pt, on arm side
def smooth(pt,side):
    y_offset = -0.08
    x_offset = 0.02
    x = pt.point.x + x_offset
    y = pt.point.y + y_offset
    z = pt.point.z
    frame = "base_footprint"
    
    x_l = x
    x_r = x
    y_l = y
    y_r = y
    z_l = z_r = z
    roll_l = roll_r = 0
    yaw_l = -pi/2
    yaw_r = pi/2
    pitch_l = pitch_r=pi/6
    grip_l = grip_r = True
    GripUtils.go_to_multi   (x_l=x,y_l=y_l,z_l=z+0.04,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame
                            ,x_r=x,y_r=y_r,z_r=z+0.04,roll_r=roll_l,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame
                            ,dur=5.0)
    GripUtils.go_to_multi   (x_l=x,y_l=y_l,z_l=z,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame
                            ,x_r=x,y_r=y_r,z_r=z,roll_r=roll_l,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame
                            ,dur=3.0)
    y_l += 0.06
    y_r -= 0.06
    pitch_l = pi/4
    pitch_r = pi/4
    
    GripUtils.go_to_multi   (x_l=x,y_l=y_l,z_l=z+0.01,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame
                            ,x_r=x,y_r=y_r,z_r=z+0.01,roll_r=roll_l,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame
                            ,dur=5.0)

def go_down_dowel(depth = DOWEL_HEIGHT/2,upside_down=False):
    #detect = not upside_down
    detect = False
    open_amt = 0.025
    x = DOWEL_X
    y = DOWEL_Y
    z = DOWEL_HEIGHT+TABLE_HEIGHT
    x_l = x
    x_r = x
    y_l = y+open_amt
    y_r = y-open_amt
    z_l = z
    z_r = z
    
    yaw_l = -pi/2
    yaw_r = pi/2
    pitch_l = 0
    pitch_r = 0
    frame_l = "base_footprint"
    frame_r = "base_footprint"
    grip_l = grip_r = True
    offsetToLeft= 0.0
    if detect:
        #Added
        #StanceUtils.call_stance("look_up",5.0)
        GripUtils.go_to_multi   (x_l=x_l-0.1,y_l=y_l-offsetToLeft,z_l=z_l-0.2,roll_l=pi/2,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r-0.1,y_r=y_r-offsetToLeft,z_r=z_r-0.2,roll_r=pi/2,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2.5)
        avg_hue = get_avg_hue()
        GripUtils.go_to_multi   (x_l=x_l-0.1,y_l=y_l-offsetToLeft,z_l=z_l,roll_l=pi/2,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r-0.1,y_r=y_r-offsetToLeft,z_r=z_r,roll_r=pi/2,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2.5)
    
    if upside_down:
        GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l-offsetToLeft,z_l=z_l,roll_l=0.0,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+0.005,y_r=y_r-offsetToLeft,z_r=z_r,roll_r=pi,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2.5)
        roll_l = -pi/2
        roll_r = 3*pi/2
    else:
        roll_l = pi/2
        roll_r = pi/2
    
    GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l-offsetToLeft,z_l=z_l,roll_l=roll_l+1.0/5,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r+0.015,y_r=y_r-offsetToLeft,z_r=z_r,roll_r=roll_r-1.0/5,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=2.5)
    GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l,z_l=z_l,roll_l=roll_l+1.0/5,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r+0.015,y_r=y_r,z_r=z_r,roll_r=roll_r-1.0/5,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)
    #Note: x_r should be + 0.005
    #z_l -= 0.04
    #z_r -= 0.04
    success = False
    while not success:
        z_l = z - 0.04
        z_r = z - 0.04
        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=3.0)
        
        z_l = z_r = TABLE_HEIGHT + DOWEL_HEIGHT-depth/2.0
        
        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=5.0)
        z_l = z_r = TABLE_HEIGHT + DOWEL_HEIGHT-depth
        #y_l += 0.02
        #y_r -= 0.02
        y_l = y+open_amt+0.02
        y_r = y-open_amt-0.02
    

        success = GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pi/5,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pi/5,grip_r=grip_r,frame_r=frame_r
                                ,dur=5.0)
                                

        if detect:
            #Added check
            if abs(get_avg_hue() - avg_hue) < 3.0:
                x_l += 0.005
                x_r += 0.005
                print "MISSED. Now trying further back"
                success = False

        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l-0.01,z_l=z_l+0.02,roll_l=roll_l,yaw_l=yaw_l,pitch_l=0,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r+0.01,z_r=z_r+0.02,roll_r=roll_r,yaw_r=yaw_r,pitch_r=0,grip_r=grip_r,frame_r=frame_r
                                ,dur=5.0)
        """                        
        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l+0.0,z_l=z_l+0.06,roll_l=roll_l,yaw_l=yaw_l,pitch_l=-pi/5,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r-0.0,z_r=z_r+0.06,roll_r=roll_r,yaw_r=yaw_r,pitch_r=-pi/5,grip_r=grip_r,frame_r=frame_r
                                ,dur=5.0)
        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l-0.01,z_l=z_l+0.02,roll_l=roll_l,yaw_l=yaw_l,pitch_l=0,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r+0.01,z_r=z_r+0.02,roll_r=roll_r,yaw_r=yaw_r,pitch_r=0,grip_r=grip_r,frame_r=frame_r
                                ,dur=5.0)
        """
    StanceUtils.call_stance("open_both",5.0)
    StanceUtils.call_stance("arms_up",5.0)
    #StanceUtils.call_stance("look_down_more",5.0)
    return              
    
def layout_sock(location,width=0.5*DOWEL_HEIGHT,direction="l",arm=None):
    
    if direction == "l":
        drag_yaw = -pi/2
        drag_amount = width*1.1 #FIXME was 1.5
        drag_arm = "l"
    else:
        drag_yaw = pi/2
        drag_amount = width*-1.1 #FIXME was 1.5
        drag_arm = "r"
    if arm:
        drag_arm = arm
    lift_height = abs(drag_amount)
    init_offset = drag_amount * -0.5
    if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,y_offset = 2*init_offset, z_offset = lift_height,dur=3.0):
        return False
    if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,y_offset = 2*init_offset, z_offset = lift_height/1.5,dur=3.0):
        return False
    if not GripUtils.go_to_pt(location,roll=pi/2,yaw=drag_yaw,pitch=pi/4,arm=drag_arm,grip=True,z_offset = 0.01,y_offset=drag_amount+init_offset,dur=5.0):
        return False
    return SUCCESS

def take_off_dowel(arm):
    x = DOWEL_X
    y = DOWEL_Y
    if arm == "l":
        yaw = -pi/2
        y -= 0.005
    else:
        yaw = pi/2
        y += 0.005
    z = DOWEL_HEIGHT+TABLE_HEIGHT - 0.045
    frame = "base_footprint"
    GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,yaw=yaw,pitch=pi/4,arm=arm,grip=False,frame=frame,dur=3.0)
    GripUtils.close_gripper(arm,extra_tight=False)
    GripUtils.go_to(x=x,y=y,z=z+0.1,roll=pi/2,yaw=yaw,pitch=0,arm=arm,grip=True,frame=frame,dur=2.0)
    GripUtils.go_to(x=x,y=y,z=z+0.2,roll=pi/2,yaw=yaw,pitch=0,arm=arm,grip=True,frame=frame,dur=2.0)
    roll = 0
    if arm=="l":
        yaw = -pi/2
    else:
        yaw = pi/2
    GripUtils.go_to(x=x-0.15,y=y,z=z+0.2,roll=roll,yaw=yaw,pitch=0,arm=arm,grip=True,frame=frame,dur=2.0)

    
def test_storage():
    """
    GripUtils.go_to_multi( x_l=0.5,y_l=TABLE_WIDTH/2.0,z_l=TABLE_HEIGHT+0.03,roll_l=pi/2,pitch_l=pi/2,yaw_l=pi/2,grip_l=True,frame_l="base_footprint",
                            x_r=0.5,y_r=-TABLE_WIDTH/2.0,z_r=TABLE_HEIGHT+0.03,roll_r=pi/2,pitch_r=pi/2,yaw_r=pi/2,grip_r=True,frame_r="base_footprint",
                            dur=5.0)
    return
    """
    quit = False
    while not quit:
        print "Store or Retrieve?"
        store = raw_input()[0]=='s'
        print "Which sock would you like to %s?"%("store" if store else "retrieve")
        i = int(raw_input())
        if i < 0:
            quit = True
        else:
            StanceUtils.call_stance("arms_up",5.0)
            if store:
                store_sock(i)
            else:
                retrieve_sock(i)
def test_state():
    while True:
        print "Press enter to capture sock data"
        raw_input()
        get_states()

def test_pickup():
    quit = False
    upside_down = False
    while not quit:
        print "Place sock and press any key"
        raw_input()
        
        #StanceUtils.call_stance("arms_up",5.0)
        #(grasp_pt,angle) = get_grip_point_click("l")
        """ Begin Auto Detection
        state = get_states()[0]
        grasp_pt = state.grasp_point
        angle = state.grasp_angle
        upside_down = not state.inside_out
        End Auto Detection """
        #pickup_sock(THIN_SOCK,grasp_pt,angle)
        #open_sock()
        
        go_down_dowel(depth=DOWEL_HEIGHT*0.7,upside_down=upside_down)
        take_off_dowel(arm="r")
        
def position_dowel():
    detect = False
    open_amt = 0.025
    x = DOWEL_X
    y = DOWEL_Y
    z = DOWEL_HEIGHT+TABLE_HEIGHT
    x_l = x
    x_r = x
    y_l = y+open_amt
    y_r = y-open_amt
    z_l = z
    z_r = z
    
    yaw_l = -pi/2
    yaw_r = pi/2
    pitch_l = 0
    pitch_r = 0
    frame_l = "base_footprint"
    frame_r = "base_footprint"
    grip_l = grip_r = True
    offsetToLeft= 0.0
    
    roll_l = pi/2
    roll_r = pi/2
    
    GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l-offsetToLeft,z_l=z_l,roll_l=roll_l+1.0/5,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r+0.015,y_r=y_r-offsetToLeft,z_r=z_r,roll_r=roll_r-1.0/5,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=2.5)
    GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l,z_l=z_l,roll_l=roll_l+1.0/5,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r+0.015,y_r=y_r,z_r=z_r,roll_r=roll_r-1.0/5,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)
    print "Press any key to continue"
    raw_input()
    return

def test_smooth():
    sm = StateMachine(DEFAULT_OUTCOMES)

    sm.userdata.location = TEST_LAYOUT_PT
    sm.userdata.distance = 0.2

    with sm:
        StateMachine.add('Smooth_Sock',Smooth("b"),{SUCCESS:SUCCESS,FAILURE:FAILURE})
    sm.execute()
    return       
                            
def main(args):
    rospy.init_node("sock_demo_node")
    #configure_prosilica()
    #test_storage()
    #test_state()
    #run_demo()
    test_pickup()
    #position_dowel()
    return
    (left_sock_state,right_sock_state) = get_states()
    
    grip_point = left_sock_state.grasp_point
    angle = left_sock_state.grip_angle
    left_inside_out = left_sock_state.inside_out
    right_inside_out = right_sock_state.inside_out
    left_thick = left_sock_state.thick
    right_thick = right_sock_state.thick
    """
    (left_inside_out,right_inside_out) = is_inside_out()
    (left_thick,right_thick) = is_thick()
    (grip_point,angle) = get_grip_point("l")
    """
    print "Is the left inside out? %s. Is the right inside out? %s"%(left_inside_out,right_inside_out) 
    print "Is the left thick? %s. Is the right thick? %s"%(left_thick,right_thick)
    print "Computed a grip_point of (%f,%f,%f)"%(grip_point.point.x,grip_point.point.y,grip_point.point.z)
    return 
    sm = StateMachine(DEFAULT_OUTCOMES)
    with sm:
        #ClumpToSmooth().add_states('ClumpToSmooth',{SUCCESS:SUCCESS,FAILURE:FAILURE})
        #StateMachine.add('ClumpToSmooth', ClumpToSmooth(), transitions={SUCCESS:SUCCESS, FAILURE:FAILURE})
        StateMachine.add('FixSock',FixSock(), transitions={SUCCESS:SUCCESS, FAILURE:FAILURE})
    

    #sis = smach_ros.IntrospectionServer('demo_smach_server', sm, '/SM_ROOT')
    #sis.start()
    outcome = sm.execute()
    return
    """   
    (left_inside_out,right_inside_out) = get_sock_states()
    if left_inside_out:
        pt = pickup_sock("l")
        open_sock()
        flip_sock(pt,"l")
    StanceUtils.call_stance("arms_up",5.0)
    if right_inside_out:
        rpt = pickup_sock("r")
        open_sock()
        flip_sock(rpt,"r")
    StanceUtils.call_stance("arms_up",5.0)
    pair_socks()
    """
if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
