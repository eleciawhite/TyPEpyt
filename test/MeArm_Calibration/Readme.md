
MeArm calibration program with a real command line. 

This uses the Arduino-CommandLine library. Get it at:
https://github.com/basilfx/Arduino-CommandLine
Download the zip linked to in their read me or clone the repository to Arduino/libraries/CommandLine.
Restart Arduino IDE, then load this project.

This also depends on code originally from 
https://github.com/mimeindustries/mearm-brains-arduino
In particular, I used BobStonesArduinoCode, an inverse kinematics subsystem.  However, I 
modified it so that the system configuration values are in a header file and respected the servo limits.
The files from the mearm-brains-arduino repo are:
  * fk.cpp, fk.h (these are unused anyway)
  * ik.cpp, ik.h (the source file is modified to use the lengths from configuration.h)
  * meArm.cpp, meArm.h (the source file is modified to use the claw valus from config and to respect the servo limits)

Supported commands when the MeArm_Calibration.ino **IK = 0** (direct control of servos)
  * ```e <pwm>```	*Sets the elbow (right) servo to the given level*
  * ```s <pwm>``` 	*Sets the shoulder (left) servo to the given level*
  * ```b <pwm>```	*Sets the base (middle) to the given PWM* 
  * ```c <pwm>```	*Sets the claw servo to the given PWM*
  * ```home```		*Homes the servos to all 90 pwm except the claw which goes to 170 for mostly closed.*
	
Supported commands when the MeArm_Calibration.ino **IK = 1** (MeArm arm controls the servos)
  * ```c <open>```		*Sets the claw to open (1) or closed (0)*
  * ```home```			*Homes the servos to the empircially determined home position*
  * ```go <x> <y> <z>``` 	*Uses the values in configuration.h to go to a desired position along a linear path from where you are. *
  * ```gd <x> <y> <z>```	*Go directly to the position given, no steps. This can be tough on the motors.*

For my arm, 0 150 70 is a good triplet, 0 200 -40 is extended and low, 0 175 105 is extended and high.
For a neat visual of travelling along a linear path, go from 0 150 70 to 150 0 70 and note that it doesn't 
turn only the base, that would create an arc, instead it moves the claw in a linear fashion.

	
Note that for each of the servo commands, the value is checked against #defines at the top of the file (such as SHOULDER_MAX) 
