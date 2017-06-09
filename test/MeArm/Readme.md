This code was adapted from the MeArm_Calibration on codebender:
https://codebender.cc/sketch:148456#MeArm_Calibration.ino

I added a very dumb command line to set the arm to different positions. Each input is two characters: a command and a parameter.
The commands are l for the left motor (the shoulder), r for the right motor (the elbow), c for the claw, and m for the middle (base).
Follow that up with a character 0-I in base 18 for the value to send (which will be multipled by 10):
	r1
Set the right servo to 10. 
	rA
Set the right servo to 100.
	rI
Set the right servo to 180.

Finally, there is a home command. It still requires a parameter but doesn't use it:
	h0
Set all the motors to their home position.	

This code depends on the built-in servo library but no other libraries.