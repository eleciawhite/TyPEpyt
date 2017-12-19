#!/usr/bin/env python
# License: Public Domain 

# Code to create a typing robot using a keyboard mapping
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# It also uses the Adafruit I2C and Adafruit_ADS1x15 libraries for reading current.
# Note that current is read in all servos, no single servo is monitored individually in this code.

# To use this code, start python and run these commands
# > execfile('ty.py')
# > ty.pressKey("h")
# > ty.pressString("hello")

import MeArm_Cal_Jetson_Configuration as cal
import math
import meArm
import TyAdc
import random
import time
import keyboardCalibration as keyCal

class TyContoller():

    def __init__(self):
        self.adc = TyAdc.TyAdc()
        self.arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
        self.arm.begin(pwmFrequency = cal.PWM_FREQUENCY) 
        time.sleep(0.5)
        self.checkBaselineCurrrent()
        self.gotoNice(keyCal.KEYBOARD_NEUTRAL)
        self.open(92)

    def __del__(self):
        self.adc.exit()
        del self.arm

    def loop(self):
        pos_goal = self.arm.getPos()

    def open(self, percent=75):
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
            return True
        else:
            print "done, timed out"
            return False

    def pressString(self, string):
        for c in string:
            self.pressKey(c)
            time.sleep(0.2)

    # 0. At neutral
    # 1. Go to place above the key, will take a time proportional to the distance
    # 2. Press key until current feedback says done
    # 3. Raise key
    # 4. Return key to neutral 
    def pressKey(self, char, delayDiv=300.0):
        debugPrint = 1
        keypos = list(keyCal.KEYPOS[char]) #make a copy of the location because we'll edit Z

        self.checkBaselineCurrrent() 

        [keyX, keyY, keyZ] = keypos
        [origX, origY, origZ] = self.arm.getPos()       # ideally this is the neutral position

        # 1. Goto to the XY location
        dist = self.arm.getDistance(keyX, keyY, origZ)
        self.arm.gotoPoint(x=keyX, y=keyY, z=origZ, debugPrint=debugPrint)		
        print "goto XY %s %s (%s, %s)" % (keypos, self.arm.getPos(), self.arm.isReachable(x=keyX, y=keyY, z=origZ), dist)
        self.waitUntilDone(minTime = dist/delayDiv, timeout = dist/delayDiv)

        # 2. Press key until feedback indicates it is done
        print "key"
        self.checkBaselineCurrrent() 
        self.arm.goDirectlyTo(x=keyX, y=keyY, z=keyZ, debugPrint=debugPrint)		
        done = self.waitForPushback(0.25)

        # 3. Raise key
        print "raise key"
        self.arm.gotoPoint(x=keyX, y=keyY, z=origZ-10, debugPrint=debugPrint)		

        # 4. Return key to neutral
        print "back to neutral"
        self.gotoNice(keyCal.KEYBOARD_NEUTRAL)



    def gotoPos(self, pos):
        [keyX, keyY, keyZ] = pos
        self.arm.gotoPoint(x=keyX, y=keyY, z=keyZ, debugPrint=1)		
        print(self.arm.getPos())

    def gotoNice(self, pos):
        [keyX, keyY, keyZ] = pos
        [curX, curY, curZ] = self.arm.getPos()
        if (curZ < keyZ): # go up and then down into position
            dist = self.arm.getDistance(keyX, keyY, z=keyZ+10)
            self.arm.gotoPoint(x=keyX, y=keyY, z=keyZ+10, debugPrint=0)

        self.arm.gotoPoint(x=keyX, y=keyY, z=keyZ, step=10, debugPrint=0)
        self.waitUntilDone(0.25)
        print(self.arm.getPos())		
   

if __name__ == '__main__':
    ty = TyContoller()




