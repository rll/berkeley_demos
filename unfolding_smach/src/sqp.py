from cvxopt import matrix, spmatrix, spdiag, sparse, normal
from cvxopt.solvers import qp
#from qp import qp
import tf
from time import clock
from sys import argv
from tf import transformations
import math
import rospy
try:
  import pymosek
except ImportError:
  import mosek
  MOSEK_VERSION = 6.0

from cvxopt import printing
from cvxopt import solvers
from geometry_msgs.msg import PoseStamped,Pose,Point,Quaternion

from numpy import r_

LOC = slice(0,3) # inds representing location
ORI = slice(3,7) # inds representing orientation

x_l = 0
y_l = 1
z_l = 2
x_r = 3
y_r = 4
z_r = 5
roll_l = 6
pitch_l = 7
yaw_l = 8
roll_r = 9
pitch_r = 10
yaw_r = 11
grip_l = 12
grip_r = 13

table_width = 1.05

pi = math.pi
def sparseSquare(value,n):
	return spmatrix(value, range(n), range(n))

def sparseZero(m,n):
	return spmatrix([], [], [], (m,n))


def base2gripper_to_torso2wrist(self,pvec):
        pvec = pvec.copy()
        x_ax = bgeom.quat2vec(pvec[3:7])
        pvec[0:3] -= .18 * x_ax # comes from looking up transform r_gripper_tool_frame -> r_wrist_roll_link        
        ps = gm.PoseStamped()
        ps.pose = bmsg.arr2msg(pvec,gm.Pose) # pose in base_link frame
        ps.header.frame_id = 'base_link'
        ps = self.tf_listener.transformPose('torso_lift_link',ps)
        return ps.pose

def torso2wrist_to_base2gripper(self,pvec):
        #pvec = pvec.copy()
        #x_ax = bgeom.quat2vec(pvec[3:7])
        #pvec[0:3] -= .18 * x_ax # comes from looking up transform r_gripper_tool_frame -> r_wrist_roll_link        
        pvec = pvec.copy()
	ps = gm.PoseStamped()
        ps.pose = bmsg.arr2msg(pvec,gm.Pose) # pose in base_link frame
        ps.header.frame_id = 'torso_lift_link'
        ps = self.tf_listener.transformPose('base_link',ps)
	new_pvec=_r[ps.pose]
	x_ax = bgeom.quat2vec(new_pvec[3:7])
	new_pvec[0:3] += .18 * x_ax
        return new_pvec

