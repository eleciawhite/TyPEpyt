# TyPEpyt
A robot that can type. Sort of. Someday.

For more information about the system and building it, look at the keyword "ty" on Embedded.fm (https://www.embedded.fm/search?q=Ty)

# test
The test directory has the intermediate tests for setting up can calibrating the MeArm mechanics. 

Start with the MeArm_Calibration for Arduino. That is for both direct servo control and inverse kinetmatics (see its README.md). 

Similar code for the MeArm on the Jetson is in python with MeArm_Cal_Jetson being the direct servo control and MeArm_IK_Jetson having the inverse kinematic code. 

# laser_cat_demo
Used for the "On Cats and Typing" presentation, this shows off different motion methods to demonstrate kinematic movement. 

This code also has the laser cat mode which uses a USB web camera to have the arm chase the laser. 

To run the cat demo,
> execfile('ty.py')
> ty.cat()
If you place your web camera so it is just over the area the arm is in (with the arm not obstructing the view), the system looks like the arm is chasing the laser. When you turn off the laser, the arm will settle into a buttwiggle, just like a real cat getting ready to pounce.

This code also explore direct path moves vs kinematic.

# prototyper
Hunt-and-peck typing at its worst. Also, dictation done badly. 

This requires the USB camera to be above the workspace so it can see the keyboard. 

To use this code, start python and run these commands in Python.
> execfile('ty.py')
> ty.start()
Lets you adjust the camera view and make sure the arm can reach all of the keys before the system starts using this to type keys.
> ty.cal()
Verifies the keyboard is in range of the arm and the camera can recognize the arm at different points in the frame.
If the arm goes out of camera frame or the blue sticker isn't recognized, then adjust your system and re-run start and cal again.
> ty.pressKey('h')
Will perss a single key after cal and start have been run.
> ty.pressString("hello")
Will press the keys one after another. The final typed string will be on the command line at the end of the command 

> ty.dictate()
Uses CMUSphinx's pocketsphinx to parse audio and then types what it hears. Note that the dictionary path is hard-coded so do a git clone https://github.com/cmusphinx/pocketsphinx into the directory parallel with this one. When done, your directory structure should look like:

-- TyPEypt
  -- prototyper
-- pocketspinc
  -- test
  -- model


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

Note that there is are bugs in the meArm URDF: it has simple linkages for the shoulder and elbow that make it so the motion planner tries to go in the Z direction but the physical version doesn't match. Also, I don't know how to model the end effector so I put it in as a wrist but that doesn't get visualized.
