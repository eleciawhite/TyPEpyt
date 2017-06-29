#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MeArmCalIK.py

import meArm

#import local config info
execfile('MeArm_Cal_Jetson_Configuration.py')

arm = meArm.meArm(
	BASE_MIN_PWM,     BASE_MAX_PWM,      BASE_MIN_ANGLE_RAD,     BASE_MAX_ANGLE_RAD,
	SHOULDER_MIN_PWM, SHOULDER_MAX_PWM,  SHOULDER_MIN_ANGLE_RAD, SHOULDER_MAX_ANGLE_RAD,
	ELBOW_MIN_PWM,    ELBOW_MAX_PWM,     ELBOW_MIN_ANGLE_RAD,    ELBOW_MAX_ANGLE_RAD,
	CLAW_MIN_PWM,     CLAW_MAX_PWM,      CLAW_MIN_ANGLE_RAD,     CLAW_MAX_ANGLE_RAD)
arm.begin()
	

