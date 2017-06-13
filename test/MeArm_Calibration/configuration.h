
#pragma once 

#define DEGREES(rads)  (((rads)*180.0)/(PI))
#define RADIANS(degs)  (((degs)*(PI))/(180.0))

#define SHOULDER_MAX_PWM         160
#define SHOULDER_MIN_PWM         30
#define SHOULDER_MAX_ANGLE_RAD   RADIANS(13)
#define SHOULDER_MIN_ANGLE_RAD   RADIANS(150)
#define SHOULDER_HOME_PWM        90 // in PWM counts
#define SHOULDER_PIN             10

#define ELBOW_MAX_PWM         140
#define ELBOW_MIN_PWM         50
#define ELBOW_MAX_ANGLE_RAD   RADIANS(112-90)
#define ELBOW_MIN_ANGLE_RAD   RADIANS(30-90)
#define ELBOW_HOME_PWM        90     // in PWM counts
#define ELBOW_PIN             9

#define CLAW_MAX_PWM          180
#define CLAW_MIN_PWM          0
#define CLAW_CLOSED_PWM       180
#define CLAW_OPEN_PWM         140
#define CLAW_HOME_PWM         170  // in PWM counts
#define CLAW_PIN              6
#define CLAW_MAX_ANGLE_RAD   RADIANS(180)
#define CLAW_MIN_ANGLE_RAD   RADIANS(0)

#define BASE_MAX_PWM          180
#define BASE_MIN_PWM          0
#define BASE_MAX_ANGLE_RAD    RADIANS(-90)
#define BASE_MIN_ANGLE_RAD    RADIANS(90)
#define BASE_HOME_PWM         90 // in PWM counts or as an angle (degrees), they are the same
#define BASE_PIN              11

#define HOME_X   0 
#define HOME_Y  150
#define HOME_Z  70        // empirically figured these out

static const float L1=80;  // Shoulder to elbow length (mm)
static const float L2=80;  // Elbow to wrist length (mm)
static const float L3=68;  // Length from wrist to hand PLUS base centre to shoulder (mm)

