#!/usr/bin/env python
# Code to calibrate the meArm by direct driving the motors
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# License: Public Domain 

import MeArm_Cal_Jetson_Configuration as cal
import math
import meArm
import TyPositionGoal
import random
import time

ROBOT_X_MIN = -120
ROBOT_X_MAX = 120
CAMERA_X_MIN = 150
CAMERA_X_MAX = 605
robotz_min = 50
robotz_max = 100


def tf_stretch(amin, amax, bmin, bmax, aval):
    atotal = amax - amin
    btotal = bmax - bmin
    factor = (aval - amin) / float(atotal)
    bval =  (factor * btotal) + bmin
    return int(bval)

def tf_cam_to_robot(x, y):
    outx = tf_stretch(CAMERA_X_MIN, CAMERA_X_MAX, ROBOT_X_MIN, ROBOT_X_MAX, x)
    outy = 70
    return (outx, outy)

arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
arm.begin(pwmFrequency = cal.PWM_FREQUENCY)
pos = TyPositionGoal.TyPositionGoal(debugging = 1)

def buttwiggle():
    x = 0
    y = int(random.uniform(70,80))
    z = int(random.uniform(3, 8))
    d = arm.getDistance(x,y,z)
    arm.gotoPointMaxDist(x,y,z,d/10.0)

def loop():
    while (True):
        cx, cy = pos.getPositionGoal()
        if cx == -1:
            print 'no dest'
            buttwiggle()
            time.sleep(random.uniform(0.005, 0.05))
        else:
            rx, rz = tf_cam_to_robot(cx, cy)
            ry = 150
            d = arm.getDistance(rx,ry,rz)
            arm.gotoPointMaxDist(rx,ry,rz,d/3.0)
            time.sleep(0.01)
                

class TyContoller():

    def __init__(self):
        self.arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
        self.arm.begin(pwmFrequency = cal.PWM_FREQUENCY)
        
        self.pos = TyPositionGoal.TyPositionGoal(debugging = 1)

    def loop(self):


if __name__ == '__main__':
    ty = TyContoller()
    ty.loop()


#def pub():
#    jc.joint_state.header.stamp = rospy.Time.now()
#    jc.publisher.publish(jc.joint_state)


