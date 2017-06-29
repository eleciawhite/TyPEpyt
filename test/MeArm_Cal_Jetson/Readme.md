
MeArm calibration program using Adafruit's Adafruit_PCA9685 python library.

Supported commands for direct control of servos
  * ```e(<pwm>) ```	Sets the elbow (right) servo to the given level.
  * ```s(<pwm>) ```     Sets the shoulder (left) servo to the given level.
  * ```b(<pwm>) ```	Sets the base (middle) to the given PWM.
  * ```c(<pwm>) ```	Sets the claw servo to the given PWM.
  * ```home() ```       Homes the servos to all 90 pwm except the claw which goes to 170 for mostly closed.
  *```off() ```          Sets the PWM channels off, freeing 
	
	
Note that for each of the servo commands, the value is checked against definitions in the configuration file.
