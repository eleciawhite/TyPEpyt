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
import keyboardCalibration as KeyCal
import TyKey as key
import cv2
import numpy as np
import sphinx as sphinx

class TyContoller():

    def __init__(self, cam):
        self.adc = TyAdc.TyAdc()
        self.arm = meArm.meArm(
	        cal.BASE_MIN_PWM,     cal.BASE_MAX_PWM,      cal.BASE_MIN_ANGLE_RAD,     cal.BASE_MAX_ANGLE_RAD,
	        cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM,  cal.SHOULDER_MIN_ANGLE_RAD, cal.SHOULDER_MAX_ANGLE_RAD,
	        cal.ELBOW_MIN_PWM,    cal.ELBOW_MAX_PWM,     cal.ELBOW_MIN_ANGLE_RAD,    cal.ELBOW_MAX_ANGLE_RAD,
	        cal.CLAW_MIN_PWM,     cal.CLAW_MAX_PWM,      cal.CLAW_MIN_ANGLE_RAD,     cal.CLAW_MAX_ANGLE_RAD)
        self.arm.begin(pwmFrequency = cal.PWM_FREQUENCY) 
        time.sleep(0.5)
        self.open(92)
        self.cam = cam
        self.keymap = key.KeyMap(cam)
        self.speech = sphinx.SpeechDetector()

    def __del__(self):
        self.adc.stop()
        del self.arm

    def start(self):
        self.checkBaselineCurrrent()
        self.adc.stop() # adc fights with display
        self.gotoArmPos(KeyCal.KEYBOARD_NEUTRAL)
        self.open(92)
        print "Check that the camera covers the main part of the keyboard, then click anywhere."
        print "Next, verify the mapping looks good. Rerun if it doesn't."
        frame, self.keyboardOutline = self.keymap.kvm(debugDraw = True)
#        self.adc.start()

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

    def freshCameraRead(self):
        for i in range(0,10):
            ret, frame = self.cam.read() # need to do this several times to flush buffer
        return frame

    def pressKey(self, char, k=0.25, showDebug=False):
        keyPos = self.keymap.charToKeyPos(char)
        goalCamPos = self.keymap.transformKeyboardToCameraPos(char)
        goalArmPos = self.transformCamPosToArmPos(goalCamPos)
        if showDebug:
            print "key pos at ", keyPos, " which is ", goalCamPos, " on the camera, arm pos ", goalArmPos

        armPosWithNeutralZ = np.append(goalArmPos, KeyCal.KEYBOARD_NEUTRAL[2])
        self.gotoArmPos(armPosWithNeutralZ)
        frame = self.freshCameraRead()
        clawCamPos = self.keymap.locateClaw(frame)
        if showDebug:
            print "Claw located at ", clawCamPos

        if clawCamPos is not None:
            clawCamPos = np.array(clawCamPos, dtype='float32')
            diffCamPos = goalCamPos - clawCamPos    
            goalArmPos = self.transformCamPosToArmPos(goalCamPos+(k*diffCamPos))
            if showDebug:
                print "diffCam ", diffCamPos," new  goalArmPos ", goalArmPos


        armPosWithNeutralZ = np.append(goalArmPos, KeyCal.KEYBOARD_NEUTRAL[2])
        self.gotoArmPos(armPosWithNeutralZ)
        armPosDown = np.append(goalArmPos, 0)
        self.gotoArmPos(armPosDown)
        done = self.waitForPushback(0.25)

        self.gotoNice(armPosWithNeutralZ)

        

    def gotoArmPos(self, pos, step = 10):
        [x, y, z] = pos
        self.arm.gotoPoint(x=x, y=y, z=z, step = step, debugPrint=0)		
        print(self.arm.getPos())

    def cal(self, neutralZ = 50, step = 10): # calibrate the camera vs the servo
        armCalPos = [[-110, 165],  
                    [ 90, 165],   
                    [100, 100],    
                    [-110, 110]] 
        clawPos = []
        camPos = []
        self.adc.stop() # adc fights with display
        for p in armCalPos:            
            self.gotoNice([p[0], p[1], neutralZ]) 
            print "Click on the blue dot in the camera image."
            self.keymap.waitForClick()
            claw = self.keymap.locateClaw()
            while claw is None:
                print "Retry that one."
                self.keymap.waitForClick()
                claw = self.keymap.locateClaw(debugDraw = True)
            else:
                print "lenclaw",len(claw)
            clawPos.append(claw)
            camPos.append(self.keymap.clickPoint)
        self.camToArmM = cv2.getPerspectiveTransform(np.array(clawPos, dtype="float32"),
                                                        np.array(armCalPos, dtype="float32"), )
        self.camToArmMinv = np.linalg.inv(self.camToArmM)
#        self.adc.start()
        self.gotoArmPos(KeyCal.KEYBOARD_NEUTRAL)
        print "Camera positions: ", camPos
        print "Detected claw positions: ", clawPos
        return self.camToArmM

    def transformArmPosToCamPos(self, pos): 
        a = np.array([[[pos[0],pos[1]]]], dtype='float32')
        return cv2.perspectiveTransform(a,self.camToArmMinv)[0][0]

    def transformCamPosToArmPos(self, pos): 
        a = np.array([[[pos[0],pos[1]]]], dtype='float32')
        return cv2.perspectiveTransform(a,self.camToArmM)[0][0]


    def clawKey(self, frame = None):  
        claw_loc = self.keymap.locateClaw(frame=frame)
        key_pos = self.keymap.transformCameraPosToKeyboard(claw_loc)
        key = self.keymap.keyPosToChar(key_pos)
        print "claw at ", claw_loc, " which is ", key_pos, " on the keyboard, character ", key
        return key

    def armPosToKey(self, arm_pos):  
        cam_pos = self.transformArmPosToCamPos(arm_pos)
        key_pos = self.keymap.transformCameraPosToKeyboard(cam_pos)
        key = self.keymap.keyPosToChar(key_pos)
        print "cam pos at ", cam_pos, " which is ", key_pos, " on the keyboard, character ", key
        return key


    def gotoNice(self, pos):
        [keyX, keyY, keyZ] = pos
        [curX, curY, curZ] = self.arm.getPos()
        if (curZ <= keyZ): # go up and then down into position
            self.arm.gotoPoint(x=keyX, y=keyY, z=keyZ+15, debugPrint=0)

        self.arm.gotoPoint(x=keyX, y=keyY, z=keyZ, step=10, debugPrint=0)
        self.waitUntilDone(0.25)
        print(self.arm.getPos())		
   
    def dictate(self):
        words = self.speech.run()
        for w in words:
            ty.pressString(w)
            ty.pressString(" ")
        print "You said: ",
        for w in words:
            print w, " ",
        print
        
if __name__ == '__main__':
    try: cam
    except NameError: 
        videoChannel = 1
        cam = cv2.VideoCapture(videoChannel)
    ty = TyContoller(cam)




