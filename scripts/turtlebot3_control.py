#!/usr/bin/env python
import rospy
from geometry_msgs.msg import *
from gazebo_msgs.msg import ModelStates
from rospy.timer import Rate
from sensor_msgs.msg import *
import random

position = Pose()
laser = LaserScan()

def position_callback(data):
    global position
    position = data.pose[-1]
    #print(position)

def laser_callback(data):
    global laser
    laser = data  
    #print(laser)  

if __name__ == '__main__':
        rospy.init_node("turtlebot3_node", anonymous=False)
        rospy.Subscriber("/gazebo/model_states", ModelStates, position_callback)
        rospy.Subscriber("/scan", LaserScan, laser_callback)
        
        pub = rospy.Publisher("/cmd_vel",Twist, queue_size=10)
        r = rospy.Rate(5)
        velocity = Twist()
        while not rospy.is_shutdown():

            if (len(laser.ranges) > 0):
                if (min(laser.ranges[90:270]) > 0.35):
                    velocity.angular.z = 0.0
                    velocity.linear.x = random.uniform(-0.25,-0.35)
                else:
                    velocity.linear.x = 0.0
                    velocity.angular.z = 0.35
                
            rospy.loginfo("Linear Velocity: %s m/s Angular Velocity: %s", velocity.linear.x,velocity.angular.z)
            pub.publish(velocity)
            r.sleep()
        
    