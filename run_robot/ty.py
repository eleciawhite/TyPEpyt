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

VIDEO_CHANNEL = 2

arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
arm.begin(pwmFrequency = cal.PWM_FREQUENCY)
pos = TyPositionGoal.TyPositionGoal(VIDEO_CHANNEL, debugging = 1)

def buttwiggle():
    x = 0
    y = int(random.uniform(70,80))
    z = int(random.uniform(3, 8))
    d = arm.getDistance(x,y,z)
    arm.gotoPointMaxDist(x,y,z,d/5.0)

def loop():
    badCount = 0
    while (True):
        p = pos.getPositionGoal()
        if p == None:
            print 'no dest'
            if badCount == 0 :          
                buttwiggle()
            else :
                arm.gotoPointMaxDist(rx,ry,rz,d/3.0)
                badCount -= 1
                
        else:
            badCount = 3
            rx = p[0]
            rz = p[1]
            ry = 100
            d = arm.getDistance(rx,ry,rz)
            arm.gotoPointMaxDist(rx,ry,rz,d/3.0)
        time.sleep(0.003)
                
def middleDistanceY(x, y, z):
    y0 = y
    d = arm.getDistanceBetween(x, y, z, 0, 100, 20)
    d0 = d
    increment = -20
    if d > 100 and y > 0:
        y += increment;
        d = arm.getDistanceBetween(x, y, z, 0, 100, 20)
        if (d > d0) : y = y0 - increment
        if y < 0 : y = 0
        print 'd- %d y %d'% (d, y)
    if d < 20:
        y += increment;
        d = arm.getDistanceBetween(x, y, z, 0, 100, 20)
        if (d < d0) : y = y0 - increment
        print 'd+ %d y %d'% (d, y)
    return y
    
def calStep(x, y, z, x_adder, z_adder, resultGoal):
    reachable = arm.isReachable(x, y, z)
    if reachable == True:    
        arm.gotoPoint(x, y, z)
        result = pos.getCalibrationPoint(x, z)
    while reachable == True and result == resultGoal:
        x += x_adder
        z += z_adder
        y = middleDistanceY(x, y, z)
        reachable = arm.isReachable(x, y, z)
        if reachable == True:
            arm.gotoPoint(x, y, z) 
            result = pos.getCalibrationPoint(x, z)
    return x, y, z

def cal():
    # move robot to four corners and call the calibration function
    pos.startCalibration()

    # right, lower
    x = 0; y = 100; z = 80  # near center
    x, y, z = calStep(x, y, z, 30, 0, True) # push out of range
    x, y, z = calStep(x, y, z, -10, 0, False) # bring into range
    x, y, z = calStep(x, y, z, 0, -10, True)  # push out of range
    rightx = x

    print '----------------------------------'

    # left, lower
    x = 0; y = 100; z = 80

    x, y, z = calStep(x, y, z, -30, 0, True) # push out of range
    x, y, z = calStep(x, y, z, 10, 0, False) # bring into range
    x, y, z = calStep(x, y, z, 0, -10, True) # push out of range
    leftx = x

    print '************************************'

    # center and look for upper
    x = int((rightx + leftx)/2.0)     
    y = 100; z = 80
    print x
    x, y, z = calStep(x, y, z, 0, 10, True) # push out of range

    print 'Cal complete'
        
    

class TyContoller():

    def __init__(self):
        self.arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
        self.arm.begin(pwmFrequency = cal.PWM_FREQUENCY)
        
        self.pos = TyPositionGoal.TyPositionGoal(debugging = 1)

#    def loop(self):


#if __name__ == '__main__':
#    ty = TyContoller()
#    ty.loop()


#def pub():
#    jc.joint_state.header.stamp = rospy.Time.now()
#    jc.publisher.publish(jc.joint_state)


