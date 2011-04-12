#!/usr/bin/env python
import roslib
roslib.load_manifest("dryer_demo")
import rospy
import StanceUtils
import PrimitiveUtils
import GripUtils
import DryerNavigationUtils
from image_processor.srv import ProcessStereo
from geometry_msgs.msg import PointStamped
from numpy import *
import sys
from smach.state import State
from smach.state_machine import StateMachine
#import smach_ros
from SmachUtils import *
import dryer_move
from cloth_manipulator import ClothTracker
from cloth_state_estimation.srv import KillMe
import RosUtils
import tf
import cloth_motions
import cloth_manipulator
from pr2_simple_motions_srvs.srv import MoveTorso

_cloth_tracker = None
_listener = None

TABLE_WIDTH = 0.98
PANTS_LENGTH = 0.49

def go_to_dryer():
    print "Going to dryer"
    DryerNavigationUtils.initToDryer()
    return True

def open_dryer():
    print "Opening dryer"
    dryer_move.openDoor()
    dryer_move.swingDoorOpen()
    return True

def find_cloth():
    return PointStamped()# if input_string[0]=='y' else False

def take_out_cloth():
    print "Taking out cloth"
    RosUtils.call_service("move_torso",MoveTorso,height=0.01)
    DryerNavigationUtils.goToPosition("enter_dryer")
    GripUtils.go_to(x=-0.1,y=-0.33,z=-0.4,roll=0,pitch=0,yaw=0,grip=False,arm="l",frame="dryer")
    DryerNavigationUtils.goToPosition("into_dryer")
    GripUtils.go_to(x=0.15,y=-0.33,z=-0.65,roll=0,pitch=pi/2,yaw=0,grip=False,arm="l",frame="dryer")
    GripUtils.close_gripper("l")
    GripUtils.go_to(x=0.15,y=-0.33,z=-0.4,roll=0,pitch=0,yaw=0,grip=True,arm="l",frame="dryer")
    DryerNavigationUtils.goToPosition("enter_dryer")
    RosUtils.call_service("move_torso",MoveTorso,height=0.3)
    return True

def go_to_folding_station():
    print "Going to folding station"
    DryerNavigationUtils.dryerToTable1()
    GripUtils.go_to(arm="l",x=0.5,y=0,z=0.35,roll=0,yaw=0,pitch=pi/2,grip=True,frame="table_height")
    GripUtils.open_gripper("l")
    return True

def unfold_cloth():
    print "Unfolding cloth"
    #Run cloth tracker
    success = _cloth_tracker.run()
    #(waist_l,waist_r) = get_waist_points()
    #fold_cloth()
    #Kill the cloth tracker cpp node so it will relaunch
    RosUtils.call_service('cloth_tracker/kill',KillMe)
    return success

def get_waist_points():
    """
    resp = RosUtils.call_service('find_waist_node/process_stereo',ProcessStereo,"wide_stereo")
    l_point = resp.pts3d[0]
    resp = RosUtils.call_service('find_waist_node/process_stereo',ProcessStereo,"wide_stereo")
    r_point = resp.pts3d[0]
    return (l_point,r_point)
    """
    return (_cloth_tracker.l_grasp_pt,_cloth_tracker.r_grasp_pt)

