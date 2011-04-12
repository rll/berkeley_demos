#!/usr/bin/env python
import roslib
roslib.load_manifest("unfolding_smach")
import rospy
import StanceUtils
import PrimitiveUtils
from pr2_simple_arm_motions import GripUtils
from image_processor.srv import *
from geometry_msgs.msg import PointStamped
import sys
from numpy import pi


def main(args):
    rospy.init_node("unfolding_click")

    StanceUtils.call_stance("look_down",3.0)
    StanceUtils.call_stance("arms_up",3.0)
    while True and not rospy.is_shutdown():
        process_mono = rospy.ServiceProxy("click_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        z_offset = 0.06
        link_frame = "r_wrist_roll_link"
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="r",z_offset=z_offset,grip=True,dur=5.0,link_frame=link_frame)
        z_offset = 0.00
        GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="r",z_offset=z_offset,grip=True,dur=5.0,link_frame=link_frame)
        rospy.sleep(5.0)

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
