#!/usr/bin/env python
# Code to calibrate the meArm by direct driving the motors
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# License: Public Domain 

# ROS imports
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header, String


# non-ROS imports
import MeArm_Cal_Jetson_Configuration as cal
import math

# Import the PCA9685 module.
import Adafruit_PWM_Servo_Driver 

class JointContoller():
    def __init__(self):
#        execfile('MeArm_Cal_Jetson_Configuration.py')   #import local config info

        # Set up ROS talker to publish joint angles
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        rospy.init_node('mearm_controller')
        self.rate = rospy.Rate(10) # 10hz
        

        self.joint_state = JointState()
        self.joint_state.header = Header()
        self.joint_state.name = ['hip', 'shoulder', 'elbow', 'wrist']
        self.joint_state.position = [1.57, 1.57, 1.57, 1.57] # will be updated in home() before publication in the loop
        self.joint_state.velocity = []
        self.joint_state.effort = []


        # Initialise the PCA9685 using the default address (0x40) and the bus   
        self.pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)
        self.pwm.setPWMFreq(cal.PWM_FREQUENCY)
    	self.home()
        
        rospy.Subscriber('chatter', String, self.callback)


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
            self.pub.publish(self.joint_state)
            self.rate.sleep()
        self.off()


if __name__ == '__main__':
    try:
        jc = JointContoller()
        jc.loop()
    except rospy.ROSInterruptException:
        pass