def fold_cloth(dir='l'):
    print "Folding cloth"
    _cloth_tracker.scoot(-0.1)
    GripUtils.recall_arm("b")
    (waist_l_base,waist_r_base) = get_waist_points()
    now = rospy.Time.now()
    waist_l_base.header.stamp = now
    waist_r_base.header.stamp = now
    _listener.waitForTransform("table_height",waist_l_base.header.frame_id,now,rospy.Duration(5.0))
    waist_l = _listener.transformPoint("table_height",waist_l_base)
    waist_r= _listener.transformPoint("table_height",waist_r_base)
    waist_l.point.z = 0
    waist_r.point.z = 0
    #Grab the waist point
    smooth()
    GripUtils.grab_point(waist_l,arm="l",yaw=-pi/2,x_offset=0.02)
    #Fold over
    ctr_x = (waist_l.point.x + waist_r.point.x)/2+0.02
    ctr_y = (waist_l.point.y + waist_r.point.y)/2
    ctr_z = waist_l.point.y - ctr_y

    GripUtils.go_to(    x=ctr_x,    y=ctr_y,    z=ctr_z,
                        roll=pi/2,  pitch=pi/2, yaw=-pi/2,
                        arm="l",    grip=True,  frame=waist_l.header.frame_id)

    GripUtils.go_to_pt(waist_r,arm="l",roll=pi/2,pitch=3*pi/4,yaw=-pi/2,grip=True,y_offset=0.01,x_offset=0.02)
    GripUtils.go_to_pt(waist_r,arm="l",roll=pi/2,pitch=3*pi/4,yaw=-pi/2,grip=False,y_offset=-0.05,x_offset=0.02,dur=2.5)
    GripUtils.go_to_pt(waist_r,arm="l",roll=pi/2,pitch=3*pi/4,yaw=-pi/2,grip=False,y_offset=-0.05,x_offset=0.02,z_offset=0.05,dur=2.5)
    GripUtils.recall_arm("b")

    #Grab waist
    scoot_amt = 0.2
    _cloth_tracker.scoot(-scoot_amt)
    ctr_x = 0.25 * waist_l.point.x + 0.75 * waist_r.point.x + scoot_amt
    ctr_y = 0.25 * waist_l.point.y + 0.75 * waist_r.point.y
    ctr_z = waist_l.point.z
    GripUtils.grab(     x=ctr_x,    y=ctr_y,    z=ctr_z,
                        roll=pi/2,  pitch=pi/4, yaw=0,
                        arm="r",    frame=waist_l.header.frame_id)
    
    sweep_drag_amount = 0.95*TABLE_WIDTH
    sweep_lift_amount = 0.6
    (x,y,z,r,p,yw) = sweep_cloth_with_scoot("r", sweep_drag_amount, TABLE_WIDTH, sweep_lift_amount,roll=pi/2)
    print "y is %f"%y
    print "(%f,%f,%f,%f,%f,%f)"%(x,y,z,r,p,y)
    smooth("l")
    GripUtils.go_to(    x=x,    y=y+PANTS_LENGTH/4-0.03,    z=PANTS_LENGTH/4,
                        roll=r,  pitch=3*pi/8, yaw=yw,
                        arm="r",    grip=True,  frame="table_height", dur=2.5)
    GripUtils.go_to(    x=x,    y=y+PANTS_LENGTH/2-0.03,    z=PANTS_LENGTH/2,
                        roll=r,  pitch=pi/2, yaw=yw,
                        arm="r",    grip=True,  frame="table_height", dur=2.5)
    GripUtils.go_to(    x=x,    y=y+3*PANTS_LENGTH/4-0.03,    z=PANTS_LENGTH/4,
                        roll=r,  pitch=5*pi/8, yaw=yw,
                        arm="r",    grip=True,  frame="table_height", dur=2.5)
    GripUtils.go_to(    x=x,    y=y+PANTS_LENGTH-0.03,    z=0.01,
                        roll=r,  pitch=pi-p, yaw=yw,
                        arm="r",    grip=True,  frame="table_height", dur=2.5)
    GripUtils.go_to(    x=x,    y=y+PANTS_LENGTH+0.05,    z=0.01,
                        roll=r,  pitch=pi-p, yaw=yw,
                        arm="r",    grip=False,  frame="table_height", dur=2.5)
    GripUtils.go_to(    x=x,    y=y+PANTS_LENGTH+0.05,    z=0.1,
                        roll=r,  pitch=pi-p, yaw=yw,
                        arm="r",    grip=False,  frame="table_height", dur=2.5)
    
    GripUtils.recall_arm("r")
    smooth()
    _cloth_tracker.scoot(scoot_amt+0.08)
    return True

