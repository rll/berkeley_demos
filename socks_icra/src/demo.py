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

TABLE_HEIGHT = 0.872
DOPPLE_X = 0.705
DOPPLE_Y = 0
DOPPLE_HEIGHT = 0.40

THICK_SOCK_INCREMENT = pi/15
THIN_SOCK_INCREMENT = pi/15
(THIN_SOCK,THICK_SOCK) = range(2)
MODE = THICK_SOCK
if MODE == THIN_SOCK:
    ANGLE_INCREMENT = THIN_SOCK_INCREMENT
else:
    ANGLE_INCREMENT = THICK_SOCK_INCREMENT

sock_pos = None

def failure():
    sys.exit("Hit a failure I couldn't recover from.")

def get_sock_states():
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

def get_grip_point(sock):
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    print "Give me the grip point"
    process_mono = rospy.ServiceProxy("click_point_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    resp.param_names = ("l","r")
    resp.params = (0.0,0.0)
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

def pickup_sock(sock):
    z_off = 0.0
    """
    while not rospy.is_shutdown():
        StanceUtils.call_stance("close_right",5.0)
        (grip_pt,angle) = get_grip_point(sock)
        GripUtils.go_to_pt(grip_pt,roll=pi/2,yaw=pi/2-angle,pitch=pi/2,arm="r",grip=True,z_offset=z_off)
        rospy.sleep(5.0)
        z_off = float(raw_input("What is the new z_offset?"))
        StanceUtils.call_stance("arms_up",5.0)
    """
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
        y_offset += 0.02
        GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
    while not GripUtils.has_object("r"):
        StanceUtils.call_stance("open_right",2.0)
        pitch -= ANGLE_INCREMENT
        y_offset -= 0.005*cos(angle)
        x_offset -= 0.005*sin(angle)
        z_offset += 0.0015
        GripUtils.go_to_pt(grip_pt,roll=roll,yaw=yaw,pitch=pitch,arm="r",x_offset=x_offset,y_offset=y_offset,z_offset=z_offset,grip=False,dur=5.0)
        GripUtils.close_gripper("r",extra_tight=True)
        break
    return grip_pt
    
def pickup_clump(arm):
    init_pt = initial_pickup("r")
    GripUtils.go_to_pt(init_pt,roll=pi/2,yaw=0,pitch=pi/2,arm="r",grip=True,z_offset = 0.08,dur=3.0)
    GripUtils.go_to_pt(init_pt,roll=pi/2,yaw=0,pitch=pi/2,arm="r",grip=True,z_offset = 0.01,y_offset=0.1,dur=3.0)
    GripUtils.go_to_pt(init_pt,roll=pi/2,yaw=0,pitch=pi/2,arm="r",grip=True,z_offset = 0.01,y_offset=-0.1,dur=3.0)
    StanceUtils.call_stance("arms_up",5.0)
    seam_pt = grab_far_left("l")
    GripUtils.go_to_pt(seam_pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",grip=True,z_offset = 0.08,dur=3.0)
    GripUtils.go_to_pt(seam_pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",grip=True,z_offset = 0.01,y_offset=+0.1,dur=3.0)
    GripUtils.go_to_pt(seam_pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",grip=True,z_offset = 0.01,y_offset=-0.1,dur=3.0)
    StanceUtils.call_stance("arms_up",5.0)
    
#Initial pickup of clump
def initial_pickup(arm):
    success = True
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
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
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    process_mono = rospy.ServiceProxy("far_right_finder_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    GripUtils.grab_point(pt,roll=-pi/2,yaw=pi/2,arm=arm,z_offset = 0.02,x_offset = -0.01)
    return pt

#Grab the far left point
def grab_far_left(arm):
    StanceUtils.call_stance("look_down",5.0)
    rospy.sleep(2.5)
    process_mono = rospy.ServiceProxy("far_left_finder_node/process_mono",ProcessMono)
    resp = process_mono("wide_stereo/left")
    pt = resp.pts3d[0]
    pt_opp = resp.pts3d[1]
    GripUtils.grab_point(pt,roll=-pi/2,yaw=-pi/2,arm=arm,z_offset = 0.02,x_offset = -0.01)
    return pt

def open_sock():
    x=0.5
    y=0.0
    z=TABLE_HEIGHT+0.4
    frame="base_footprint"
    #old strategy
    GripUtils.go_to(x=x,y=y+0.007,z=z,roll=pi/2,yaw=pi/2,pitch=-pi/8,grip=True,frame=frame,arm="r",dur=5.0)
    GripUtils.go_to(x=x,y=y+0.05,z=z,roll=pi/2,yaw=-pi/2,pitch=0,grip=False,frame=frame,arm="l",dur=5.0)
    GripUtils.go_to(x=x,y=y-0.004,z=z+0.01,roll=pi/2,yaw=-pi/2,pitch=pi/5,grip=False,frame=frame,arm="l",dur=5.0)
    GripUtils.go_to(x=x,y=y-0.0035,z=z+0.001,roll=pi/2,yaw=-pi/2,pitch=pi/5,grip=True,frame=frame,arm="l",dur=2.0) #changed from -0.007 to -0.0065
    
    #GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,yaw=pi/2,pitch=0,grip=True,frame=frame,arm="r",dur=5.0)
    #GripUtils.go_to(x=x,y=y+0.04,z=z+0.05,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=False,frame=frame,arm="l",dur=5.0)    
    #GripUtils.go_to(x=x,y=y+0.04,z=z+0.005,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=False,frame=frame,arm="l",dur=5.0)
    #GripUtils.go_to(x=x,y=y,z=z,roll=pi/2,yaw=pi/2,pitch=-pi/16,grip=True,frame=frame,arm="r",dur=5.0)
    #GripUtils.go_to(x=x,y=y+0.06,z=z-0.025,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=False,frame=frame,arm="l",dur=5.0)
    #GripUtils.go_to(x=x,y=y+0.025,z=z-0.225,roll=pi/2,yaw=-pi/2,pitch=pi/2,grip=True,frame=frame,arm="l",dur=1.0)
    #GripUtils.go_to(x=x,y=y+0.025,z=z,roll=pi/2,yaw=-pi/2,pitch=0,grip=True,frame=frame,arm="l",dur=5.0)
    
    
    GripUtils.close_gripper("l",extra_tight=True)
    open_amt = 0.025
    GripUtils.go_to_multi   (x_l=x,y_l=y+open_amt,z_l=z+0.01,roll_l=pi/2,yaw_l=-pi/2,pitch_l=0,grip_l=True,frame_l=frame
                            ,x_r=x,y_r=y-open_amt,z_r=z+0.01,roll_r=pi/2,yaw_r=pi/2,pitch_r=0,grip_r=True,frame_r=frame
                            ,dur=5.0)
                            
def flip_sock(pt,arm):
    wiggle_down_dopple()
    StanceUtils.call_stance("arms_up",5.0)
    take_off_dopple(pt,arm=arm)
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
    
def wiggle_down_dopple(back_up = True):
    open_amt = 0.02 #original 0.025
    x = DOPPLE_X
    y = DOPPLE_Y
    z = DOPPLE_HEIGHT+TABLE_HEIGHT
    x_l = x
    x_r = x
    y_l = y+open_amt
    y_r = y-open_amt
    z_l = z
    z_r = z
    roll_l = pi/2
    roll_r = pi/2
    yaw_l = -pi/2
    yaw_r = pi/2
    pitch_l = 0
    pitch_r = 0
    frame_l = "base_footprint"
    frame_r = "base_footprint"
    grip_l = grip_r = True
    offsetToLeft= 0.01
    GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l-offsetToLeft,z_l=z_l,roll_l=roll_l+1.0/5,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r+0.005,y_r=y_r-offsetToLeft,z_r=z_r,roll_r=roll_r-1.0/5,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)
    GripUtils.go_to_multi   (x_l=x_l+0.005,y_l=y_l,z_l=z_l,roll_l=roll_l+1.0/5,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r+0.005,y_r=y_r,z_r=z_r,roll_r=roll_r-1.0/5,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)                            
    z_l -= 0.04
    z_r -= 0.04
    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=2.0)
    x_step = 0.015
    #z_step = 0.0175
    z_step = 0.02
    #max_iters = (DOPPLE_HEIGHT - 0.15) / z_step * 2
    max_iters = 27;
    new_z_l = z_l
    new_z_r = z_r
    print "Going for %d wiggle iterations"%max_iters
    
    
    
    for i in range(3):
        new_z_l -= 2.0*z_step;
        new_z_r -= 2.0*z_step;
        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=1)
        new_z_l += 1*z_step;
        new_z_r += 1*z_step;
        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=1)
    
    xWiggleList = [0, 0.02, 0, -0.02]
    yWiggleList = [0.02, 0, -0.02, 0]
    new_z_l += 2.5*z_step;
    new_z_r += 2.5*z_step;
    for i in range(max_iters):
        currentXoffset= xWiggleList[i%4];
        currentYoffset= yWiggleList[i%4];
        
        new_z_l -= 5.0*z_step;
        new_z_r -= 5.0*z_step;

        GripUtils.go_to_multi   (x_l=x_l + currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r + currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2)
                                
        new_z_l += 5.0*z_step;
        new_z_r += 5.0*z_step;

        GripUtils.go_to_multi   (x_l=x_l + currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r + currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2)       
                                
        new_z_l -= 5.0*z_step;
        new_z_r -= 5.0*z_step;

        GripUtils.go_to_multi   (x_l=x_l + currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r + currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2)                                                         
                                
        new_z_l += 4.75*z_step;
        new_z_r += 4.75*z_step;
        GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=2)

    new_z_l = TABLE_HEIGHT + 0.2
    new_z_r = TABLE_HEIGHT + 0.2
        
    GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=3)

    new_z_l = TABLE_HEIGHT + 0.3
    new_z_r = TABLE_HEIGHT + 0.3
        
    GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=3)
                                
    #new_z_l = TABLE_HEIGHT + 0.05
    #new_z_r = TABLE_HEIGHT + 0.05
    #    
    #GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
    #                            ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
    #                            ,dur=5)  
                                
    new_z_l = TABLE_HEIGHT + 0.1
    new_z_r = TABLE_HEIGHT + 0.1
        
    GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=3)                                                              

    new_z_l = TABLE_HEIGHT + 0.2
    new_z_r = TABLE_HEIGHT + 0.2
        
    GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=3)

    new_z_l = TABLE_HEIGHT + 0.05
    new_z_r = TABLE_HEIGHT + 0.05
        
    GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                                ,dur=3)    

    new_z_l = TABLE_HEIGHT + 0.15
    new_z_r = TABLE_HEIGHT + 0.15
        
    GripUtils.go_to_multi   (x_l=x_l+currentXoffset,y_l=y_l+currentYoffset,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l-pi/8,grip_l=grip_l,frame_l=frame_l
                                ,x_r=x_r+currentXoffset,y_r=y_r+currentYoffset,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r-pi/8,grip_r=grip_r,frame_r=frame_r
                                ,dur=3)

    #amplitude= 2.0
    #new_z_l -= 0.5*amplitude*z_step;
    #new_z_r += 0.5*amplitude*z_step;
    # new wiggle algorithm
    #for i in range(max_iters):
    #    if (i>3):
    #        new_z_l += 0.5*amplitude*z_step;
    #        new_z_r -= 0.5*amplitude*z_step;
    #        amplitude= 5.0
    #        new_z_l -= 0.5*amplitude*z_step;
    #        new_z_r += 0.5*amplitude*z_step;
    #    new_z_l += amplitude*z_step
    #    new_z_r -= amplitude*z_step
    #    new_z_l -= 0.25*z_step
    #    new_z_r -= 0.25*z_step
    #    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
    #                            ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
    #                            ,dur=2)
    #
    #    new_z_l -= amplitude*z_step
    #    new_z_r += amplitude*z_step
    #    new_z_l -= 0.25*z_step
    #    new_z_r -= 0.25*z_step        
    #    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
    #                            ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
    #                            ,dur=2)    
    
    
    
