# meArm.py - York Hack Space May 2014
# A motion control library for Phenoptix meArm using Adafruit 16-channel PWM servo driver

from Adafruit_PWM_Servo_Driver import PWM
import kinematics
import time
from math import pi
import math

execfile('MeArm_Cal_Jetson_Configuration.py')

class meArm():
    def __init__(self, sweepMinBase = 145, sweepMaxBase = 49, angleMinBase = -pi/4, angleMaxBase = pi/4,
    			 sweepMinShoulder = 118, sweepMaxShoulder = 22, angleMinShoulder = pi/4, angleMaxShoulder = 3*pi/4,
    			 sweepMinElbow = 144, sweepMaxElbow = 36, angleMinElbow = pi/4, angleMaxElbow = -pi/4,
    			 sweepMinGripper = 75, sweepMaxGripper = 115, angleMinGripper = pi/2, angleMaxGripper = 0):
        """Constructor for meArm - can use as default arm=meArm(), or supply calibration data for servos."""
    	self.servoInfo = {}
    	self.servoInfo["base"] = self.setupServo(sweepMinBase, sweepMaxBase, angleMinBase, angleMaxBase)
    	self.servoInfo["shoulder"] = self.setupServo(sweepMinShoulder, sweepMaxShoulder, angleMinShoulder, angleMaxShoulder)
    	self.servoInfo["elbow"] = self.setupServo(sweepMinElbow, sweepMaxElbow, angleMinElbow, angleMaxElbow)
    	self.servoInfo["gripper"] = self.setupServo(sweepMinGripper, sweepMaxGripper, angleMinGripper, angleMaxGripper)
    	self.minGripper = angleMinGripper
        self.maxGripper = angleMaxGripper
    def __del__(self):
        # power off the motors
    	self.pwm.setPWM(self.base, 0, 0)
    	self.pwm.setPWM(self.shoulder, 0, 0)
    	self.pwm.setPWM(self.elbow, 0, 0)
    	self.pwm.setPWM(self.gripper, 0, 0)
	 
    # Adafruit servo driver has four 'blocks' of four servo connectors, 0, 1, 2 or 3.
    def begin(self, pwmFrequency = 60, block = 0, address = 0x40, busnum =1):
        """Call begin() before any other meArm calls.  Optional parameters to select a different block of servo connectors or different I2C address."""
        self.pwm = PWM(address, busnum) # Address of Adafruit PWM servo driver
    	self.base = block * 4
    	self.shoulder = block * 4 + 1
    	self.elbow = block * 4 + 2
    	self.gripper = block * 4 + 3
    	self.pwm.setPWMFreq(pwmFrequency)
    	self.closeGripper()
        self.home()

    def home(self):
    	self.goDirectlyTo(HOME_X, HOME_Y, HOME_Z)
    	
    def setupServo(self, n_min, n_max, a_min, a_max):
        """Calculate servo calibration record to place in self.servoInfo"""
        rec = {}
        n_range = n_max - n_min
        a_range = a_max - a_min
        if a_range == 0: return
        gain = n_range / a_range
        zero = n_min - gain * a_min
        rec["gain"] = gain
        rec["zero"] = zero
        rec["min"] = n_min
        rec["max"] = n_max
        rec["a_min"] = a_min
        rec["a_max"] = a_max
        return rec
    
    def angle2pwm(self, servo, angle):
        """Work out pulse length to use to achieve a given requested angle taking into account stored calibration data"""
        n_max = self.servoInfo[servo]["max"]
        n_min = self.servoInfo[servo]["min"]
        ret = int(0.5 + (self.servoInfo[servo]["zero"] + self.servoInfo[servo]["gain"] * angle))
        if (ret > n_max) : 
            print " x %d (%d -> %d)" % (math.degrees(angle), ret, n_max)
            ret = n_max
            angle = self.servoInfo[servo]["a_max"]
        if (ret < n_min) : 
            print " n %d (%d -> %d)" % (math.degrees(angle), ret, n_min)
            ret = n_min
            angle = self.servoInfo[servo]["a_min"]
        return (angle, ret)

    def setPwm(self, channel, pwm):
        # convert to local servo counts
        pwm = 150 + int(pwm*450.0/180.0)
        self.pwm.setPWM(channel, 0, pwm)
    	
    def goDirectlyTo(self, x, y, z, debugPrint=1):
        """Set servo angles so as to place the gripper at a given Cartesian point as quickly as possible, without caring what path it takes to get there"""
        angles = [0,0,0]
        if kinematics.solve(x, y, z, angles):
            radBase = angles[0]
            radShoulder = angles[1]
            radElbow = angles[2]
            radBase, pwm_val = self.angle2pwm("base", radBase)
            self.setPwm(self.base, pwm_val)

            radShoulder, pwm_val = self.angle2pwm("shoulder", radShoulder)
            self.setPwm(self.shoulder, pwm_val)

            radElbow, pwm_val = self.angle2pwm("elbow", radElbow)
            self.setPwm(self.elbow, pwm_val)

            self.x, self.y, self.z = kinematics.unsolve(radBase, radShoulder, radElbow)
            if (debugPrint):
                print "goto %s (actual %s ; ang bse %s ) " % ([int(x),int(y),int(z)], 
                                                        [int(self.x), int(self.y), int(self.z)],
                                                        [int(math.degrees(radBase)), int(math.degrees(radShoulder)), 
                                                            int(math.degrees(radElbow))])
            else: 
                print "No solution for %s" % [int(x),int(y),int(z)]
    
    def gotoPoint(self, x, y, z, debugPrint=1):
        """Travel in a straight line from current position to a requested position"""
    	x0 = self.x
    	y0 = self.y
    	z0 = self.z
    	dist = kinematics.distance(x0, y0, z0, x, y, z)
    	step = 10
    	i = 0
    	while i < dist:
    		self.goDirectlyTo(x0 + (x - x0) * i / dist, y0 + (y - y0) * i / dist, z0 + (z - z0) * i / dist, debugPrint)
    		time.sleep(0.03)
    		i += step
    	self.goDirectlyTo(x, y, z, debugPrint)
    	time.sleep(0.05)

    def getDistance(self, x, y, z):
    	dist = kinematics.distance(self.x, self.y, self.z, x, y, z)
    	return dist

    def getDistanceBetween(self, x, y, z, x1, y1, z1):
    	dist = kinematics.distance(x1, y1, z1, x, y, z)
    	return dist

    def gotoPointMaxDist(self, x, y, z, maxDist):
        """Travel in a straight line from current position to a requested position"""
        x0 = self.x
        y0 = self.y
        z0 = self.z
        dist = kinematics.distance(x0, y0, z0, x, y, z)
        if dist < maxDist: maxDist = dist
        if maxDist == 0: maxDist = dist
        self.goDirectlyTo(x0 + (x - x0) * maxDist / dist, y0 + (y - y0) * maxDist / dist, z0 + (z - z0) * maxDist / dist)


    def openGripper(self):
        """Open the gripper, dropping whatever is being carried"""
        _, pwm = self.angle2pwm("gripper", CLAW_OPEN_RAD)
    	self.setPwm(self.gripper, pwm)
    	
    def closeGripper(self):
        """Close the gripper, grabbing onto anything that might be there"""
        _, pwm = self.angle2pwm("gripper", CLAW_CLOSED_RAD)
    	self.setPwm(self.gripper,pwm)

    def gripperClosePercent(self, percentOpen):
        """Close gripper by some percent, 100 is tightly closed and 0 is fully open"""
        clawDistance = self.maxGripper - self.minGripper
        clawAngle = clawDistance*(percentOpen/100.0) + self.minGripper
        _, pwm = self.angle2pwm("gripper", clawAngle)
    	self.setPwm(self.gripper, pwm)
    
    def isReachable(self, x, y, z):
        """Returns True if the point is (theoretically) reachable """
        angles = [0,0,0]
        if kinematics.solve(x, y, z, angles) != None:
            radBase, _ = self.angle2pwm("base", angles[0])
            if radBase == angles[0]:
                radShoulder, _ = self.angle2pwm("shoulder", angles[1])
                if radShoulder == angles[1]:
                    radElbow, _ = self.angle2pwm("elbow", angles[2])
                    if radElbow == angles[2]:
                        return True
        print 'Not reachable: %d %d %d'%(x,y,z)
        return False
    
    def getPos(self):
        """Returns the current position of the gripper"""
    	return [self.x, self.y, self.z]