def sweep_cloth_with_scoot(direction, drag_amount, table_width, lift_amount,roll=0,scoot=0):

    forward_amount = 0.5
    hover_amount = 0.06

    edge_distance = (table_width/2.0)+.04
    edge_distance_low = (table_width/2.0)

    if direction == "r":
        drag_arm = "r"
        edge_y_high = edge_distance
        edge_y_low  = edge_distance_low
        drag_yaw = pi/2
        waypoint_y = edge_y_low - (drag_amount/2.0)
        final_y = edge_y_low - drag_amount
    else:
        drag_arm = "l"
        edge_y_high = -1 * edge_distance
        edge_y_low  = -1 * edge_distance_low
        drag_yaw = -pi/2
        waypoint_y = edge_y_low + (drag_amount/2.0)
        final_y = edge_y_low + drag_amount
    
    # Take it to table edge and hold it high

    if not GripUtils.go_to(x=forward_amount-.21,y=edge_y_high,z=lift_amount+0.01,
            roll=roll,pitch=0,yaw=drag_yaw,grip=True,
            frame="table_height",arm=drag_arm,dur=3):
        return False
    
    for i in range(2):
        GripUtils.go_to(x=forward_amount-.21,y=edge_y_high-.02,z=lift_amount-.2,
                roll=roll,pitch=0,yaw=drag_yaw,grip=True,
                frame="table_height",arm=drag_arm,dur=1.0/(0.7*i+1))

        # Lower it at table edge

        if not GripUtils.go_to(x=forward_amount,y=edge_y_low,z=hover_amount,
                roll=roll,pitch=pi/4,yaw=drag_yaw,grip=True,
                frame="table_height",arm=drag_arm,dur=1):
            return False

    # Sweep it back halfway

    if not GripUtils.go_to(x=forward_amount,y=waypoint_y,z=hover_amount,
            roll=roll,pitch=pi/4,yaw=drag_yaw,grip=True,
            frame="table_height",arm=drag_arm,dur=2.5):
        return False

    # Sweep it back the rest of the way
    if not GripUtils.go_to(x=forward_amount,y=final_y,z=hover_amount,
            roll=roll,pitch=pi/4,yaw=drag_yaw,grip=True,
            frame="table_height",arm=drag_arm,dur=2.5):
        return False
    print "Final_y is: %f"%final_y
    return (forward_amount,final_y,hover_amount,
            roll,pi/4,drag_yaw)


def smooth(arm='b'):
    location = PointStamped()
    location.point.x = 0.5
    location.header.frame_id = "table_height"
    distance = TABLE_WIDTH/3
    initial_separation = 0.11
    GripUtils.recall_arm(arm)
    if arm == 'b':
        #Put arms together, with a gap of initial_separation between grippers
        if not GripUtils.go_to_pts(point_l=location,grip_r=True, grip_l=True, point_r=location,
                roll_l=pi/2,yaw_l=0,pitch_l=-pi/2,y_offset_l=initial_separation/2.0,z_offset_l=0.05
                ,link_frame_l="l_wrist_back_frame",
                roll_r=pi/2,yaw_r=0,pitch_r=-pi/2,y_offset_r=-1*initial_separation/2.0,z_offset_r=0.05
                ,link_frame_r="r_wrist_back_frame",dur=4.0):
            success = False
        if not GripUtils.go_to_pts(point_l=location,grip_r=True, grip_l=True, point_r=location,
                roll_l=pi/2,yaw_l=0,pitch_l=-pi/2,y_offset_l=initial_separation/2.0,z_offset_l=-0.03, 
                link_frame_l="l_wrist_back_frame",
                roll_r=pi/2,yaw_r=0,pitch_r=-pi/2,y_offset_r=-1*initial_separation/2.0,z_offset_r=-0.03, 
                link_frame_r="r_wrist_back_frame",dur=2.0):
            success = False
        if not GripUtils.go_to_pts(point_l=location,grip_r=True, grip_l=True, point_r=location,
                roll_l=pi/2,yaw_l=0,pitch_l=-pi/2,
                y_offset_l=(distance+initial_separation)/2.0, z_offset_l=-0.03,
                link_frame_l="l_wrist_back_frame",
                roll_r=pi/2,yaw_r=0,pitch_r=-pi/2,
                y_offset_r=-1*(distance+initial_separation)/2.0, z_offset_r=-0.03,
                link_frame_r="r_wrist_back_frame",dur=2.0):
            success = False
    else:
        #Right is negative in the y axis
        if arm=="r":
            y_multiplier = -1
        else:
            y_multiplier = 1
        location.point.y -= y_multiplier*distance/2
        if not GripUtils.go_to_pt(point=location,grip=True,roll=pi/2,yaw=0,pitch=-pi/2,
                z_offset=0.05,arm=arm,
                link_frame="%s_wrist_back_frame"%arm,dur=4.0):
            success = False
        if not GripUtils.go_to_pt(point=location,grip=True,roll=pi/2,yaw=0,pitch=-pi/2,
                z_offset=-0.01,arm=arm,
                link_frame="%s_wrist_back_frame"%arm,dur=2.0):
            success = False
        if not GripUtils.go_to_pt(point=location,grip=True,roll=pi/2,yaw=0,pitch=-pi/2,
                y_offset=y_multiplier*distance,z_offset=-0.01,arm=arm,
                link_frame="%s_wrist_back_frame"%arm,dur=2.0):
            success = False
    GripUtils.recall_arm(arm)
    return True

