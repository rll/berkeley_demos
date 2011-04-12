#!/usr/bin/env python
import roslib
roslib.load_manifest("unfolding")
import rospy
import StanceUtils
import PrimitiveUtils
import GripUtils
from image_processor.srv import *
from geometry_msgs.msg import PointStamped
from web_api_srvs.srv import *
from numpy import *
import sys

#Initial params. Note that triangle_length, towel_width, and towel_height will be overridden once it has detected the towel
TABLE_HEIGHT = 0.87 #Was 0.865
STRETCH_FACTOR = 1.00
TOWEL_STRETCH_FACTOR = 0.95
triangle_length = 0.8
towel_width = 0.6
towel_height = 0.2

(TWITTER,CONSOLE) = range(2)
MODE = CONSOLE

#Initial pickup of towel clump
def initial_pickup():
    success = True
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    process_mono = rospy.ServiceProxy("clump_center_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    z_offset = 0.06
    GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
    GripUtils.close_gripper("l")
    while not GripUtils.has_object("l"):
        print "has_object returned False"
        z_offset -= 0.02
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
        GripUtils.close_gripper("l")
    return success
    
#Grab the far right point
def grab_far_right():
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    process_mono = rospy.ServiceProxy("far_right_finder_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    return GripUtils.grab_point(pt,roll=-pi/2,yaw=pi/2,arm="r")

#Grab the far left point
def grab_far_left():
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    process_mono = rospy.ServiceProxy("far_left_finder_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    pt_opp = resp.pts3d[1]
    triangle_length = sqrt( (pt_opp.point.x - pt.point.x)**2 + (pt_opp.point.y - pt.point.y)**2 )
    return GripUtils.grab_point(pt,roll=-pi/2,yaw=-pi/2,arm="l")

# Takes the towel from the flat, double triangle configuration, and grabs the chosen point
def grab_triangle():
    print "grab triangle start"
    success = True
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    process_mono = rospy.ServiceProxy("triangle_fitter_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt_l = resp.pts3d[0]
    pt_r = resp.pts3d[1]
    pt_tl = resp.pts3d[2]
    pt_tr = resp.pts3d[3]
    #Compute approximate widths
    towel_width = sqrt( (pt_l.point.x - pt_tr.point.x)**2 + (pt_l.point.y - pt_tr.point.y)**2 )
    towel_height = sqrt( (pt_l.point.x - pt_tl.point.x)**2 + (pt_l.point.y - pt_tl.point.y)**2 )
    print "grab triangle finish"
    l_or_r = choose_triangle_pt(resp.image_annotated)
    if l_or_r == "l" or l_or_r == "L":
        StanceUtils.call_stance("open_left",1.0)
        StanceUtils.call_stance("left_up",5.0)
        return GripUtils.grab_point(pt_l,roll=-pi/2,yaw=0,pitch=pi/3,arm="l")
    else:
        StanceUtils.call_stance("open_right",1.0)
        StanceUtils.call_stance("right_up",2.0)
        return GripUtils.grab_point(pt_r,roll=pi/2,yaw=0,pitch=pi/3,arm="r")
    

#Choose which half of the triangle to grabh    
def choose_triangle_pt(image_annotated):

    print "Which point should I choose?"
    if MODE==CONSOLE:
        inp = raw_input()
    else:
        ask = rospy.ServiceProxy("status_maker_node/ask_graphic_question",AskGraphicQuestion)
        inp = ask(image=image_annotated,question="Can anyone tell me which half of the cloth is on top? (please start @replies with 'l' or 'r')").answer
    if inp[0] == "l":
        print "Chose left"
        return "l"
    elif inp[0] == "r":
        print "Chose right"
        return "r"
    else:
        print "I don't understand."

#Once you are holding the triangle, spread it out on table    
def spread_out_triangle():
    print "spread out triangle start"
    success = True
    stretch_length = triangle_length*STRETCH_FACTOR
    x_l = x_r = 0.3
    y_l = stretch_length/2.0
    y_r = -1*y_l
    z_l = z_r = 0.15
    roll_l = -pi/2
    roll_r = pi/2
    pitch_l = pitch_r = pi/3
    yaw_l = -pi/2
    yaw_r = pi/2
    grip_l=grip_r=True
    frame_l=frame_r= "torso_lift_link"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7.5)
    for i in range(2):
        success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l-0.07,z_l=z_l-0.15,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                        ,x_r=x_r,y_r=y_r+0.07,z_r=z_r-0.15,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                        ,dur=0.25)

        success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                        ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                        ,dur=0.25)
    z_l=z_r=TABLE_HEIGHT + 0.075
    x_l += 0.1
    x_r += 0.1
    frame_l=frame_r="base_footprint"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=10.0)
           
    x_l += 0.39
    x_r += 0.39
    yaw_l += pi/3
    yaw_r -= pi/3
    z_l=z_r=TABLE_HEIGHT

    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=10.0)
    #StanceUtils.call_stance("open_both",1.0)
    #StanceUtils.call_stance("close_both",1.0)
    print "spread out triangle finish"
    return success
    
