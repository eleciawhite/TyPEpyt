
MeArm calibration program with a real command line. 

This uses the Arduino-CommandLine library. Get it at:
https://github.com/basilfx/Arduino-CommandLine
Download the zip linked to in their read me or clone the repository to Arduino/libraries/CommandLine.
Restart Arduino IDE, then load this project.

Supportedcommands
	e <pwm> 	Sets the elbow (right) servo to the given level
	s <pwm> 	Sets the shoulder (left) servo to the given level
	b <pwm>		Sets the base (middle) to the given PWM (wich is equivalent to angle for me)
	c <pwm>		Sets the claw servo to the given PWM
	home		Homes the servos to all 90 except the claw which goes to 170.

Note that for each of the servo commands, the value is checked against #defines at the top of the file (such as SHOULDER_MAX) 
