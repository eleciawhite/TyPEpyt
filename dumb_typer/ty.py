#!/usr/bin/env python
# Code to calibrate the meArm by direct driving the motors
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# License: Public Domain 

import MeArm_Cal_Jetson_Configuration as cal
import math
import meArm
import TyAdc
import random
import time
import keyboardCalibration as keyCal

VIDEO_CHANNEL = 1
Y_MIDDLE_ZONE = 100
GRIPPER_DELAY_DEFAULT = 30

class TyContoller():

    def __init__(self):
        self.adc = TyAdc.TyAdc()
        self.arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
        self.arm.begin(pwmFrequency = cal.PWM_FREQUENCY)     
        self.open(92)
        self.checkBaselineCurrrent()
        self.gotoNice(keyCal.KEYBOARD_NEUTRAL)

    def __del__(self):
        self.adc.exit()
        del self.arm

    def loop(self):
        pos_goal = self.arm.getPos()

    def open(self, percent=75):
        self.arm.gripperClosePercent(percent)

    def close(self, percent=89):
        self.arm.gripperClosePercent(percent)

    def checkBaselineCurrrent(self):
        self.currentCheckTime = time.time()
        self.baselineCurrent = self.adc.magnitude()

    def isMotionComplete(self):
        okMultiplier = 3 # can go over 10% and still considered done
        adc = self.adc.magnitude();
        if (adc < self.baselineCurrent):
            self.baselineCurrent = adc; # use the lowest
        print "%s: base %s mag %s" % (time.time(), self.baselineCurrent, adc)
        if (adc < self.baselineCurrent * okMultiplier):
            return True
        if (adc < 150):
            return True
        return False

    def waitUntilDone(self, minTime = 0.1, timeout=0.5):
        time.sleep(minTime)
        timeStarted = time.time()
        dt = time.time() - timeStarted
        while (not self.isMotionComplete() and dt < timeout): 
            dt = time.time() - timeStarted
            time.sleep(0.05)
        if self.isMotionComplete():
            self.checkBaselineCurrrent()
            print "done, motion finished"
        else:
            print "done, timed out"

    def waitForPushback(self, timeout):
        pushbackCurrent = 25
        timeStarted = time.time()
        dt = time.time() - timeStarted 
        adc = self.adc.magnitude()
        print "%s: pushback %s mag %s (%s)" % (time.time(), self.baselineCurrent, adc, (adc - self.baselineCurrent))  
        while ((abs(adc - self.baselineCurrent) < pushbackCurrent) and dt < timeout):
            adc = self.adc.magnitude()
            dt = time.time() - timeStarted
            time.sleep(0.05)
            print "%s: pushback %s mag %s (%s)" % (time.time(), self.baselineCurrent, adc, (adc - self.baselineCurrent))  
        if abs(adc - self.baselineCurrent) >= pushbackCurrent:
            print "done, pushed"
        else:
            print "done, timed out"


    def pressString(self, string):
        for c in string:
            self.pressKey(c)

    def pressKey(self, char):
        keypos = list(keyCal.KEYPOS[char]) #make a copy 

        self.checkBaselineCurrrent()
        dist = self.gotoXY(keypos)
        print dist
#        self.waitUntilDone(minTime = dist/300.0, timeout = 0.5)
        self.waitUntilDone(minTime = 0.1, timeout = dist/300.0)
        

        self.checkBaselineCurrrent()
        self.gotoPos(keyCal.KEYPOS[char])
        self.waitForPushback(1.0)
        print "gotoNicely"
        self.gotoNice(keyCal.KEYBOARD_NEUTRAL)

    def gotoXY(self, pos):
        [goalX, goalY, goalZ] = pos
        [curX, curY, curZ] = self.arm.getPos()
        
        dist = self.arm.getDistance(goalX, goalY, curZ)
        self.arm.goDirectlyTo(x=goalX, y=goalY, z=curZ, debugPrint=1)		
        print "goto XY %s %s %s" % (pos, self.arm.getPos(), self.arm.isReachable(x=goalX, y=goalY, z=curZ))
        return dist

    def gotoXY2(self, pos):
        [goalX, goalY, goalZ] = pos
        [curX, curY, curZ] = self.arm.getPos()
        dist = self.arm.getDistance(goalX, goalY, curZ)
        self.arm.goDirectlyTo(x=goalX, y=goalY, z=curZ, debugPrint=1)		
        print "goto XY %s %s %s" % (pos, self.arm.getPos(), self.arm.isReachable(x=goalX, y=goalY, z=curZ))
        return dist

    def gotoPos(self, pos):
        [goalX, goalY, goalZ] = pos
        self.arm.goDirectlyTo(x=goalX, y=goalY, z=goalZ, debugPrint=1)		
        print(self.arm.getPos())
    def gotoNice(self, pos):
        [goalX, goalY, goalZ] = pos
        [curX, curY, curZ] = self.arm.getPos()
        if (curZ < goalZ): # go up and then down into position
            dist = self.arm.getDistance(goalX, goalY, z=goalZ+25)
            self.arm.goDirectlyTo(x=goalX, y=goalY, z=goalZ+25, debugPrint=0)
            self.waitUntilDone(minTime = dist/1000.0, timeout = 0.5)

        self.arm.goDirectlyTo(x=goalX, y=goalY, z=goalZ, debugPrint=0)
        self.waitUntilDone(1.0)
        print(self.arm.getPos())		
    


if __name__ == '__main__':
    ty = TyContoller()
#    ty.loop()