#The initial spreading out of the towel
def spread_out_towel_unsmoothed():
    success = True
    stretch_length = towel_width*TOWEL_STRETCH_FACTOR
    x_l = x_r = 0.2
    y_l = stretch_length/2.0
    y_r = -1*y_l
    z_l = z_r = 0.3
    roll_l = 0
    roll_r = 0
    pitch_l = pitch_r = 0
    yaw_l = -pi/2
    yaw_r = pi/2
    grip_l=grip_r=True
    frame_l=frame_r= "torso_lift_link"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7)

    z_l=z_r=TABLE_HEIGHT + towel_height/2.0
    x_l += 0.18
    x_r += 0.18
    pitch_l = pitch_r = pi/4

    frame_l=frame_r="base_footprint"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=4)
    yaw_l += pi/3
    yaw_r -= pi/3          
    x_l += 0.375
    x_r += 0.375

    z_l=z_r=TABLE_HEIGHT

    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7)
    success &= StanceUtils.call_stance("open_both",1.0)
    return success

#Second spreading out of the towel -- tries to keep it more taut    
def spread_out_towel_smoothed():
    success = True
    stretch_length = towel_width*TOWEL_STRETCH_FACTOR
    x_l = x_r = 0.10
    y_l = stretch_length/2.0
    y_r = -1*y_l
    z_l = z_r = 0.52 + TABLE_HEIGHT
    roll_l = 0
    roll_r = 0
    pitch_l = pitch_r = 0
    yaw_l = -pi/2
    yaw_r = pi/2
    grip_l=grip_r=True
    frame_l=frame_r= "base_footprint"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7)
    z_l-= 0.24
    z_r -= 0.24
    x_l += 0.20
    x_r += 0.20
    pitch_l = pitch_r = 0

    frame_l=frame_r="base_footprint"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7)

    x_l += 0.10
    x_r += 0.10
    pitch_l = pitch_r = 0

    frame_l=frame_r="base_footprint"
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=3.5)
    yaw_l += pi/3
    yaw_r -= pi/3          
    x_l += 0.24
    x_r += 0.24
    #yaw_l += pi/3
    #yaw_r -= pi/3
    z_l=z_r=TABLE_HEIGHT+0.025

    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7)
    success &= StanceUtils.call_stance("open_both",1.0)
    return success

#Smooths the towel when it is fully spread out
def smooth_towel():
    success = PrimitiveUtils.call_primitive("smooth_towel")
    return success

#Smooths the towel once it has already been folded (and is halfway closer to the robot)
def smooth_towel_small():
    success = PrimitiveUtils.call_primitive("smooth_towel_small")
    return success

