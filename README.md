# TyPEpyt
A robot that can type

# test
The test directory has the intermediate tests for setting up the MeArm system. 

Start with the MeArm_Calibration for Arduino. That is for both direct servo control and inverse kinetmatics (see its README.md). 

Similar code for the MeArm on the Jetson is in python with MeArm_Cal_Jetson being the direct servo control and MeArm_IK_Jetson having the inverse kinematic code.

# ros_ws
Robot Operating System (ROS) workspace for catkins. 
Currently, this works with rvis, gazebo, and moveit. 

To lanch all three in a demo environment:
```	
        cd ros_ws
	source devel/setup.bash
	roslaunch typepyt_moveit_config all.launch
```

For just Gazebo, change the last line to:
```	
        roslaunch typepyt typepyt.launch
```

This code also works with a meArm python controller (typepyt/scripts) and the MoveIt motion controller. The meArm is connected to a PCA9685 which is connected to I2C1.

To make that work, you probably need a bunch of windows insetead of backgrounding (&) the different verbose commands:
``` 
    roscore &
    cd ros_ws
    source devel/setup.bash
    cd src/typepyt/scripts
    python meArm.py &
    roslaunch typepyt_moveit_config demo.launch 
```

Note that there is are bugs in the meArm URDF: it has simple linkages for the shoulder and elbow that make it so the motion 
planner tries to go in the Z direction but the physical version doesn't match. Also, I don't know how to model the end effector so I put it in as a wrist but that doesn't get visualized.
