#!/usr/bin/env python  
import roslib
roslib.load_manifest('unfolding_smach')

import rospy
import tf

"""
Broadcasts all table-related frames for the PR2 unfolding demo(s)
Assumes a parameter "table_height" has been set
"""

if __name__ == '__main__':
    rospy.init_node('table_frame_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(1000.0)
    table_height = rospy.get_param("table_height",1.0)
    while not rospy.is_shutdown():
       br.sendTransform((0.0, 0.0, table_height),
                        (0.0, 0.0, 0.0, 1.0),
                        rospy.Time.now(),
                        "table_height",
                        "base_footprint")
       rate.sleep()

