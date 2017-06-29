#!/usr/bin/env python
# Code to calibrate the meArm by direct driving the motors
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# License: Public Domain 


from __future__ import division
import time
import math

# Import the PCA9685 module.
import Adafruit_PWM_Servo_Driver 

#import local config info
execfile('MeArm_Cal_Jetson_Configuration.py')

# Initialise the PCA9685 using the default address (0x40) and the bus 
pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)

# Set frequency to 60hz, good for servos.
pwm.setPWMFreq(PWM_FREQUENCY)


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
    pwm_val = 150 + int(pulse*450.0/180.0) # magic incantation to make the timing work
    pwm.setPWM(channel, 0, pwm_val)


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