#    for i in range(max_iters):
#        roll_l = roll_r = pi/2
#        new_z_l -= z_step
#        new_z_r -= z_step
#        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
#                            ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
#                            ,dur=0.75*(i/3 + 1))
#        
#        x_l += x_step
#        x_r -= x_step
#        roll_l = 2*pi/5
#        roll_r = 3 *pi/5
#        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
#                            ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
#                            ,dur=0.75)
#        x_l -= 2*x_step
#        x_r += 2*x_step
#        GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
#                            ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
#                            ,dur=0.75)
#        roll_l = roll_r = pi/2
#        x_l += x_step
#        x_r -= x_step
#        if back_up:
#            GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
#                            ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
#                            ,dur=0.75*(i/3 + 1))
#
#    #End down
#    new_z_l -= z_step
#    new_z_r -= z_step
#    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=new_z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
#                            ,x_r=x_r,y_r=y_r,z_r=new_z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
#                            ,dur=5.0)

    GripUtils.open_gripper("b")
    

def take_off_dopple(pt,arm):
    x = DOPPLE_X
    y = DOPPLE_Y
    if arm == "l":
        yaw = -pi/2
        y -= 0.005
    else:
        yaw = pi/2
        y += 0.005
    z = DOPPLE_HEIGHT+TABLE_HEIGHT - 0.045
    frame = "base_footprint"
    GripUtils.go_to(x=x,y=y,z=z,roll=0,yaw=yaw,pitch=pi/4,arm=arm,grip=False,frame=frame,dur=5.0)
    GripUtils.close_gripper(arm,extra_tight=False)
    GripUtils.go_to(x=x,y=y,z=z+0.1,roll=0,yaw=yaw,pitch=0,arm=arm,grip=True,frame=frame,dur=5.0)
    GripUtils.go_to(x=x,y=y,z=z+0.2,roll=0,yaw=yaw,pitch=0,arm=arm,grip=True,frame=frame,dur=5.0)
    roll = 0
    if arm=="l":
        yaw = -pi/2
    else:
        yaw = pi/2
    GripUtils.go_to(x=x-0.15,y=y,z=z+0.2,roll=roll,yaw=yaw,pitch=0,arm=arm,grip=True,frame=frame,dur=5.0)
    #Spreads out
    GripUtils.go_to_pt(pt,roll=roll,yaw=yaw,pitch=0,arm=arm,grip=True,z_offset = 0.2,y_offset=0.2,dur=5.0) # previously z_o= 0.08 y_o 0.1
    GripUtils.go_to_pt(pt,roll=roll,yaw=yaw,pitch=pi/2,arm=arm,grip=True,dur=7.5,y_offset = -0.2,z_offset=0.015)
    GripUtils.open_gripper(arm)
    GripUtils.go_to_pt(pt,roll=roll,yaw=yaw,pitch=pi/4,arm=arm,grip=False,dur=2.5,y_offset = -0.2,z_offset=0.025)
    StanceUtils.call_stance("arms_up",5.0)
    
