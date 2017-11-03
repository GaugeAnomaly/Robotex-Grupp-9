#!/usr/bin/env python
import rospy
from std_msgs.msg import String

from src.ROSPackage.src.robot_movements import *

rospy.init_node('autonomous_logic_node', anonymous=True)
#  If referee has given the start but not the stop command
allowed_to_play = True
#  Camera dimensions for reference
cam_width = 640
cam_height = 480
#  Current coordinates of the main ball and the basket in sight
ball_x = -1
ball_y = -1
basket_x = -1
basket_y = -1
#  Booleans that get updated via callbacks
ball_in_sight = False
basket_in_sight = False
ball_caught = False
#  Maximum turning speed
max_turn_speed = 5

caught_lower_threshold = cam_height * 0.83
## Ball centering variables
center_x = cam_width / 2
center_y = cam_height / 2
threshold_x1 = center_x - int(cam_width / 20)
threshold_x2 = center_x + int(cam_width / 20)


# Functions
#  TODO: take into account the refereee start, ping and stop signals
def referee_callback(data):
    global allowed_to_play
    #  allowed_to_paly = data.data...


# TODO: get basket information
def cam_callback(data):
    global ball_x, ball_y, ball_in_sight, basket_in_sight, basket_x, basket_y
    # rospy.loginfo(data.data)
    parsed_data = data.data.split("--")
    if parsed_data[0] == 'green':
        if float(parsed_data[1]) < 0:
            ball_in_sight = False
            # rospy.loginfo("%s %d %d", ball_in_sight, ball_x, ball_y)
        else:
            ball_x = float(parsed_data[1])
            ball_y = float(parsed_data[2])
            ball_in_sight = True
            # rospy.loginfo("%s %d %d", ball_in_sight, ball_x, ball_y)
    if parsed_data[0] == 'orange':
        if float(parsed_data[1]) < 0:
            basket_in_sight = True
        else:
            basket_x = float(parsed_data[1])
            basket_y = float(parsed_data[2])
            basket_in_sight = True


# TODO: make turning speed proportional to offset
def center_ball():
    if ball_in_sight:
        if threshold_x1 <= ball_x <= threshold_x2:
            stop_rotating()
        else:
            if ball_x < threshold_x1:
                turn_left_state(max([(threshold_x1 - ball_x) * 0.01, max_turn_speed]))
            elif ball_x > threshold_x2:
                turn_right_state(max([(ball_x - threshold_x2) * 0.01, max_turn_speed]))


# TODO: make moving proportional to offset
def center_basket():
    if basket_in_sight:
        if threshold_x1 <= basket_x <= threshold_x2:
            stop_moving()
        else:
            if basket_x < threshold_x1:
                move_right_state()
            elif basket_x > threshold_x2:
                move_left_state()


# TODO: implement calculation
def calculate_thrower_speed():
    return 200


# Predicate functions
def ball_is_caught() -> bool:
    return ball_y > caught_lower_threshold


def ball_is_centered() -> bool:
    return threshold_x1 <= ball_x <= threshold_x2


def basket_is_centered() -> bool:
    return threshold_x1 <= basket_x <= threshold_x2


# States
#  TODO: add initial ball discovering rotation and maybe spatial mapping
def looking_for_ball():
    global state
    if ball_in_sight:
        state = moving_to_ball


def moving_to_ball():
    global state
    if ball_in_sight:
        center_ball()
        if not ball_is_caught():
            move_forward_state()
        else:
            state = finding_basket
    else:
        state = looking_for_ball


# Assuming the ball is found, the robot will twirl around the ball until both the ball and the basket are centered
def finding_basket():
    global state
    if ball_in_sight and not basket_in_sight:
        move_left_state()
        center_ball()
    elif ball_in_sight and basket_in_sight:
        center_ball()
        center_basket()
        if ball_is_centered() and basket_is_centered():
            stop_moving()  # just in case
            stop_rotating()
            state = throw_ball
    else:
        state = looking_for_ball


def throw_ball():
    global state
    set_thrower_speed(calculate_thrower_speed())
    move_forward(0.5)
    state = looking_for_ball


state = looking_for_ball
rospy.Subscriber("balldistance", String, cam_callback)
init_robot_connection()

while not rospy.is_shutdown() and allowed_to_play:
    state()

deinit_robot_connection()