#Takes a wrinkly towel on the table, lays it back down more nicely, and folds it    
def fold_towel():
    success = True
    StanceUtils.call_stance("look_down",5.0)
    StanceUtils.call_stance("arms_up",3.0)
    rospy.sleep(2.0)
    process_mono = rospy.ServiceProxy("towel_fitter_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt_bl = resp.pts3d[0]
    pt_tl = resp.pts3d[1]
    pt_tr = resp.pts3d[2]
    pt_br = resp.pts3d[3]
    #Try re-spreading out

    #Update belief about width and height
    towel_width = ( sqrt((pt_bl.point.x-pt_br.point.x)**2 + (pt_bl.point.y-pt_br.point.y)**2) + sqrt((pt_bl.point.x-pt_br.point.x)**2 + (pt_bl.point.y-pt_br.point.y)**2) ) / 2.0
    towel_height = ( sqrt((pt_bl.point.x-pt_tl.point.x)**2 + (pt_bl.point.y-pt_tl.point.y)**2) + sqrt((pt_tr.point.x-pt_br.point.x)**2 + (pt_tr.point.y-pt_br.point.y)**2) ) / 2.0
    success &= GripUtils.grab_point(pt_bl,roll=pi/2,yaw=-pi/2,pitch=pi/4,arm="l",x_offset=0.02)
    success &= GripUtils.grab_point(pt_br,roll=-pi/2,yaw=pi/2,pitch=pi/4,arm="r",x_offset=0.02)
    spread_out_towel_smoothed()
    smooth_towel()

     #Now back to folding
    
    resp = process_mono("wide_stereo/left")
    pt_bl = resp.pts3d[0]
    pt_tl = resp.pts3d[1]
    pt_tr = resp.pts3d[2]
    pt_br = resp.pts3d[3]
    success &= GripUtils.grab_point(pt_tl,roll=-pi/2,yaw=-pi/2,pitch=pi/4,arm="l")
    success &= GripUtils.grab_point(pt_tr,roll=pi/2,yaw= pi/2,pitch=pi/4,arm="r")
    (bl_x,bl_y,bl_z) = (pt_bl.point.x,pt_bl.point.y,pt_bl.point.z)
    (tl_x,tl_y,tl_z) = (pt_tl.point.x,pt_tl.point.y,pt_tl.point.z)
    (br_x,br_y,br_z) = (pt_br.point.x,pt_br.point.y,pt_br.point.z)
    (tr_x,tr_y,tr_z) = (pt_tr.point.x,pt_tr.point.y,pt_tr.point.z)
    x_l = (tl_x+bl_x)/2.0
    y_l = (tl_y+bl_y)/2.0 - 0.05
    z_l = bl_z + sqrt( (bl_x-tl_x)**2 + (bl_y-tl_y)**2 )/2.0
    x_r = (tr_x+br_x)/2.0
    y_r = (tr_y+br_y)/2.0 + 0.05
    z_r = br_z + sqrt( (br_x-tr_x)**2 + (br_y-tr_y)**2 )/2.0
    pitch_l = pitch_r = pi/4
    roll_l = 0
    roll_r = 0
    yaw_l=-pi/2
    yaw_r= pi/2
    grip_l=grip_r=True
    frame_l=frame_r = pt_bl.header.frame_id
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7.5)
    x_l = bl_x
    y_l = bl_y
    z_l = z_r = bl_z
    x_r = br_x
    y_r = br_y
    yaw_l = -3*pi/4
    yaw_r = 3*pi/4
    pitch_l=pitch_r = pi/4
    roll_l = pi/2
    roll_r = -pi/2
    success &= GripUtils.go_to_multi (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,pitch_l=pitch_l,yaw_l=yaw_l,grip_l=grip_l,frame_l=frame_l
                                    ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,pitch_r=pitch_r,yaw_r=yaw_r,grip_r=grip_r,frame_r=frame_r
                                    ,dur=7.5)
    success &= StanceUtils.call_stance("open_both",1.0)
    success &= StanceUtils.call_stance("arms_up",2.5)
    success &= smooth_towel_small()
    ctr_l_x = .75*bl_x + .25*tl_x
    ctr_l_y = .75*bl_y + .25*tl_y
    z = bl_z
    yaw = -pi/2
    roll = -pi/2
    pitch = pi/4
    frame = pt_bl.header.frame_id
    success &= GripUtils.grab(x=ctr_l_x,y=ctr_l_y,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame)
    ctr_r_x = .75*br_x + .25*tr_x
    ctr_r_y = .75*br_y + .25*tr_y
    alpha = 0.333
    ctr_ml_x = (1-alpha)*ctr_l_x + alpha*ctr_r_x
    ctr_ml_y = (1-alpha)*ctr_l_y + alpha*ctr_r_y
    ctr_mr_x = (1-alpha)*ctr_r_x + alpha*ctr_l_x
    ctr_mr_y = (1-alpha)*ctr_r_y + alpha*ctr_l_y
    up_z = z+sqrt( (ctr_l_x - ctr_r_x)**2 + (ctr_l_y - ctr_r_y)**2) / 3.0
    pitch = pi/2
    success &= GripUtils.go_to(x=ctr_ml_x,y=ctr_ml_y,z=up_z,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=True,dur=5.0)
    z = bl_z
    pitch = 3*pi/4
    
    success &= GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y+0.02,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=True,dur=5.0)
    yaw = pi/2
    roll = pi/2
    pitch = pi/4
    success &= StanceUtils.call_stance("open_left",1.0)
    success &= GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y-0.05,z=z+0.02,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=False,dur=1.0)
    success &= StanceUtils.call_stance("left_up",2.5)
    success &= GripUtils.grab(x=ctr_r_x,y=ctr_r_y,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame)
    pitch = pi/2
    success &= GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y-0.02,z=up_z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame,grip=True,dur=5.0)
    z = bl_z+0.01
    pitch = 3*pi/4
    
    success &= GripUtils.go_to(x=ctr_ml_x,y=ctr_ml_y-0.02,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame,grip=True,dur=5.0)
    success &= StanceUtils.call_stance("open_right",1.0)
    success &= GripUtils.go_to(x=ctr_ml_x,y=ctr_ml_y+0.05,z=z+0.02,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame,grip=False,dur=1.0)
    success &= StanceUtils.call_stance("right_up",2.5)
    
    #Pick up
    #success &= GripUtils.grab(x=ctr_ml_x,y=ctr_ml_y,z=z,roll=-pi/2,yaw=-pi/2,pitch=pi/4,arm="l",frame=frame)
    #success &= GripUtils.grab(x=ctr_mr_x,y=ctr_mr_y,z=z,roll=pi/2,yaw=pi/2,pitch=pi/4,arm="r",frame=frame)
    success &= GripUtils.go_to_multi (x_l=ctr_ml_x+0.03,y_l=ctr_ml_y+0.06,z_l=z+0.01,roll_l=-pi/2,pitch_l=pi/4,yaw_l=-pi/2,grip_l=False,frame_l=frame
                                    ,x_r=ctr_mr_x+0.03,y_r=ctr_mr_y-0.03,z_r=z+0.01,roll_r= pi/2,pitch_r=pi/4,yaw_r= pi/2,grip_r=False,frame_r=frame
                                    ,dur=3.0)
    success &= GripUtils.go_to_multi (x_l=ctr_ml_x+0.03,y_l=ctr_ml_y-0.05,z_l=z+0.01,roll_l=-pi/2,pitch_l=pi/4,yaw_l=-pi/2,grip_l=False,frame_l=frame
                                    ,x_r=ctr_mr_x+0.03,y_r=ctr_mr_y+0.05,z_r=z+0.01,roll_r= pi/2,pitch_r=pi/4,yaw_r= pi/2,grip_r=False,frame_r=frame
                                    ,dur=3.0)
    success &= StanceUtils.call_stance("close_both",1.0)
    success &= GripUtils.go_to_multi (x_l=ctr_ml_x+0.03,y_l=ctr_ml_y-0.05,z_l=z+0.1,roll_l=-pi/2,pitch_l=pi/4,yaw_l=-pi/2,grip_l=True,frame_l=frame
                                    ,x_r=ctr_mr_x+0.03,y_r=ctr_mr_y+0.05,z_r=z+0.1,roll_r= pi/2,pitch_r=pi/4,yaw_r= pi/2,grip_r=True,frame_r=frame
                                    ,dur=3.0)
    return success