state_space_size = 14
def generate_trajectory_final(tl,tr,bl,br):#(init_state,goal_state)
	n = state_space_size*15
	A = matrix(0.0,(n,n))
        for i in range(state_space_size,state_space_size*4):
		A[i,i] = 1.0
	for i in range(state_space_size*5,state_space_size*14):
		A[i,i] = 1.0
	A[state_space_size*5+x_r, state_space_size*5+x_r] = 0.0
	A[state_space_size*5+y_r, state_space_size*5+4] = 0.0
	A[state_space_size*5+z_r, state_space_size*5+5] = 0.0
        A[state_space_size*5+roll_r, state_space_size*5+9] = 0.0
        A[state_space_size*5+pitch_r, state_space_size*5+10] = 0.0
        A[state_space_size*5+yaw_r, state_space_size*5+11] = 0.0

        A[state_space_size*6+x_r, state_space_size*6+x_r] = 0.0
        A[state_space_size*6+y_r, state_space_size*6+y_r] = 0.0
        A[state_space_size*6+z_r, state_space_size*6+z_r] = 0.0
        A[state_space_size*6+roll_r, state_space_size*6+roll_r] = 0.0
        A[state_space_size*6+pitch_r, state_space_size*6+pitch_r] = 0.0
        A[state_space_size*6+yaw_r, state_space_size*6+yaw_r] = 0.0

        A[state_space_size*7+x_r, state_space_size*7+x_r] = 0.0
        A[state_space_size*7+y_r, state_space_size*7+y_r] = 0.0
        A[state_space_size*7+z_r, state_space_size*7+z_r] = 0.0
        A[state_space_size*7+roll_r, state_space_size*7+roll_r] = 0.0
        A[state_space_size*7+pitch_r, state_space_size*7+pitch_r] = 0.0
        A[state_space_size*7+yaw_r, state_space_size*7+yaw_r] = 0.0

        A[state_space_size*8+x_r, state_space_size*8+x_r] = 0.0
        A[state_space_size*8+y_r, state_space_size*8+y_r] = 0.0
        A[state_space_size*8+z_r, state_space_size*8+z_r] = 0.0
        A[state_space_size*8+roll_r, state_space_size*8+roll_r] = 0.0
        A[state_space_size*8+pitch_r, state_space_size*8+pitch_r] = 0.0
        A[state_space_size*8+yaw_r, state_space_size*8+yaw_r] = 0.0        
 
        A[state_space_size*9+x_r, state_space_size*9+x_r] = 0.0
        A[state_space_size*9+y_r, state_space_size*9+y_r] = 0.0
        A[state_space_size*9+z_r, state_space_size*9+z_r] = 0.0
        A[state_space_size*9+roll_r, state_space_size*9+roll_r] = 0.0
        A[state_space_size*9+pitch_r, state_space_size*9+pitch_r] = 0.0
        A[state_space_size*9+yaw_r, state_space_size*9+yaw_r] = 0.0

        A[state_space_size*11+x_l, state_space_size*11+x_l] = 0.0
        A[state_space_size*11+y_l, state_space_size*11+y_l] = 0.0
        A[state_space_size*11+z_l, state_space_size*11+z_l] = 0.0
        A[state_space_size*11+roll_l, state_space_size*11+roll_l] = 0.0
        A[state_space_size*11+pitch_l, state_space_size*11+pitch_l] = 0.0
        A[state_space_size*11+yaw_l, state_space_size*11+yaw_l] = 0.0

        A[state_space_size*12+x_l, state_space_size*12+x_l] = 0.0
        A[state_space_size*12+y_l, state_space_size*12+y_l] = 0.0
        A[state_space_size*12+z_l, state_space_size*12+z_l] = 0.0
        A[state_space_size*12+roll_l, state_space_size*12+roll_l] = 0.0
        A[state_space_size*12+pitch_l, state_space_size*12+pitch_l] = 0.0
        A[state_space_size*12+yaw_l, state_space_size*12+yaw_l] = 0.0

        A[state_space_size*13+x_l, state_space_size*13+x_l] = 0.0
        A[state_space_size*13+y_l, state_space_size*13+y_l] = 0.0
        A[state_space_size*13+z_l, state_space_size*13+z_l] = 0.0
        A[state_space_size*13+roll_l, state_space_size*13+roll_l] = 0.0
        A[state_space_size*13+pitch_l, state_space_size*13+pitch_l] = 0.0
        A[state_space_size*13+yaw_l, state_space_size*13+yaw_l] = 0.0

        A[state_space_size*13+x_l, state_space_size*13+x_l] = 0.0
        A[state_space_size*13+y_l, state_space_size*13+y_l] = 0.0
        A[state_space_size*13+z_l, state_space_size*13+z_l] = 0.0
        A[state_space_size*13+roll_l, state_space_size*13+roll_l] = 0.0
        A[state_space_size*13+pitch_l, state_space_size*13+pitch_l] = 0.0
        A[state_space_size*13+yaw_l, state_space_size*13+yaw_l] = 0.0

	B = matrix(0.0, (n,1))
	B[state_space_size,0] = tl['x']-0.02
	B[state_space_size+1,0] = tl['y']
	B[state_space_size+2,0] = tl['z']
	B[state_space_size+3,0] = tr['x']-0.02
	B[state_space_size+4,0] = tr['y']
	B[state_space_size+5,0] = tr['z']
	B[state_space_size+6,0] = -math.pi/2
	B[state_space_size+7,0] = math.pi/4
	B[state_space_size+8,0] = -math.pi/3
	B[state_space_size+9,0] = math.pi/2
	B[state_space_size+10,0] = math.pi/4
	B[state_space_size+11,0] = math.pi/3
	B[state_space_size+12,0] = 1.0
	B[state_space_size+13,0] = 1.0
        B[state_space_size*2,0] = (tl['x'] + bl['x']) / 2.0
        B[state_space_size*2+1,0] = (tl['y'] + bl['y']) / 2.0
        B[state_space_size*2+2,0] = bl['z'] + (math.sqrt((tl['x'] - bl['x'])**2 + (tl['y'] - bl['y'])**2) / 2.0)
        B[state_space_size*2+3,0] = (tr['x'] + br['x']) / 2.0
        B[state_space_size*2+4,0] = (tr['y'] + br['y']) / 2.0
        B[state_space_size*2+5,0] = br['z'] + (math.sqrt((tr['x'] - br['x'])**2 + (tr['y'] - br['y'])**2) / 2.0)
        B[state_space_size*2+6,0] = 0
        B[state_space_size*2+7,0] = math.pi/4
        B[state_space_size*2+8,0] = -math.pi/2
        B[state_space_size*2+9,0] = 0
        B[state_space_size*2+10,0] = math.pi/4
        B[state_space_size*2+11,0] = math.pi/2
        B[state_space_size*2+12,0] = 1.0
        B[state_space_size*2+13,0] = 1.0
	B[state_space_size*3,0] = bl['x']
        B[state_space_size*3+1,0] = bl['y'] - 0.02
        B[state_space_size*3+2,0] = bl['z'] + 0.08
        B[state_space_size*3+3,0] = br['x']
        B[state_space_size*3+4,0] = br['y']
        B[state_space_size*3+5,0] = br['z'] + 0.08
        B[state_space_size*3+6,0] = math.pi/2
        B[state_space_size*3+7,0] = math.pi/4
        B[state_space_size*3+8,0] = -3*math.pi/4
        B[state_space_size*3+9,0] = -math.pi/2
        B[state_space_size*3+10,0] = math.pi/4
        B[state_space_size*3+11,0] = 3*math.pi/4
        B[state_space_size*3+12,0] = 1.0
        B[state_space_size*3+13,0] = 1.0
        B[state_space_size*5,0] = 0.75*bl['x'] + 0.25*tl['x']
        B[state_space_size*5+1,0] = 0.75*bl['y'] + 0.25*tl['y']
        B[state_space_size*5+2,0] = bl['z']
        B[state_space_size*5+6,0] = -math.pi/2
        B[state_space_size*5+7,0] = math.pi/4
        B[state_space_size*5+8,0] = -math.pi/2
        B[state_space_size*5+12,0] = 1.0
        B[state_space_size*5+13,0] = 1.0

        B[state_space_size*6,0] = (1.0-0.333)*(0.75*bl['x'] + 0.25*tl['x']) + 0.333*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*6+1,0] = (1.0-0.333)*(0.75*bl['y'] + 0.25*tl['y']) + 0.333*(0.75*br['y'] + 0.25*tr['y'])
        B[state_space_size*6+2,0] = bl['z'] + (math.sqrt( (0.75*bl['x'] + 0.25*tl['x'] - 0.75*br['x'] - 0.25*tr['x'])**2 + (0.75*bl['y'] + 0.25*tl['y'] - 0.75*br['y'] - 0.25*tr['y'])**2) / 3.0)
        B[state_space_size*6+6,0] = -math.pi/2
        B[state_space_size*6+7,0] = math.pi/2
        B[state_space_size*6+8,0] = -math.pi/2
        B[state_space_size*6+12,0] = 1.0
        B[state_space_size*6+13,0] = 1.0
		
        B[state_space_size*7,0] = (0.75*bl['x'] + 0.25*tl['x']+ 0.75*br['x'] + 0.25*tr['x']) / 2.0
        B[state_space_size*7+1,0] = (0.75*bl['y'] + 0.25*tl['y'] + 0.75*br['y'] + 0.25*tr['y']) /2.0
        B[state_space_size*7+2,0] = (2*bl['z'] + (math.sqrt( (0.75*bl['x'] + 0.25*tl['x'] - 0.75*br['x'] - 0.25*tr['x'])**2 + (0.75*bl['y'] + 0.25*tl['y'] - 0.75*br['y'] - 0.25*tr['y'])**2) / 3.0)) / 2.0
        B[state_space_size*7+6,0] = -math.pi/2
        B[state_space_size*7+7,0] = (math.pi/2 + 3*pi/4)/2.0
        B[state_space_size*7+8,0] = -math.pi/2
        B[state_space_size*7+12,0] = 1.0
        B[state_space_size*7+13,0] = 1.0
        
	B[state_space_size*8,0] = (0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (1.0-0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*8+1,0] = (0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (1.0-0.333)*(0.75*br['y'] + 0.25*tr['y'])
        B[state_space_size*8+2,0] = bl['z']
        B[state_space_size*8+6,0] = -math.pi/2
        B[state_space_size*8+7,0] = 3*math.pi/4
        B[state_space_size*8+8,0] = -math.pi/2
        B[state_space_size*8+12,0] = 1.0
        B[state_space_size*8+13,0] = 1.0

	B[state_space_size*9,0] = (0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (1.0-0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*9+1,0] = (0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (1.0-0.333)*(0.75*br['y'] + 0.25*tr['y'])-0.03
        B[state_space_size*9+2,0] = bl['z']
        B[state_space_size*9+6,0] = math.pi/2
        B[state_space_size*9+7,0] = math.pi/4
        B[state_space_size*9+8,0] = math.pi/2
        B[state_space_size*9+12,0] = 1.0
        B[state_space_size*9+13,0] = 1.0

        B[state_space_size*10+3,0] = 0.75*br['x'] + 0.25*tr['x']
        B[state_space_size*10+4,0] = 0.75*br['y'] + 0.25*tr['y']
        B[state_space_size*10+5,0] = bl['z']
        B[state_space_size*10+9,0] = math.pi/2
        B[state_space_size*10+10,0] = math.pi/4
        B[state_space_size*10+11,0] = math.pi/2
        B[state_space_size*10+12,0] = 1.0
        B[state_space_size*10+13,0] = 1.0

        B[state_space_size*10,0] = (0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (1.0-0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*10+1,0] = (0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (1.0-0.333)*(0.75*br['y'] + 0.25*tr['y'])-0.03
        B[state_space_size*10+2,0] = bl['z']+0.22
        B[state_space_size*10+6,0] = -math.pi/2
        B[state_space_size*10+7,0] = math.pi/4
        B[state_space_size*10+8,0] = -math.pi/3
        B[state_space_size*10+12,0] = 1.0
        B[state_space_size*10+13,0] = 1.0


	B[state_space_size*11+3,0] = (0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (1.0-0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*11+4,0] = (0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (1.0-0.333)*(0.75*br['y'] + 0.25*tr['y'])-0.03
        B[state_space_size*11+5,0] = bl['z'] + (math.sqrt( (0.75*bl['x'] + 0.25*tl['x'] - 0.75*br['x'] - 0.25*tr['x'])**2 + (0.75*bl['y'] + 0.25*tl['y'] - 0.75*br['y'] - 0.25*tr['y'])**2) / 3.0)
        B[state_space_size*11+9,0] = math.pi/2
        B[state_space_size*11+10,0] = math.pi/4
        B[state_space_size*11+11,0] = math.pi/2
        B[state_space_size*11+12,0] = 1.0
        B[state_space_size*11+13,0] = 1.0
	"""
        B[state_space_size*11+3,0] = (0.75*bl['x'] + 0.25*tl['x']+ 0.75*br['x'] + 0.25*tr['x']) / 2.0
        B[state_space_size*11+4,0] = (0.75*bl['y'] + 0.25*tl['y'] + 0.75*br['y'] + 0.25*tr['y'] - 0.06) /2
        B[state_space_size*11+5,0] = (2*bl['z'] + (math.sqrt( (0.75*bl['x'] + 0.25*tl['x'] - 0.75*br['x'] - 0.25*tr['x'])**2 + (0.75*bl['y'] + 0.25*tl['y'] - 0.75*br['y'] - 0.25*tr['y'])**2) / 3.0)) / 2.0
        B[state_space_size*11+9,0] = math.pi/2
        B[state_space_size*11+10,0] = math.pi/2
        B[state_space_size*11+11,0] = math.pi/2
        B[state_space_size*11+12,0] = 1.0
        B[state_space_size*11+13,0] = 1.0
	"""
        B[state_space_size*12+3,0] = (1 - 0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*12+4,0] = (1 - 0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (0.333)*(0.75*br['y'] + 0.25*tr['y'])-0.03
        B[state_space_size*12+5,0] = bl['z']+0.02
        B[state_space_size*12+9,0] = math.pi/2
        B[state_space_size*12+10,0] = 3*math.pi/4
        B[state_space_size*12+11,0] = math.pi/2
        B[state_space_size*12+12,0] = 1.0
        B[state_space_size*12+13,0] = 1.0

        B[state_space_size*13+3,0] = (1 - 0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*13+4,0] = (1 - 0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (0.333)*(0.75*br['y'] + 0.25*tr['y'])+0.03
        B[state_space_size*13+5,0] = bl['z']+0.02
        B[state_space_size*13+9,0] = math.pi/2
        B[state_space_size*13+10,0] = math.pi/4
        B[state_space_size*13+11,0] = math.pi/2
        B[state_space_size*13+12,0] = 1.0
        B[state_space_size*13+13,0] = 1.0

        B[state_space_size*13+3,0] = (1 - 0.333)*(0.75*bl['x'] + 0.25*tl['x']) + (0.333)*(0.75*br['x'] + 0.25*tr['x'])
        B[state_space_size*13+4,0] = (1 - 0.333)*(0.75*bl['y'] + 0.25*tl['y']) + (0.333)*(0.75*br['y'] + 0.25*tr['y'])+0.03
        B[state_space_size*13+5,0] = bl['z']+0.2
        B[state_space_size*13+9,0] = math.pi/2
        B[state_space_size*13+10,0] = math.pi/4
        B[state_space_size*13+11,0] = math.pi/2
        B[state_space_size*13+12,0] = 1.0
        B[state_space_size*13+13,0] = 1.0



	"""
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



		
	        yaw = pi/2
        roll = pi/2
        pitch = pi/4
        GripUtils.open_gripper("l")
        if not GripUtils.go_to(x=ctr_mr_x,y=ctr_mr_y-0.05,z=z+0.02,roll=roll,yaw=yaw,pitch=pitch,arm="l",frame=frame,grip=False,dur=1.0):
            return FAILURE
        GripUtils.recall_arm("l")
        if not GripUtils.grab(x=ctr_r_x,y=ctr_r_y-0.01,z=z,roll=roll,yaw=yaw,pitch=pitch,arm="r",frame=frame):
            return FAILURE


	if not GripUtils.go_to(x=(ctr_ml_x+ctr_mr_x)/2.0,y=(ctr_ml_y+ctr_mr_y+0.02)/2.0,z=(up_z+bl_z)/2.0,roll=roll,yaw=yaw,pitch=(pitch+3*pi/4)/2.0,arm="l",frame=frame,grip=True,dur=5.0):

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
	"""


	G = matrix(0.0,(n,n))
	G[1,1] = -1.0
	G[2,2] = -1.0
	G[4,4] = 1.0
	G[5,5] = -1.0
	G[state_space_size*4+1,state_space_size*4+1] = -1.0
	G[state_space_size*4+2,state_space_size*4+2] = -1.0
	G[state_space_size*4+4,state_space_size*4+4] = 1.0
	G[state_space_size*4+5,state_space_size*4+5] = -1.0
	G[state_space_size*11+y_l,state_space_size*11+y_l] = -1.0
	G[state_space_size*11+z_l,state_space_size*11+z_l] = -1.0
	#G[state_space_size*6+5,state_space_size*6+5] = -1.0
	H = matrix(0.0, (n,1))
	H[1,0] = -0.45
        H[2,0] = -0.85
	H[4,0] = -0.45
        H[5,0] = -0.85
	H[state_space_size*4+1,0] = -0.45
	H[state_space_size*4+4,0] = -0.45
        H[state_space_size*4+2,0] = -0.85
        H[state_space_size*4+5,0] = -0.85
	H[state_space_size*11+y_l,0]= -0.55
	H[state_space_size*11+z_l,0]= -0.95
	#H[state_space_size*6+5,0] = -0.85
	
	P = matrix(0.0, (n,n))
	for i in range(state_space_size):
		P[i,i] = 1.0
	for i in range(state_space_size,n-state_space_size):
		P[i,i] = 2.0
	for i in range(n-state_space_size,n):
		P[i,i] = 1.0
	for j in range(state_space_size,n):
		P[j,j-state_space_size] = -1.0
		P[j-state_space_size,j] = -1.0
	#print P[0:13,0:13]
	#P[0:14,0:14] = matrix(1.0, (state_space_size,state_space_size))
	#P[14:28,14:28] = matrix(1.0, (state_space_size,state_space_size))
	#print P
	Q = matrix(0.0, (n,1))
	#Q = sparseZero(14,1)
	#print Q
	x = qp(P,Q,G,H,A,B,solver='mosek')['x']
	#x= mosek.qp(P,Q,G,H,A,B)['x']
	print x
	pose_l = []
	pose_r = []
	for i in range(0,15):
		quat = tf.transformations.quaternion_from_euler(x[state_space_size*i+roll_l] , x[state_space_size*i+pitch_l], x[state_space_size*i+yaw_l])
		
		#quat=tf.transformations.quaternion_from_euler(0.0,0.0,0.0)
		#quat = tf.transformations.quaternion_from_euler(-math.pi/2.0,math.pi/4.0,-math.pi/3.0)
		pose_l.append(r_[x[state_space_size*i+x_l,0] , x[state_space_size*i+y_l,0], x[state_space_size*i+z_l,0], quat[0], quat[1],quat[2],quat[3]])
		
		print pose_l
		#pose_l.append(r_[0.6+i*0.01,0.45+i*0.01,-0.25+i*0.01, quat[0], quat[1],quat[2],quat[3]])
        for i in range(0,15):
	        #pose_r.append(r_[Pose(position = Point(x[state_space_size*i+6] , x[state_space_size*i+7], x[state_space_size*i+8]), orientation = tf.transformations.quaternion_from_euler(x[state_space_size*i+9] , x[state_space_size*i+10], x[state_space_size*i+11]))])
                quat = tf.transformations.quaternion_from_euler(x[state_space_size*i+roll_r] , x[state_space_size*i+pitch_r], x[state_space_size*i+yaw_r])
                #quat = tf.transformations.quaternion_from_euler(0.0,0.0,0.0)
		#quat = tf.transformations.quaternion_from_euler(math.pi/2.0,math.pi/4.0,math.pi/3.0)
		pose_r.append (r_[x[state_space_size*i+x_r,0] , x[state_space_size*i+y_r,0], x[state_space_size*i+z_r,0], quat[0], quat[1],quat[2],quat[3]])
		#pose_r.append(r_[0.6+i*0.01, -0.45+i*0.01, -0.25+i*0.01, quat[0], quat[1],quat[2],quat[3]])
		print pose_r
	return [x,pose_l,pose_r]



drag_offset = 0.01
def generate_trajectory_pick(pt):
        
	n = state_space_size*5
	z_offset = 0.06
        #GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
	A = matrix(0.0,(n,n))
        for i in range(state_space_size,state_space_size*5):
                A[i,i] = 1.0
        A[state_space_size+ x_r, state_space_size+x_r] = 0.0
        A[state_space_size + y_r, state_space_size+y_r] = 0.0
        A[state_space_size+z_r, state_space_size+z_r] = 0.0
        A[state_space_size+roll_r, state_space_size+roll_r] = 0.0
        A[state_space_size+pitch_r, state_space_size+pitch_r] = 0.0
        A[state_space_size+yaw_r, state_space_size+yaw_r] = 0.0
        A[state_space_size*2+ x_r, state_space_size*2+x_r] = 0.0
        A[state_space_size*2 + y_r, state_space_size*2+y_r] = 0.0
        A[state_space_size*2+z_r, state_space_size*2+z_r] = 0.0
        A[state_space_size*2+roll_r, state_space_size*2+roll_r] = 0.0
        A[state_space_size*2+pitch_r, state_space_size*2+pitch_r] = 0.0
        A[state_space_size*2+yaw_r, state_space_size*2+yaw_r] = 0.0
        A[state_space_size*3+ x_r, state_space_size*3+x_r] = 0.0
        A[state_space_size*3 + y_r, state_space_size*3+y_r] = 0.0
        A[state_space_size*3+z_r, state_space_size*3+z_r] = 0.0
        A[state_space_size*3+roll_r, state_space_size*3+roll_r] = 0.0
        A[state_space_size*3+pitch_r, state_space_size*3+pitch_r] = 0.0
        A[state_space_size*3+yaw_r, state_space_size*3+yaw_r] = 0.0

	

	B = matrix(0.0,(n,1))
	B[state_space_size,0] = pt.point.x
        B[state_space_size+1,0] = pt.point.y
        B[state_space_size+2,0] = pt.point.z
        B[state_space_size+6,0] = pi/2
        B[state_space_size+7,0] = pi/2
        B[state_space_size+8,0] = 0
        B[state_space_size+12,0] = 1.0
        B[state_space_size+13,0] = 1.0
        B[state_space_size*2,0] = 0.4 - drag_offset*2
        B[state_space_size*2+1,0] = -table_width/2.0 
        B[state_space_size*2+2,0] = 1.4		#Adjust based on towel width
        B[state_space_size*2+6,0] = pi/2
        B[state_space_size*2+7,0] = 0
        B[state_space_size*2+8,0] = -pi/2
        B[state_space_size*2+12,0] = 1.0
        B[state_space_size*2+13,0] = 1.0
        B[state_space_size*3,0] = 0.4 - drag_offset*2
        B[state_space_size*3+1,0] = -table_width/2.0 
        B[state_space_size*3+2,0] = 0.06+0.78         #Adjust based on towel width
        B[state_space_size*3+6,0] = pi/2
        B[state_space_size*3+7,0] = pi/4
        B[state_space_size*3+8,0] = -pi/2
        B[state_space_size*3+12,0] = 1.0
        B[state_space_size*3+13,0] = 1.0
        B[state_space_size*4,0] = 0.4 - drag_offset*2
        B[state_space_size*4+1,0] = -table_width/2.0 + table_width*0.95
        B[state_space_size*4+2,0] = 0.06+0.78         #Adjust based on towel width
        B[state_space_size*4+6,0] = pi/2
        B[state_space_size*4+7,0] = pi/4
        B[state_space_size*4+8,0] = -pi/2
        B[state_space_size*4+12,0] = 1.0
        B[state_space_size*4+13,0] = 1.0
        B[state_space_size*4+x_r,0] = 0.6
        B[state_space_size*4+y_r,0] = -0.45
        B[state_space_size*4+z_r,0] = 0.85         #Adjust based on towel width
        B[state_space_size*4+roll_r,0] = pi/2
        B[state_space_size*4+pitch_r,0] = pi/4
        B[state_space_size*4+yaw_r,0] = pi/3
        B[state_space_size*4+12,0] = 1.0
        B[state_space_size*4+13,0] = 1.0



	
        G = matrix(0.0,(n,n))
	G[2,2] = -1.0
	G[x_r,x_r]=1.0
	G[y_r,y_r]=1.0
	G[z_r,z_r]=-1.0
        G[state_space_size+x_r,state_space_size+x_r]=1.0
        G[state_space_size+y_r,state_space_size+y_r]=1.0
        G[state_space_size+z_r,state_space_size+z_r]=-1.0
        G[state_space_size*2+x_r,state_space_size*2+x_r]=1.0
        G[state_space_size*2+y_r,state_space_size*2+y_r]=1.0
        G[state_space_size*2+z_r,state_space_size*2+z_r]=-1.0
        G[state_space_size*3+x_r,state_space_size*3+x_r]=1.0
        G[state_space_size*3+y_r,state_space_size*3+y_r]=1.0
        G[state_space_size*3+z_r,state_space_size*3+z_r]=-1.0
       #G[state_space_size*6+5,state_space_size*6+5] = -1.0
        H = matrix(0.0, (n,1))
	H[2,0] = -0.95
        H[x_r,0]=0.3
        H[y_r,0]=-0.8
        H[z_r,0]=-0.9
        H[state_space_size+x_r,0]=0.2
        H[state_space_size+y_r,0]=-0.8
        H[state_space_size+z_r,0]=-0.9
        H[state_space_size*2+x_r,0]=0.2
        H[state_space_size*2+y_r,0]=-0.8
        H[state_space_size*2+z_r,0]=-0.9
        H[state_space_size*3+x_r,0]=0.2
        H[state_space_size*3+y_r,0]=-0.8
        H[state_space_size*3+z_r,0]=-0.9
#H[state_space_size*6+5,0] = -0.85

        P = matrix(0.0, (n,n))
        for i in range(state_space_size):
                P[i,i] = 1.0
        for i in range(state_space_size,n-state_space_size):
                P[i,i] = 2.0
        for i in range(n-state_space_size,n):
                P[i,i] = 1.0
        for j in range(state_space_size,n):
                P[j,j-state_space_size] = -1.0
                P[j-state_space_size,j] = -1.0
        #print P[0:13,0:13]
        #P[0:14,0:14] = matrix(1.0, (state_space_size,state_space_size))
        #P[14:28,14:28] = matrix(1.0, (state_space_size,state_space_size))
        #print P
        Q = matrix(0.0, (n,1))
        #Q = sparseZero(14,1)
        #print Q
        x = qp(P,Q,G,H,A,B,solver='mosek')['x']
	return x

pt_r = None

def generate_trajectory_sweepright(pt):
       
	pt_r = pt
	n = state_space_size*4
        #GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
	A = matrix(0.0,(n,n))
        for i in range(state_space_size*4):
                A[i,i] = 1.0
        A[state_space_size+ x_l, state_space_size+x_l] = 0.0
        A[state_space_size +y_l, state_space_size+y_l] = 0.0
        A[state_space_size+z_l, state_space_size+z_l] = 0.0
        A[state_space_size+roll_l, state_space_size+roll_l] = 0.0
        A[state_space_size+pitch_l, state_space_size+pitch_l] = 0.0
        A[state_space_size+yaw_l, state_space_size+yaw_l] = 0.0
        A[state_space_size*2+ x_l, state_space_size*2+x_l] = 0.0
        A[state_space_size*2 + y_l, state_space_size*2+y_l] = 0.0
        A[state_space_size*2+z_l, state_space_size*2+z_l] = 0.0
        A[state_space_size*2+roll_l, state_space_size*2+roll_l] = 0.0
        A[state_space_size*2+pitch_l, state_space_size*2+pitch_l] = 0.0
        A[state_space_size*2+yaw_l, state_space_size*2+yaw_l] = 0.0
	
	

	B = matrix(0.0,(n,1))
	B[0,0] = 0.4
        B[1,0] = -table_width/2 + table_width*0.95
        B[2,0] = 0.06+0.78
        B[6,0] = pi/2
        B[7,0] = pi/4
        B[8,0] = -pi/2
        B[12,0] = 1.0
        B[13,0] = 1.0
        B[x_r,0] = pt.point.x
        B[y_r,0] = pt.point.y
        B[z_r,0] = pt.point.z
        B[roll_r,0] = -pi/2
        B[pitch_r,0] = pi/4
        B[yaw_r,0] = pi/2
        B[12,0] = 1.0
        B[13,0] = 1.0
        B[state_space_size+x_r,0] = 0.4 - drag_offset*2
        B[state_space_size+y_r,0] = table_width/2.0
        B[state_space_size+z_r,0] = 1.4 	#Adjust based on towel width
        B[state_space_size+roll_r,0] = pi/2
        B[state_space_size+pitch_r,0] = 0
        B[state_space_size+yaw_r,0] = pi/2
        B[state_space_size+12,0] = 1.0
        B[state_space_size+13,0] = 1.0
        B[state_space_size*2+x_r,0] = 0.4 - drag_offset*2
        B[state_space_size*2+y_r,0] = table_width/2.0 
        B[state_space_size*2+z_r,0] = 0.06+0.78         #Adjust based on towel width
        B[state_space_size*2+roll_r,0] = pi/2
        B[state_space_size*2+pitch_r,0] = pi/4
        B[state_space_size*2+yaw_r,0] = pi/2
        B[state_space_size*2+12,0] = 1.0
        B[state_space_size*2+13,0] = 1.0
        B[state_space_size*3+x_r,0] = 0.4 - drag_offset*2
        B[state_space_size*3+y_r,0] = table_width/2.0 - table_width*0.95
        B[state_space_size*3+z_r,0] = 0.06+0.78         #Adjust based on towel width
        B[state_space_size*3+roll_r,0] = pi/2
        B[state_space_size*3+pitch_r,0] = pi/4
        B[state_space_size*3+yaw_r,0] = pi/2
        B[state_space_size*3+12,0] = 1.0
        B[state_space_size*3+13,0] = 1.0
        B[state_space_size*3+x_l,0] = 0.6
        B[state_space_size*3+y_l,0] = 0.45
        B[state_space_size*3+z_l,0] = 0.85         #Adjust based on towel width
        B[state_space_size*3+roll_l,0] = -pi/2
        B[state_space_size*3+pitch_l,0] = pi/4
        B[state_space_size*3+yaw_l,0] = -pi/3
        #B[state_space_size*3+12,0] = 1.0
        #B[state_space_size*3+13,0] = 1.0



	
        G = matrix(0.0,(n,n))
        G[state_space_size+x_l,state_space_size+x_l]=1.0
        G[state_space_size+y_l,state_space_size+y_l]=-1.0
        G[state_space_size+z_l,state_space_size+z_l]=-1.0
        G[state_space_size*2+x_l,state_space_size*2+x_l]=1.0
        G[state_space_size*2+y_l,state_space_size*2+y_l]=-1.0
        G[state_space_size*2+z_l,state_space_size*2+z_l]=-1.0
       #G[state_space_size*6+5,state_space_size*6+5] = -1.0
        H = matrix(0.0, (n,1))
        H[state_space_size+x_l,0]=0.2
        H[state_space_size+y_l,0]=-0.8
        H[state_space_size+z_l,0]=-0.9
        H[state_space_size*2+x_l,0]=0.2
        H[state_space_size*2+y_l,0]=-0.8
        H[state_space_size*2+z_l,0]=-0.9
#H[state_space_size*6+5,0] = -0.85

        P = matrix(0.0, (n,n))
        for i in range(state_space_size):
                P[i,i] = 1.0
        for i in range(state_space_size,n-state_space_size):
                P[i,i] = 2.0
        for i in range(n-state_space_size,n):
                P[i,i] = 1.0
        for j in range(state_space_size,n):
                P[j,j-state_space_size] = -1.0
                P[j-state_space_size,j] = -1.0
        #print P[0:13,0:13]
        #P[0:14,0:14] = matrix(1.0, (state_space_size,state_space_size))
        #P[14:28,14:28] = matrix(1.0, (state_space_size,state_space_size))
        #print P
        Q = matrix(0.0, (n,1))
        #Q = sparseZero(14,1)
        #print Q
        x = qp(P,Q,G,H,A,B,solver='mosek')['x']
	return x

def generate_trajectory_layout(pt,cloth_width):
        forward_amount = 0.48
	#cloth_width = cloth_width *0.925 
	n = state_space_size*6
        #GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
	A = matrix(0.0,(n,n))
        for i in range(state_space_size*6):
                A[i,i] = 1.0

	

	B = matrix(0.0,(n,1))
	B[0,0] = pt.point.x - 0.02
        B[1,0] = pt.point.y
        B[2,0] = pt.point.z
        B[6,0] = -pi/2
        B[7,0] = pi/4
        B[8,0] = -pi/2
        B[12,0] = 1.0
        B[13,0] = 1.0
        #B[x_r,0] = pt_r.point.x
        #B[y_r,0] = pt_r.point.y
        #B[z_r,0] = pt_r.point.z
        #B[roll_r,0] = -pi/2
        #B[pitch_r,0] = pi/4
        #B[yaw_r,0] = pi/2
        #B[12,0] = 1.0
        #B[13,0] = 1.0
        B[state_space_size+x_l,0] = 0.2
        B[state_space_size+y_l,0] = cloth_width/2.0
        B[state_space_size+z_l,0] = 0.625 + 0.78         #Adjust based on towel width
        B[state_space_size+roll_l,0] = 0
        B[state_space_size+pitch_l,0] = 0
        B[state_space_size+yaw_l,0] = -pi/2
        B[state_space_size+x_r,0] = 0.2
        B[state_space_size+y_r,0] = -cloth_width/2.0
        B[state_space_size+z_r,0] = 0.625 + 0.78		#Adjust based on towel width
        B[state_space_size+roll_r,0] = 0
        B[state_space_size+pitch_r,0] = 0
        B[state_space_size+yaw_r,0] = pi/2
        B[state_space_size+12,0] = 1.0
        B[state_space_size+13,0] = 1.0
        B[state_space_size*2+x_l,0] = 0.2
        B[state_space_size*2+y_l,0] = cloth_width/2.0
        B[state_space_size*2+z_l,0] = (0.75*0.625 + 0.25*0.03) + 0.78         #Adjust based on towel width
        B[state_space_size*2+roll_l,0] = 0
        B[state_space_size*2+pitch_l,0] = pi/4
        B[state_space_size*2+yaw_l,0] = -pi/2
        B[state_space_size*2+x_r,0] = 0.2
        B[state_space_size*2+y_r,0] = -cloth_width/2.0
        B[state_space_size*2+z_r,0] = (0.75*0.625 + 0.25*0.03) + 0.78                #Adjust based on towel width
        B[state_space_size*2+roll_r,0] = 0
        B[state_space_size*2+pitch_r,0] = pi/4
        B[state_space_size*2+yaw_r,0] = pi/2
        B[state_space_size*2+12,0] = 1.0
        B[state_space_size*2+13,0] = 1.0
        B[state_space_size*3+x_l,0] = (0.2*2 + forward_amount)/2.0
        B[state_space_size*3+y_l,0] = cloth_width/2.0
        B[state_space_size*3+z_l,0] = (0.25*0.625 + 0.75*0.03) + 0.78         #Adjust based on towel width
        B[state_space_size*3+roll_l,0] = 0
        B[state_space_size*3+pitch_l,0] = pi/4
        B[state_space_size*3+yaw_l,0] = -pi/2
        B[state_space_size*3+x_r,0] = (0.2*2 + forward_amount)/2.0
        B[state_space_size*3+y_r,0] = -cloth_width/2.0
        B[state_space_size*3+z_r,0] = (0.25*0.625 + 0.75*0.03) + 0.78                #Adjust based on towel width
        B[state_space_size*3+roll_r,0] = 0
        B[state_space_size*3+pitch_r,0] = pi/4
        B[state_space_size*3+yaw_r,0] = pi/2
        B[state_space_size*3+12,0] = 1.0
        B[state_space_size*3+13,0] = 1.0
        B[state_space_size*4+x_l,0] = 0.2 + forward_amount - 0.1
        B[state_space_size*4+y_l,0] = cloth_width/2.0
        B[state_space_size*4+z_l,0] = (0.25*0.625 + 0.75*0.03) + 0.78         #Adjust based on towel width
        B[state_space_size*4+roll_l,0] = 0
        B[state_space_size*4+pitch_l,0] = pi/4
        B[state_space_size*4+yaw_l,0] = -pi/2
        B[state_space_size*4+x_r,0] = 0.2 + forward_amount - 0.1
        B[state_space_size*4+y_r,0] = -cloth_width/2.0
        B[state_space_size*4+z_r,0] = (0.25*0.625 + 0.75*0.03) + 0.78                #Adjust based on towel width
        B[state_space_size*4+roll_r,0] = 0
        B[state_space_size*4+pitch_r,0] = pi/4
        B[state_space_size*4+yaw_r,0] = pi/2
        B[state_space_size*4+12,0] = 1.0
        B[state_space_size*4+13,0] = 1.0
        B[state_space_size*5+x_l,0] = 0.2 + forward_amount + 0.1
        B[state_space_size*5+y_l,0] = cloth_width/2.0
        B[state_space_size*5+z_l,0] = 0.03 + 0.03 + 0.78         #Adjust based on towel width
        B[state_space_size*5+roll_l,0] = 0
        B[state_space_size*5+pitch_l,0] = pi/4
        B[state_space_size*5+yaw_l,0] = -pi/5
        B[state_space_size*5+x_r,0] = 0.2 + forward_amount + 0.1
        B[state_space_size*5+y_r,0] = -cloth_width/2.0
        B[state_space_size*5+z_r,0] = 0.03 + 0.03 + 0.78                #Adjust based on towel width
        B[state_space_size*5+roll_r,0] = 0
        B[state_space_size*5+pitch_r,0] = pi/4
        B[state_space_size*5+yaw_r,0] = pi/5
        B[state_space_size*5+12,0] = 1.0
        B[state_space_size*5+13,0] = 1.0



	
        G = matrix(0.0,(n,n))
      #G[state_space_size*6+5,state_space_size*6+5] = -1.0
        H = matrix(0.0, (n,1))

#H[state_space_size*6+5,0] = -0.85

        P = matrix(0.0, (n,n))
        for i in range(state_space_size):
                P[i,i] = 1.0
        for i in range(state_space_size,n-state_space_size):
                P[i,i] = 2.0
        for i in range(n-state_space_size,n):
                P[i,i] = 1.0
        for j in range(state_space_size,n):
                P[j,j-state_space_size] = -1.0
                P[j-state_space_size,j] = -1.0
        #print P[0:13,0:13]
        #P[0:14,0:14] = matrix(1.0, (state_space_size,state_space_size))
        #P[14:28,14:28] = matrix(1.0, (state_space_size,state_space_size))
        #print P
        Q = matrix(0.0, (n,1))
        #Q = sparseZero(14,1)
        #print Q
        x = qp(P,Q,G,H,A,B,solver='mosek')['x']
	return x

def generate_trajectory_rect(pt_l,pt_r,left,cloth_width):
      	forward_amount = 0.45 
	#cloth_width = cloth_width *0.925 
	n = state_space_size*8
        #GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
	A = matrix(0.0,(n,n))
        for i in range(state_space_size*7):
                A[i,i] = 1.0
	if left:
		A[x_l,x_l] = 0.0
		A[y_l,y_l] = 0.0
		A[z_l,z_l] = 0.0
		A[roll_l,roll_l] = 0.0
		A[pitch_l,pitch_l] = 0.0
		A[yaw_l,yaw_l] = 0.0
	else:
                A[x_r,x_r] = 0.0
                A[y_r,y_r] = 0.0
                A[z_r,z_r] = 0.0
                A[roll_r,roll_r] = 0.0
                A[pitch_r,pitch_r] = 0.0 
                A[yaw_r,yaw_r] = 0.0
	

	B = matrix(0.0,(n,1))
	if left:
		B[x_r,0] = pt_r.point.x
        	B[y_r,0] = pt_r.point.y
		B[z_r,0] = pt_r.point.z
		B[roll_r,0] = -pi/2
		B[pitch_r,0] = pi/4
		B[yaw_r,0] = pi/3
	else:
                B[x_l,0] = pt_l.point.x
                B[y_l,0] = pt_l.point.y
                B[z_l,0] = pt_l.point.z
                B[roll_l,0] = pi/2
                B[pitch_l,0] = pi/4
                B[yaw_l,0] = -pi/3
        B[state_space_size+x_r,0] = pt_r.point.x
        B[state_space_size+y_r,0] = pt_r.point.y
        B[state_space_size+z_r,0] = pt_r.point.z
        B[state_space_size+roll_r,0] = -pi/2
        B[state_space_size+pitch_r,0] = pi/4
        B[state_space_size+yaw_r,0] = pi/3
        B[state_space_size+x_l,0] = pt_l.point.x
        B[state_space_size+y_l,0] = pt_l.point.y
        B[state_space_size+z_l,0] = pt_l.point.z
        B[state_space_size+roll_l,0] = pi/2
        B[state_space_size+pitch_l,0] = pi/4
        B[state_space_size+yaw_l,0] = -pi/3

        B[state_space_size*2+x_l,0] = 0.2 
        B[state_space_size*2+y_l,0] = cloth_width/2.0
        B[state_space_size*2+z_l,0] = 0.625 + 0.78         #Adjust based on towel width
        B[state_space_size*2+roll_l,0] = 0
        B[state_space_size*2+pitch_l,0] = 0
        B[state_space_size*2+yaw_l,0] = -pi/2
        B[state_space_size*2+x_r,0] = 0.2
        B[state_space_size*2+y_r,0] = -cloth_width/2.0
        B[state_space_size*2+z_r,0] = 0.625 + 0.78		#Adjust based on towel width
        B[state_space_size*2+roll_r,0] = 0
        B[state_space_size*2+pitch_r,0] = 0
        B[state_space_size*2+yaw_r,0] = pi/2
        B[state_space_size*2+12,0] = 1.0
        B[state_space_size*2+13,0] = 1.0
        B[state_space_size*3+x_l,0] = 0.2
        B[state_space_size*3+y_l,0] = cloth_width/2.0
        B[state_space_size*3+z_l,0] = (0.75*0.625 + 0.25*0.03) + 0.78         #Adjust based on towel width
        B[state_space_size*3+roll_l,0] = 0
        B[state_space_size*3+pitch_l,0] = pi/4
        B[state_space_size*3+yaw_l,0] = -pi/2
        B[state_space_size*3+x_r,0] = 0.2
        B[state_space_size*3+y_r,0] = -cloth_width/2.0
        B[state_space_size*3+z_r,0] = (0.75*0.625 + 0.25*0.03) + 0.78                #Adjust based on towel width
        B[state_space_size*3+roll_r,0] = 0
        B[state_space_size*3+pitch_r,0] = pi/4
        B[state_space_size*3+yaw_r,0] = pi/2
        B[state_space_size*3+12,0] = 1.0
        B[state_space_size*3+13,0] = 1.0
        B[state_space_size*4+x_l,0] = (0.2*2 + forward_amount)/2.0#forward_amount + 0.2 - 0.1 - cloth_height/2
        B[state_space_size*4+y_l,0] = cloth_width/2.0
        B[state_space_size*4+z_l,0] = (0.25*0.625 + 0.75*0.03) + 0.78         #Adjust based on towel width
        B[state_space_size*4+roll_l,0] = 0
        B[state_space_size*4+pitch_l,0] = pi/4
        B[state_space_size*4+yaw_l,0] = -pi/2
        B[state_space_size*4+x_r,0] = (0.2*2 + forward_amount)/2.0
        B[state_space_size*4+y_r,0] = -cloth_width/2.0
        B[state_space_size*4+z_r,0] = (0.25*0.625 + 0.75*0.03) + 0.78                 #Adjust based on towel width
        B[state_space_size*4+roll_r,0] = 0
        B[state_space_size*4+pitch_r,0] = pi/4
        B[state_space_size*4+yaw_r,0] = pi/2
        B[state_space_size*4+12,0] = 1.0
        B[state_space_size*4+13,0] = 1.0
        B[state_space_size*5+x_l,0] = 0.2 + forward_amount - 0.1
        B[state_space_size*5+y_l,0] = cloth_width/2.0
        B[state_space_size*5+z_l,0] = (0.25*0.625 + 0.75*0.03) + 0.78         #Adjust based on towel width
        B[state_space_size*5+roll_l,0] = 0
        B[state_space_size*5+pitch_l,0] = pi/4
        B[state_space_size*5+yaw_l,0] = -pi/2
        B[state_space_size*5+x_r,0] = 0.2 + forward_amount - 0.1
        B[state_space_size*5+y_r,0] = -cloth_width/2.0
        B[state_space_size*5+z_r,0] = (0.25*0.625 + 0.75*0.03) + 0.78                #Adjust based on towel width
        B[state_space_size*5+roll_r,0] = 0
        B[state_space_size*5+pitch_r,0] = pi/4
        B[state_space_size*5+yaw_r,0] = pi/2
        B[state_space_size*5+12,0] = 1.0
        B[state_space_size*5+13,0] = 1.0
        B[state_space_size*6+x_l,0] = 0.2 + forward_amount + 0.1
        B[state_space_size*6+y_l,0] = cloth_width/2.0
        B[state_space_size*6+z_l,0] = 0.03 + 0.03 + 0.78         #Adjust based on towel width
        B[state_space_size*6+roll_l,0] = 0
        B[state_space_size*6+pitch_l,0] = pi/4
        B[state_space_size*6+yaw_l,0] = -pi/5
        B[state_space_size*6+x_r,0] = 0.2 + forward_amount + 0.1
        B[state_space_size*6+y_r,0] = -cloth_width/2.0
        B[state_space_size*6+z_r,0] = 0.03 + 0.03 + 0.78                #Adjust based on towel width
        B[state_space_size*6+roll_r,0] = 0
        B[state_space_size*6+pitch_r,0] = pi/4
        B[state_space_size*6+yaw_r,0] = pi/5
        B[state_space_size*6+12,0] = 1.0
        B[state_space_size*6+13,0] = 1.0



	
        G = matrix(0.0,(n,n))
        if left:
                G[y_l,y_l] = -1.0
                G[z_l,z_l] = -1.0
        else:
                G[y_r,y_r] = 1.0
                G[z_r,z_r] = -1.0
	G[state_space_size*7+y_l,state_space_size*7+y_l] = -1.0
      	G[state_space_size*7+z_l,state_space_size*7+z_l] = -1.0
	G[state_space_size*7+y_r,state_space_size*7+y_r] = 1.0
	G[state_space_size*7+z_r,state_space_size*7+z_r] = -1.0
	#G[state_space_size*6+5,state_space_size*6+5] = -1.0

        H = matrix(0.0, (n,1))
        if left:
                H[y_l,0] = -0.4
                H[z_l,0] = -0.85
        else:   
                H[y_r,0] = -0.4
                H[z_r,0] = -0.85
        H[state_space_size*7+y_l,0] = -0.4
        H[state_space_size*7+z_l,0] = -0.85
        H[state_space_size*7+y_r,0] = -0.4
        H[state_space_size*7+z_r,0] = -0.85


	#H[state_space_size*6+5,0] = -0.85

        P = matrix(0.0, (n,n))
        for i in range(state_space_size):
                P[i,i] = 1.0
        for i in range(state_space_size,n-state_space_size):
                P[i,i] = 2.0
        for i in range(n-state_space_size,n):
                P[i,i] = 1.0
        for j in range(state_space_size,n):
                P[j,j-state_space_size] = -1.0
                P[j-state_space_size,j] = -1.0
        #print P[0:13,0:13]
        #P[0:14,0:14] = matrix(1.0, (state_space_size,state_space_size))
        #P[14:28,14:28] = matrix(1.0, (state_space_size,state_space_size))
        #print P
        Q = matrix(0.0, (n,1))
        #Q = sparseZero(14,1)
        #print Q
        x = qp(P,Q,G,H,A,B,solver='mosek')['x']
	return x

def generate_trajectory_flip(pt_bl,pt_br,cloth_width):
      	forward_amount = 0.45 
	#cloth_width = cloth_width *0.925 
	n = state_space_size*7
        #GripUtils.go_to_pt(pt,roll=pi/2,yaw=0,pitch=pi/2,arm="l",z_offset=z_offset,grip=False,dur=5.0)
	A = matrix(0.0,(n,n))
        for i in range(state_space_size*6):
                A[i,i] = 1.0

	B = matrix(0.0,(n,1))
        B[x_r,0] = pt_br.point.x+0.02
        B[y_r,0] = pt_br.point.y-0.02
        B[z_r,0] = pt_br.point.z
        B[roll_r,0] = -pi/2
        B[pitch_r,0] = pi/4
        B[yaw_r,0] = pi/2
        B[x_l,0] = pt_bl.point.x+0.02
        B[y_l,0] = pt_bl.point.y
        B[z_l,0] = pt_bl.point.z
        B[roll_l,0] = pi/2
        B[pitch_l,0] = pi/4
        B[yaw_l,0] = -pi/2

        B[state_space_size+x_l,0] = 0.2 
        B[state_space_size+y_l,0] = cloth_width/2.0
        B[state_space_size+z_l,0] = 0.625 + 0.78         #Adjust based on towel width
        B[state_space_size+roll_l,0] = 0
        B[state_space_size+pitch_l,0] = 0
        B[state_space_size+yaw_l,0] = -pi/2
        B[state_space_size+x_r,0] = 0.2
        B[state_space_size+y_r,0] = -cloth_width/2.0
        B[state_space_size+z_r,0] = 0.625 + 0.78		#Adjust based on towel width
        B[state_space_size+roll_r,0] = 0
        B[state_space_size+pitch_r,0] = 0
        B[state_space_size+yaw_r,0] = pi/2
        B[state_space_size+12,0] = 1.0
        B[state_space_size+13,0] = 1.0
        B[state_space_size*2+x_l,0] = 0.2
        B[state_space_size*2+y_l,0] = cloth_width/2.0
        B[state_space_size*2+z_l,0] = (0.75*0.625 + 0.25*0.06) + 0.78         #Adjust based on towel width
        B[state_space_size*2+roll_l,0] = 0
        B[state_space_size*2+pitch_l,0] = pi/4
        B[state_space_size*2+yaw_l,0] = -pi/2
        B[state_space_size*2+x_r,0] = 0.2
        B[state_space_size*2+y_r,0] = -cloth_width/2.0
        B[state_space_size*2+z_r,0] = (0.75*0.625 + 0.25*0.06) + 0.78                #Adjust based on towel width
        B[state_space_size*2+roll_r,0] = 0
        B[state_space_size*2+pitch_r,0] = pi/4
        B[state_space_size*2+yaw_r,0] = pi/2
        B[state_space_size*2+12,0] = 1.0
        B[state_space_size*2+13,0] = 1.0
        B[state_space_size*3+x_l,0] = (0.2*2 + forward_amount)/2.0#forward_amount + 0.2 - 0.1 - cloth_height/2
        B[state_space_size*3+y_l,0] = cloth_width/2.0
        B[state_space_size*3+z_l,0] = (0.25*0.625 + 0.75*0.06) + 0.78         #Adjust based on towel width
        B[state_space_size*3+roll_l,0] = 0
        B[state_space_size*3+pitch_l,0] = pi/4
        B[state_space_size*3+yaw_l,0] = -pi/2
        B[state_space_size*3+x_r,0] = (0.2*2 + forward_amount)/2.0
        B[state_space_size*3+y_r,0] = -cloth_width/2.0
        B[state_space_size*3+z_r,0] = (0.25*0.625 + 0.75*0.06) + 0.78                 #Adjust based on towel width
        B[state_space_size*3+roll_r,0] = 0
        B[state_space_size*3+pitch_r,0] = pi/4
        B[state_space_size*3+yaw_r,0] = pi/2
        B[state_space_size*3+12,0] = 1.0
        B[state_space_size*3+13,0] = 1.0
        B[state_space_size*4+x_l,0] = 0.2 + forward_amount - 0.1
        B[state_space_size*4+y_l,0] = cloth_width/2.0
        B[state_space_size*4+z_l,0] = (0.25*0.625 + 0.75*0.06) + 0.78         #Adjust based on towel width
        B[state_space_size*4+roll_l,0] = 0
        B[state_space_size*4+pitch_l,0] = pi/4
        B[state_space_size*4+yaw_l,0] = -pi/2
        B[state_space_size*4+x_r,0] = 0.2 + forward_amount - 0.1
        B[state_space_size*4+y_r,0] = -cloth_width/2.0
        B[state_space_size*4+z_r,0] = (0.25*0.625 + 0.75*0.06) + 0.78                #Adjust based on towel width
        B[state_space_size*4+roll_r,0] = 0
        B[state_space_size*4+pitch_r,0] = pi/4
        B[state_space_size*4+yaw_r,0] = pi/2
        B[state_space_size*4+12,0] = 1.0
        B[state_space_size*4+13,0] = 1.0
        B[state_space_size*5+x_l,0] = 0.2 + forward_amount + 0.1
        B[state_space_size*5+y_l,0] = cloth_width/2.0
        B[state_space_size*5+z_l,0] = 0.03 + 0.03 + 0.78         #Adjust based on towel width
        B[state_space_size*5+roll_l,0] = 0
        B[state_space_size*5+pitch_l,0] = pi/4
        B[state_space_size*5+yaw_l,0] = -pi/5
        B[state_space_size*5+x_r,0] = 0.2 + forward_amount + 0.1
        B[state_space_size*5+y_r,0] = -cloth_width/2.0
        B[state_space_size*5+z_r,0] = 0.03 + 0.03 + 0.78                #Adjust based on towel width
        B[state_space_size*5+roll_r,0] = 0
        B[state_space_size*5+pitch_r,0] = pi/4
        B[state_space_size*5+yaw_r,0] = pi/5
        B[state_space_size*5+12,0] = 1.0
        B[state_space_size*5+13,0] = 1.0



	
        G = matrix(0.0,(n,n))
	G[state_space_size*6+y_l,state_space_size*6+y_l] = -1.0
      	G[state_space_size*6+z_l,state_space_size*6+z_l] = -1.0
	G[state_space_size*6+y_r,state_space_size*6+y_r] = 1.0
	G[state_space_size*6+z_r,state_space_size*6+z_r] = -1.0
	#G[state_space_size*6+5,state_space_size*6+5] = -1.0

        H = matrix(0.0, (n,1))
        H[state_space_size*6+y_l,0] = -0.4
        H[state_space_size*6+z_l,0] = -0.85
        H[state_space_size*6+y_r,0] = -0.4
        H[state_space_size*6+z_r,0] = -0.85


	#H[state_space_size*6+5,0] = -0.85

        P = matrix(0.0, (n,n))
        for i in range(state_space_size):
                P[i,i] = 1.0
        for i in range(state_space_size,n-state_space_size):
                P[i,i] = 2.0
        for i in range(n-state_space_size,n):
                P[i,i] = 1.0
        for j in range(state_space_size,n):
                P[j,j-state_space_size] = -1.0
                P[j-state_space_size,j] = -1.0
        #print P[0:13,0:13]
        #P[0:14,0:14] = matrix(1.0, (state_space_size,state_space_size))
        #P[14:28,14:28] = matrix(1.0, (state_space_size,state_space_size))
        #print P
        Q = matrix(0.0, (n,1))
        #Q = sparseZero(14,1)
        #print Q
        x = qp(P,Q,G,H,A,B,solver='mosek')['x']
	return x



if __name__ == "__main__":
	generate_trajectory({'x':0, 'y':0, 'z':0}, {'x':0, 'y':0, 'z':0},{'x':0, 'y':0, 'z':0},{'x':0, 'y':0, 'z':0})


