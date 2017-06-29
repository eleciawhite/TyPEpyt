# TyPEpyt
A robot that can type

# test
The test directory has the intermediate tests for setting up the MeArm system. 

Start with the MeArm_Calibration for Arduino. That is for both direct servo control and inverse kinetmatics (see its README.md). 

Similar code for the MeArm on the Jetson is in python with MeArm_Cal_Jetson being the direct servo control and MeArm_IK_Jetson having the inverse kinematic code.

# ros_ws
Robot Operating System (ROS) workspace for catkins. 
Currently, this works with rvis, gazebo, and moveit. 

To lanch all three:
```	cd ros_ws
	source devel/setup.bash
	roslaunch typepyt_moveit_config all.launch```

For just Gazebo, change the last line to:
```	roslaunch typepyt typepyt.launch```
