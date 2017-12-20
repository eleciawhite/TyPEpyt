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

VIDEO_CHANNEL = 1
Y_MIDDLE_ZONE = 100

class TyContoller():

    def __init__(self):
        self.arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
        self.arm.begin(pwmFrequency = cal.PWM_FREQUENCY)     
        self.pos = TyPositionGoal.TyPositionGoal(VIDEO_CHANNEL, debugging = 1)

    def __del__(self):
        del self.pos
        del self.arm

    # The butt wiggles when there is no laser to chase.
    # This is an area where there are multiple joint angle solutions to the 
    # inverse kinematic math for the goal position. The gripper can stay mostly
    # where it is while the joints move around, leading to a butt-wiggle like motion.
    def buttwiggle(self): 
        x = 0
        y = int(random.uniform(70,80))
        z = int(random.uniform(3, 8))
        d = self.arm.getDistance(x,y,z)
        self.arm.gotoPointMaxDist(x,y,z,d/5.0)
        self.arm.gripperClosePercent(95)


    # When the laser is neaby, the gipper snaps, until then, it opens 
    def gripperSnap(self, distance, gripperPercent):
        if distance < 15:
            if gripperPercent < 70:  #time to snap
                gripperPercent = 95
            else:
                gripperPercent -= 1
        else:
            gripperPercent = 85
        self.arm.gripperClosePercent(gripperPercent)
        print distance
        return gripperPercent

    def cat(self):
        currentGripperPercent = 95
        ry = Y_MIDDLE_ZONE
        while (True):
            p = self.pos.getPositionGoal()
            if p == None:
                print 'no dest'
                self.buttwiggle()
                ry = Y_MIDDLE_ZONE
            else:
                rx = p[0]
                rz = p[1]
                ry = self.middleDistanceY(rx, ry, rz) # keep y in the good range for these x,z values
                d = self.arm.getDistance(rx, ry, rz)
                print 'want [%d, %d, %d]'%(rx, ry, rz)
                self.arm.gotoPointMaxDist(rx, ry, rz, d/3.0) # go partway there
                currentGripperPercent = self.gripperSnap(d, currentGripperPercent)
#            time.sleep(0.003)
                    
    def moveJoint(self): # move base to show difference between motion
        self.arm.gotoPoint(-120, 75, 70) # base angle = 60 based on debug out
        baseAngle = -60
        while baseAngle <= 60:
            _, pwm_val = self.arm.angle2pwm("base", math.radians(baseAngle))
            self.arm.setPwm(self.arm.base, pwm_val)
            baseAngle += 5
            time.sleep(0.03)
        time.sleep(1.0)
        while baseAngle >= -60:
            _, pwm_val = self.arm.angle2pwm("base", math.radians(baseAngle))
            self.arm.setPwm(self.arm.base, pwm_val)
            baseAngle -= 5
            time.sleep(0.03)

    def moveKinematic(self):
        self.arm.gotoPoint(120, 75, 70)
        time.sleep(1.0)
        self.arm.gotoPoint(-120, 75, 70)

    def middleDistanceY(self, x, y, z):
        midX = 0 ; midY = 85; midZ = 10
        y0 = y
        d = self.arm.getDistanceBetween(x, y, z, midX, midY, midZ)
        d0 = d
        print 'y d %d' % d
        increment = -20
        if d > 120:
            y += increment;
            d = self.arm.getDistanceBetween(x, y, z, midX, midY, midZ)
            if (d > d0) : y = y0 - increment
            d = self.arm.getDistanceBetween(x, y, z, midX, midY, midZ)
            print 'd- %d y %d'% (d, y)
        if d < 80:
            y -= increment;
            d = self.arm.getDistanceBetween(x, y, z, midX, midY, midZ)
            if (d < d0) : y = y0 + increment
            d = self.arm.getDistanceBetween(x, y, z, midX, midY, midZ)
            print 'd+ %d y %d'% (d, y)
        if y < 0 : y = 0
        return y
        
    def calStep(self, x, y, z, x_adder, z_adder, resultGoal):
        reachable = self.arm.isReachable(x, y, z)
        if reachable == True:    
            self.arm.gotoPoint(x, y, z)
            result = self.pos.getCalibrationPoint(x, z)
        while reachable == True and result == resultGoal:
            x += x_adder
            z += z_adder
            y = self.middleDistanceY(x, y, z)
            reachable = self.arm.isReachable(x, y, z)
            if reachable == True:
                self.arm.gotoPoint(x, y, z) 
                result = self.pos.getCalibrationPoint(x, z)
        return x, y, z

    def cal(self):
        # move robot to four corners and call the calibration function
        self.pos.startCalibration()

        # right, lower
        x = 0; y = 150; z = 80  # near center
        x, y, z = self.calStep(x, y, z, 30, 0, True) # push out of range
        x, y, z = self.calStep(x, y, z, -10, 0, False) # bring into range
        rightx = x

        print '---------------------------------- %d %d'%(x,z)

        # left, lower
        x = 0; y = 150; z = 80
        x, y, z = self.calStep(x, y, z, -30, 0, True) # push out of range
        x, y, z = self.calStep(x, y, z, 10, 0, False) # bring into range
        leftx = x

        print '************************************ %d %d'%(x,z)

        # center and look for upper
        x = int((rightx + leftx)/2.0)     
        y = 150; z = 80
        print x
        x, y, z = self.calStep(x, y, z, 0, 5, True) # push out of range
        y = 150; z = 80
        x, y, z = self.calStep(x, y, z, 0, -10, True)  # push out of range

        print 'Cal complete  %d %d'%(x,z)
            
    


if __name__ == '__main__':
    ty = TyContoller()
#    ty.loop()