def pair_socks():
    
    pickup_sock("l")
    open_sock()
    put_on_dopple(depth=0.28)
    StanceUtils.call_stance("arms_up",5.0)
    pickup_sock("l") #Node: we do "l" because this is now the only sock on the table. It is now the "left" one.
    open_sock()
    
    put_on_dopple(depth=DOPPLE_HEIGHT-0.1)
    #put_on_dopple(depth=0.29)
    StanceUtils.call_stance("arms_up",5.0)
    take_off_dopple_pair()
    return
    
def put_on_dopple(depth=0.28):
    open_amt = 0.02
    x = DOPPLE_X+0.0075
    y = DOPPLE_Y
    z = DOPPLE_HEIGHT+TABLE_HEIGHT
    x_l = x
    x_r = x
    y_l = y+open_amt
    y_r = y-open_amt
    z_l = z
    z_r = z
    roll_l = -pi/2
    roll_r = -pi/2
    yaw_l = -pi/2
    yaw_r = pi/2
    pitch_l = 0
    pitch_r = 0
    frame_l = "base_footprint"
    frame_r = "base_footprint"
    grip_l = grip_r = True
    GripUtils.go_to_multi   (x_l=x_l-0.1,y_l=y_l,z_l=z_l,roll_l=roll_l+pi/2,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r-0.1,y_r=y_r,z_r=z_r,roll_r=roll_r-pi/2,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)
    GripUtils.go_to_multi   (x_l=x_l-0.05,y_l=y_l,z_l=z_l,roll_l=roll_l+pi/4,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r-0.05,y_r=y_r,z_r=z_r,roll_r=roll_r-pi/4,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)
    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)
    z_l -= 0.04
    z_r -= 0.04
    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=2.0)
    z_l = z_r = TABLE_HEIGHT + DOPPLE_HEIGHT-depth
    
    GripUtils.go_to_multi   (x_l=x_l,y_l=y_l,z_l=z_l,roll_l=roll_l,yaw_l=yaw_l,pitch_l=pitch_l,grip_l=grip_l,frame_l=frame_l
                            ,x_r=x_r,y_r=y_r,z_r=z_r,roll_r=roll_r,yaw_r=yaw_r,pitch_r=pitch_r,grip_r=grip_r,frame_r=frame_r
                            ,dur=5.0)

def take_off_dopple_pair():
    x = DOPPLE_X
    y = DOPPLE_Y
    yaw = pi/2
    y += 0.005
    z = DOPPLE_HEIGHT+TABLE_HEIGHT - 0.045
    frame = "base_footprint"
    GripUtils.go_to(x=x,y=y,z=z,roll=0,yaw=yaw,pitch=pi/4,arm="r",grip=False,frame=frame,dur=5.0)
    GripUtils.close_gripper("r",extra_tight=False)
    GripUtils.go_to(x=x,y=y,z=z+0.1,roll=pi/2,yaw=yaw,pitch=0,arm="r",grip=True,frame=frame,dur=5.0)
    GripUtils.go_to(x=x,y=y,z=z+0.2,roll=pi/2,yaw=yaw,pitch=0,arm="r",grip=True,frame=frame,dur=5.0)
    GripUtils.go_to(x=x-0.2,y=y,z=z+0.2,roll=pi/2,yaw=yaw,pitch=0,arm="r",grip=True,frame=frame,dur=5.0)

                            
def main(args):
    print "Running demo"
    rospy.init_node("sock_demo_node")
    PrimitiveUtils.call_primitive("init")
    pt = pickup_clump("r")
    pt = pickup_sock("l")
    open_sock()
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
