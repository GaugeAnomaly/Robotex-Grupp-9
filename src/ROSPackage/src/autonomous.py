#!/usr/bin/env python
from time import sleep
from robot_movements import *
from std_msgs.msg import String
import rospy
rospy.init_node('autonomous_logic_node', anonymous=True)
cam_width = 640
cam_height = 480
cor_x = -1
cor_y = -1
ball_in_sight = False
ball_caught = False
caught_lower_threshold = cam_height * 0.83


def callback(data):
    global cor_x, cor_y, ball_in_sight
    #rospy.loginfo(data.data)
    parsed_data = data.data.split("--")
    if parsed_data[0] == 'green':
        if float(parsed_data[1]) < 0:
            ball_in_sight = False
            #rospy.loginfo("%s %d %d", ball_in_sight, cor_x, cor_y)
        else:
            cor_x = float(parsed_data[1])
            cor_y = float(parsed_data[2])
            ball_in_sight = True
            #rospy.loginfo("%s %d %d", ball_in_sight, cor_x, cor_y)


rospy.Subscriber("balldistance", String, callback)
init_robot_connection()

def center_view_on_ball():  # if ball is close enough to the center, this function can just pass
    center_x = cam_width/2
    center_y = cam_height/2
    threshold_x1 = center_x - int(cam_width/20)
    threshold_x2 = center_x + int(cam_width/20)

    while ball_in_sight and not rospy.is_shutdown():
        if threshold_x1 <= cor_x and cor_x <= threshold_x2:
            break
        else:
            if cor_x < threshold_x1:
                turn_left(0.1)
                if cor_x > threshold_x2:
                    turn_right(0.05)
            elif cor_x > threshold_x2:
                turn_right(0.1)
                if cor_x < threshold_x1:
                    turn_left(0.05)


def ball_is_caught():
    if cor_y > caught_lower_threshold:
        return True
    else:
        return False

while not rospy.is_shutdown():
    rospy.loginfo("%s %d %d", ball_in_sight, cor_x, cor_y)
    if not ball_in_sight:
        pass
        # This can also be turn_right(0.5)
        #turn_left(0.5)  # takes time in seconds as argument
        #rospy.loginfo("ball not in sight")
    else:
        while ball_in_sight and not ball_caught and not rospy.is_shutdown():
            #rospy.loginfo("%s %d %d", ball_in_sight, cor_x, cor_y)
            #rospy.loginfo("Im here")
            #rospy.loginfo("ball in sight and not caught")
            center_view_on_ball()  # only rotates to the correct position
            move_forward(0.1)  # also takes seconds
            if ball_is_caught():  # if the ball is very close to the front of the robot
                ball_caught = True
                rospy.loginfo("ball caught")
        if ball_caught and not ball_is_caught():  # if the ball was caught previously but not anymore
            rospy.loginfo("ball lost")
            ball_caught = False
deinit_robot_connection()