def go_to_stacking_station():
    print "Going to the stacking station"
    DryerNavigationUtils.table1ToTable2(0.6)
    return True

def stack_cloth():
    print "Stacking cloth"
    return True

def final_state():
    print "Final state"
    return True

class Initialize(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,output_keys=[])
        
    def execute(self,userdata):
        GripUtils.recall_arm('b')
        return SUCCESS

class GoToDryer(SuccessFailureState):

    def execute(self,userdata):
        return SUCCESS if go_to_dryer() else FAILURE


class OpenDryer(SuccessFailureState):

    def execute(self,userdata):
        return SUCCESS if open_dryer() else FAILURE

class FindCloth(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,output_keys=["cloth_location"])

    def execute(self,userdata):
        cloth_location = find_cloth()
        if cloth_location:
            userdata.cloth_location = cloth_location
            return SUCCESS
        else:
            return FAILURE

class TakeOutCloth(SuccessFailureState):
    def __init__(self):
        SuccessFailureState.__init__(self,input_keys=["cloth_location"])

    def execute(self,userdata):
        return SUCCESS if take_out_cloth() else FAILURE

class GoToFoldingStation(SuccessFailureState):
    def execute(self,userdata):
        return SUCCESS if go_to_folding_station() else FAILURE

class UnfoldCloth(SuccessFailureState):
    def execute(self,userdata):

        return SUCCESS if unfold_cloth() else FAILURE

class FoldCloth(SuccessFailureState):
    def execute(self,userdata):
        return SUCCESS if fold_cloth() else FAILURE

class GoToStackingStation(SuccessFailureState):
    def execute(self,userdata):
        return SUCCESS if go_to_stacking_station() else FAILURE

class StackCloth(SuccessFailureState):
    def execute(self,userdata):
        return SUCCESS if stack_cloth() else FAILURE

class FinalState(SuccessFailureState):
    def execute(self,userdata):
        return SUCCESS if final_state() else FAILURE

class GenericUserData:
    def __init__(self):
        pass

def main(args):
    rospy.init_node("dryer_demo_node")
    global _listener
    _listener = tf.TransformListener()
    global _cloth_tracker
    _cloth_tracker = ClothTracker(disable_services=False)
    DryerNavigationUtils.loadLocations()
    sm = OuterStateMachine(DEFAULT_OUTCOMES)

    START_STATE = 'Go_To_Dryer'
    with sm:
         OuterStateMachine.add('Initialize',                Initialize(),           {SUCCESS:START_STATE,FAILURE:FAILURE})
         OuterStateMachine.add('Go_To_Dryer',               GoToDryer(),            {SUCCESS:'Open_Dryer',FAILURE:FAILURE})
         OuterStateMachine.add('Open_Dryer',                OpenDryer(),            {SUCCESS:'Find_Cloth',FAILURE:FAILURE})
         OuterStateMachine.add('Find_Cloth',                FindCloth(),            {SUCCESS:'Take_Out_Cloth',FAILURE:'Final_State'})
         OuterStateMachine.add('Take_Out_Cloth',            TakeOutCloth(),         {SUCCESS:'Go_To_Folding_Station',FAILURE:FAILURE})
         OuterStateMachine.add('Go_To_Folding_Station',     GoToFoldingStation(),   {SUCCESS:'Unfold_Cloth',FAILURE:FAILURE})
         OuterStateMachine.add('Unfold_Cloth',              UnfoldCloth(),          {SUCCESS:'Fold_Cloth',FAILURE:'Unfold_Cloth'})
         OuterStateMachine.add('Fold_Cloth',                FoldCloth(),            {SUCCESS:SUCCESS,FAILURE:FAILURE})
         OuterStateMachine.add('Go_To_Stacking_Station',    GoToStackingStation(),  {SUCCESS:'Stack_Cloth',FAILURE:FAILURE})
         OuterStateMachine.add('Stack_Cloth',               StackCloth(),           {SUCCESS:'Go_To_Dryer',FAILURE:FAILURE})
         OuterStateMachine.add('Final_State',               FinalState(),           {SUCCESS:SUCCESS,FAILURE:FAILURE})
    
    outcome = sm.execute()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
