#!/usr/bin/env python
# Code to calibrate the meArm by direct driving the motors
# This uses the Adafruit I2C and Servo libraries for controlling the PCA9685. 
# License: Public Domain 

# ROS imports
import rospy
import actionlib
from std_msgs.msg import Header, String
from control_msgs.msg    import FollowJointTrajectoryAction
from control_msgs.msg    import FollowJointTrajectoryFeedback
from control_msgs.msg    import FollowJointTrajectoryGoal
from control_msgs.msg    import FollowJointTrajectoryResult
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg     import JointState

# non-ROS imports
import MeArm_Cal_Jetson_Configuration as cal
import math

# Import the PCA9685 module.
import Adafruit_PWM_Servo_Driver 

class JointContoller():
    _feedback = FollowJointTrajectoryFeedback()
    _result = FollowJointTrajectoryResult()

    def __init__(self):
        self.name = rospy.get_name()

        self.publisher = rospy.Publisher('joint_states', JointState, queue_size=10)
        # Set up action client 
        self.action_server = actionlib.SimpleActionServer('%s/follow_joint_trajectory'%self.name, 
                                            FollowJointTrajectoryAction, 
                                            self.do_action_callback, False)
        self.action_server.start()         

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

    def do_action_callback(self, goal):
        print 'Received goal %d'%len(goal.trajectory.points[0].positions)
        timePassed = rospy.Duration(0)
        self.joint_state.name = goal.trajectory.joint_names

        for point in goal.trajectory.points:
           self.joint_state.header.stamp = rospy.Time.now()
           self.move_arm(goal.trajectory.joint_names, point.positions)
           self.publisher.publish(self.joint_state)
           rospy.sleep(point.time_from_start - timePassed)
           timePassed = point.time_from_start
           print('step')

        self._result.error_code = 0
        self.action_server.set_succeeded(self._result)
        print('move complete')
   
    def get_joint_goal(self, joint_name, joint_list, goal_list):
        if joint_name in joint_list:
            index = joint_list.index(joint_name)
            return goal_list[index]
        print 'ERROR!! Could not find %s goal'% joint_name

    def set_joint_state(self, joint_name, pulse): 
        index = self.joint_state.name.index(joint_name)
        print '%s at %d is %d (%0.2f)' % (joint_name, index, pulse, math.radians(pulse))         
        self.joint_state.position[index] = math.radians(pulse);

    def move_arm(self, names, goal):
        base = self.get_joint_goal('hip', names, goal)
        shoulder = self.get_joint_goal('shoulder', names, goal)
        elbow = self.get_joint_goal('elbow', names, goal)
        claw = self.get_joint_goal('wrist', names, goal)
        self.setJointAngles(base, shoulder, elbow, claw)

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
        pwm_val = 150 + int(pulse*450.0/180.0) # magic incantation to make the timing work
        self.pwm.setPWM(channel, 0, pwm_val)

    def b(self, pulse):
        pulse = self.check_min_max(cal.BASE_MIN_PWM, cal.BASE_MAX_PWM, pulse)
        self.set_joint_state('hip', pulse) 
        self.set_servo_pulse(cal.BASE_SERVO_CHANNEL, pulse)

    def s(self, pulse):
        pulse = self.check_min_max(cal.SHOULDER_MIN_PWM, cal.SHOULDER_MAX_PWM, pulse)
        self.set_joint_state('shoulder', pulse) 
        self.set_servo_pulse(cal.SHOULDER_SERVO_CHANNEL, pulse)

    def e(self, pulse):
        pulse = self.check_min_max(cal.ELBOW_MIN_PWM, cal.ELBOW_MAX_PWM, pulse)
        self.set_joint_state('elbow', pulse)         
        self.set_servo_pulse(cal.ELBOW_SERVO_CHANNEL, pulse)

    def c(self, pulse):
        pulse = self.check_min_max(cal.CLAW_MIN_PWM, cal.CLAW_MAX_PWM, pulse)
        self.set_joint_state('wrist', pulse) 
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

    def loop(self):
        # publish states regularly though this is also done on commands
        while not rospy.is_shutdown():
            self.joint_state.header.stamp = rospy.Time.now()
            self.publisher.publish(self.joint_state)
            self.rate.sleep()
        self.off()

if __name__ == '__main__':
    try:
        rospy.init_node('arm_controller')
        jc = JointContoller()
        jc.loop()
    except rospy.ROSInterruptException:
        pass


#def pub():
#    jc.joint_state.header.stamp = rospy.Time.now()
#    jc.publisher.publish(jc.joint_state)


