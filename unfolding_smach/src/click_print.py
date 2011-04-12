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

    while True and not rospy.is_shutdown():
        process_mono = rospy.ServiceProxy("click_node/process_mono",ProcessMono)
        resp = process_mono("wide_stereo/left")
        pt = resp.pts3d[0]
        print pt
        GripUtils.go_to_pt(point=pt,roll=pi/2,pitch=pi/2,yaw=0,grip=True,arm="l",dur=5.0,link_name="l_tip_frame")
        print "waiting.."
        a = raw_input()

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
