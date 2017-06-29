#!/usr/bin/env python
# Code to calibrate the meArm by direct driving the motors
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# License: Public Domain 

# ROS imports
import rospy
import actionlib
from std_msgs.msg import Header, String
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryFeedback
from control_msgs.msg import FollowJointTrajectoryGoal
from control_msgs.msg import FollowJointTrajectorResult


# non-ROS imports
import MeArm_Cal_Jetson_Configuration as cal
import math

# Import the PCA9685 module.
import Adafruit_PWM_Servo_Driver 


# action related definitions
DEFAULT_FREQ = 60.0
MAX_FREQ = 200.0

class JointContoller():
    _feedback = FollowJointTrajectoryFeedback()
    _result = FollowJointTrajectoryResult()

    def __init__(self):
        self.name = rospy.get_name().replace('/','')
        self.publisher = rospy.Publisher('%s/joint_path_command'%self.name, JointTrajectory, queue_size=10)
        # Set up action client 
        self.action_server = actionlib.SimpleActionServer('%s'%self.name, 
                                            FollowJointTrajectoryAction, 
                                            self.do_action_callback, False)
        self.action_server.start()         
        
        # Set up joint states
        self.joint_state = JointState()
        self.joint_state.header = Header()
        self.joint_state.name = ['hip', 'shoulder', 'elbow', 'wrist']
        self.joint_state.position = [1.57, 1.57, 1.57, 1.57] # will be updated in home() before publication in the loop
        self.joint_state.velocity = []
        self.joint_state.effort = []

        self.desired_freq = DEFAULT_FREQ
        self.ros_initialized = False
        self.action_running = False

        self.ros_setup()

        # Initialise the PCA9685 using the default address (0x40) and the bus   
        self.pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)
        self.pwm.setPWMFreq(cal.PWM_FREQUENCY)
    	self.home()
        
    
    def ros_setup:
        # Creates and inits ROS components
        if self.ros_initialized:
            return 0
        # Set up publish joint angles
        rospy.init_node('%s'%self.node_name)
        


        self.rate = rospy.Rate(10) # 10hz

    def do_action_callback(self, action):


    def check_min_max(self, minVal, maxVal, test):
        if (test < minVal):
	        test = minVal
	        print "min %d" % (minVal)		
        if (test > maxVal):
	        test = maxVal
	        print "min %d" % (maxVal)		
        return test

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
        self.joint_state.position[channel] = math.radians(pulse);
        pwm_val = 150 + int(pulse*450.0/180.0) # magic incantation to make the timing work
        self.pwm.setPWM(channel, 0, pwm_val)

    def b(self, pulse):
        pulse = self.check_min_max(cal.BASE_MIN_PWM, cal.BASE_MAX_PWM, pulse)
        self.set_servo_pulse(cal.BASE_SERVO_CHANNEL, pulse)

    def s(self, pulse):
        pulse = self.check_min_max(cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM, pulse)
        self.set_servo_pulse(cal.SHOULDER_SERVO_CHANNEL, pulse)

    def e(self, pulse):
        pulse = self.check_min_max(cal.ELBOW_MIN_PWM, cal.ELBOW_MAX_PWM, pulse)
        self.set_servo_pulse(cal.ELBOW_SERVO_CHANNEL, pulse)

    def c(self, pulse):
        pulse = self.check_min_max(cal.CLAW_MIN_PWM, cal.CLAW_MAX_PWM, pulse)
        self.set_servo_pulse(cal.CLAW_SERVO_CHANNEL, pulse)

    def setJointAngles(self, base, shoulder, elbow, claw):
        self.b(int(math.degrees(base)))
        self.s(int(math.degrees(shoulder)))
        self.e(int(math.degrees(elbow)))
        self.c(int(math.degrees(claw)))

    def home(self):
        self.b(cal.BASE_HOME_PWM)
        self.s(cal.SHOULDER_HOME_PWM)
        self.e(cal.ELBOW_HOME_PWM)
        self.c(cal.CLAW_HOME_PWM)

    def off(self):
        self.pwm.setPWM(cal.BASE_SERVO_CHANNEL, 0, 0)
        self.pwm.setPWM(cal.SHOULDER_SERVO_CHANNEL, 0, 0)
        self.pwm.setPWM(cal.ELBOW_SERVO_CHANNEL, 0, 0)
        self.pwm.setPWM(cal.CLAW_SERVO_CHANNEL, 0, 0)

    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def loop(self):
        #check for commands, publish states
        while not rospy.is_shutdown():
            self.joint_state.header.stamp = rospy.Time.now()
            self.state_publisher.publish(self.joint_state)
            self.rate.sleep()
        self.off()


if __name__ == '__main__':
    try:
        jc = JointContoller()
        jc.loop()
    except rospy.ROSInterruptException:
        pass

