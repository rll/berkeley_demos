#!/usr/bin/env python
import roslib
roslib.load_manifest("unfolding_smach")
import rospy
import GripUtils
from image_processor.srv import *
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped
from numpy import *
import sys
from smach import State, StateMachine
import smach_ros
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pr2_simple_motions_srvs.srv import *
from pr2_simple_motions_msgs.msg import *
import math
from nav_msgs.srv import *

numStacked = 0


def loadLocations():
	srv = rospy.ServiceProxy("locations/load_locations", LoadLocations)
	resp = srv("hackathon_demo")

def setNumStacked(num):
	global numStacked
	numStacked = num

def goToPosition(name):
	srv = rospy.ServiceProxy("locations/%s"%name, ExecuteLocation)
	resp = srv(5, [])
	return True

def goFromAToB(a, b):
	goToPosition("pre-%s"%a)
	goToPosition("pre-%s"%b)
	goToPosition(b)

def dryerToTable1():
	goFromAToB("Dryer", "Table1")

"""
Assumes Brett is already gripping pants from both sides.
"""
def table1ToTable2(width):
	global numStacked
	GripUtils.go_to_relative_multi(0, 0, 0.2, True, 0, 0, 0.2, True, "base_footprint", None)
	goFromAToB("Table1", "Table2")
	GripUtils.go_to_relative_multi(0, 0, -0.2+0.02*numStacked, True, 0, 0, -0.2+0.02*numStacked, True, "base_footprint", None)
	numStacked += 1
	GripUtils.open_grippers()

def table2ToDryer():
	goFromAToB("Table2", "Dryer")

def main(args):

    rospy.init_node("hackathon_nav")
    listener = tf.TransformListener()
    rospy.sleep(5)
    loadLocations()
    print "cycle"
    while raw_input():
        print "To Dryer"
        table2ToDryer()
        print "To Table1"
        dryerToTable1()
        print "To Table2"
        table1ToTable2(.5)

        print "cycle"
    
if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except rospy.ROSInterruptException: pass
