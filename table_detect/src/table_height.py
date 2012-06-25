#!/usr/bin/python
import roslib; roslib.load_manifest('table_detect')
from pcl.msg import ModelCoefficients
import rospy
import rosparam
import tf
from geometry_msgs.msg import PointStamped
from subprocess import call
import math
import numpy as np

OFFSET = -0.005

def table_coeffs_cb(data):
    openni_frame = data.header.frame_id
    ps = PointStamped()
    ps.header.frame_id = openni_frame
    #print data.values
    h_openni = -data.values[3]/data.values[2]
    ps.point.z = h_openni
    try:
        listener.waitForTransform('base_footprint', openni_frame, rospy.Time.now(), rospy.Duration(4.0))
        #(trans, rot) = listener.lookupTransform('/base_link', openni_frame, rospy.Time())
        ps = listener.transformPoint('base_footprint', ps)
    except:
        return
    if math.isnan(ps.point.z) or np.isnan(ps.point.z):
        return
    h_floor = ps.point.z + OFFSET
    print 'table height: ', h_floor
    rosparam.set_param('/table_height', str(h_floor))
    call(['rosnode', 'kill', 'table_detect_node'])
    rospy.signal_shutdown('table height set')


#p = rospy.wait_for_message('table_model_coefficients', ModelCoefficients, 5.0)
rospy.init_node('table_height_node')
listener = tf.TransformListener()
rospy.Subscriber('table_model_coefficients', ModelCoefficients, table_coeffs_cb)
rospy.spin()
