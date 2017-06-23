# This uses the Adafruit library for controlling the PCA9685. 
# Author: Tony DiCola originally with extensive modifications from Elecia White
# License: Public Domain

from __future__ import division
import time
import math

# Import the PCA9685 module.
import Adafruit_PCA9685

#import local config info
execfile('MeArm_Cal_Jetson_Configuration.py')

# Initialise the PCA9685 using the default address (0x40) and the bus 
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Configure min and max servo pulse lengths
servo_min = 0
servo_max = 180
servo_freq = 47  # Frequency of the servo: usually 60, empircially determined with a scope to match Arduino 

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(servo_freq)


def check_min_max(minVal, maxVal, test):
    if (test < minVal):
	 test = minVal
         print "min %d" % (minVal)		
    if (test > maxVal):
	 test = maxVal
         print "min %d" % (maxVal)		
    return test

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse = check_min_max(servo_min, servo_max, pulse)
    pwm_val = 111 + pulse*2   # empirically determined with a scope to match Arduino 
    pwm.set_pwm(channel, 0, pwm_val)


def b(pulse):
    pulse = check_min_max(BASE_MIN_PWM, BASE_MAX_PWM, pulse)
    set_servo_pulse(BASE_SERVO_CHANNEL, pulse)

def s(pulse):
    pulse = check_min_max(SHOULDER_MIN_PWM, SHOULDER_MAX_PWM, pulse)
    set_servo_pulse(SHOULDER_SERVO_CHANNEL, pulse)

def e(pulse):
    pulse = check_min_max(ELBOW_MIN_PWM, ELBOW_MAX_PWM, pulse)
    set_servo_pulse(ELBOW_SERVO_CHANNEL, pulse)

def c(pulse):
    pulse = check_min_max(CLAW_MIN_PWM, CLAW_MAX_PWM, pulse)
    set_servo_pulse(CLAW_SERVO_CHANNEL, pulse)

def setJointAngles(base, shoulder, elbow, claw):
    b(int(math.degrees(base)))
    s(int(math.degrees(shoulder)))
    e(int(math.degrees(elbow)))
    c(int(math.degrees(claw)))

def home():
    b(BASE_HOME_PWM)
    s(SHOULDER_HOME_PWM)
    e(ELBOW_HOME_PWM)
    c(CLAW_HOME_PWM)

def off():
    pwm.set_pwm(BASE_SERVO_CHANNEL, 0, 0)
    pwm.set_pwm(SHOULDER_SERVO_CHANNEL, 0, 0)
    pwm.set_pwm(ELBOW_SERVO_CHANNEL, 0, 0)
    pwm.set_pwm(CLAW_SERVO_CHANNEL, 0, 0)



