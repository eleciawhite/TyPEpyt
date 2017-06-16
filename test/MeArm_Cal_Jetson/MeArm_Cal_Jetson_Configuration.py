
#pragma once 

PI = 3.1415

def DEGREES(rads):
  (((rads)*180.0)/(PI))
def RADIANS(degs):
  (((degs)*(PI))/(180.0))

SHOULDER_MAX_PWM =        160
SHOULDER_MIN_PWM =        30
SHOULDER_MAX_ANGLE_RAD =   RADIANS(13)
SHOULDER_MIN_ANGLE_RAD =  RADIANS(150)
SHOULDER_HOME_PWM     =   90 # in servo PWM counts
SHOULDER_SERVO_CHANNEL = 1


ELBOW_MAX_PWM       =  140
ELBOW_MIN_PWM       =  50
ELBOW_MAX_ANGLE_RAD =   RADIANS(112-90)
ELBOW_MIN_ANGLE_RAD =  RADIANS(30-90)
ELBOW_HOME_PWM      =   90     # in PWM counts
ELBOW_SERVO_CHANNEL = 2

CLAW_MAX_PWM        =  180
CLAW_MIN_PWM        =  0
CLAW_CLOSED_PWM     =  180
CLAW_OPEN_PWM       =  140
CLAW_HOME_PWM       =  170  # in PWM counts
CLAW_SERVO_CHANNEL  = 3
CLAW_MAX_ANGLE_RAD  = RADIANS(180)
CLAW_MIN_ANGLE_RAD  = RADIANS(0)

BASE_MAX_PWM       =   180
BASE_MIN_PWM       =   0
BASE_MAX_ANGLE_RAD =   RADIANS(-90)
BASE_MIN_ANGLE_RAD =   RADIANS(90)
BASE_HOME_PWM      =   90 # in PWM counts or as an angle (degrees), they are the same
BASE_SERVO_CHANNEL = 0

HOME_X =  0 
HOME_Y = 150
HOME_Z = 70        # empirically figured these out

L1=80  # Shoulder to elbow length (mm)
L2=80  # Elbow to wrist length (mm)
L3=68  # Length from wrist to hand PLUS base centre to shoulder (mm)