#Thanks the user who assisted it in folding    
def thank():
    if MODE==TWITTER:
        status = rospy.ServiceProxy("status_maker_node/pull_image",PullImage)
        status(image_topic="wide_stereo/left/image_rect_color",caption="Thanks for the help, everyone. Here's the finished product.")
    else:
        print "Thanks!"

#For future, more closed-loop control. At the moment it isn't set to do anything but crash...
def failure():
    sys.exit("Hit a failure I couldn't recover from.")

def main(args):
    rospy.init_node("unfolding_demo_node")
    success = StanceUtils.call_stance("open_both",3.0)
    success &= StanceUtils.call_stance("arms_up",3.0)
    rospy.sleep(5.0)
    #success &= PrimitiveUtils.call_primitive("initial_pickup")
    success &= initial_pickup()
    success &= PrimitiveUtils.call_primitive("sweep_left")
    success &= PrimitiveUtils.call_primitive("sweep_left_smooth")
    success &= grab_far_right()    
    success &= PrimitiveUtils.call_primitive("sweep_right")
    success &= PrimitiveUtils.call_primitive("sweep_right_smooth")
    success &= grab_far_left()
    success &= spread_out_triangle()
    success &= grab_triangle()
    success &= spread_out_towel_unsmoothed()
    success &= smooth_towel()
    success &= fold_towel()
        
    thank()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
