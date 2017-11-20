#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Bool
from time import sleep

from robot_movements import *

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
basket_width = 0
#  Booleans that get updated via callbacks
ball_in_sight = False
basket_in_sight = False
ball_caught = False
#  Maximum turning speed
max_turn_speed = 7
max_move_speed = 7

caught_lower_threshold = cam_height * 0.80
## Ball centering variables
offset = 10
center_x = cam_width / 2 + offset
center_y = cam_height / 2
threshold_x1 = center_x - int(cam_width / 120) + offset
threshold_x2 = center_x + int(cam_width / 120) + offset
widths = [29,31,35,34,39,41,42,45,46,48,49,51,48,48.5,51,53.33,54,56,
59.33, 61, 64.75, 67.333, 70, 74, 79.25, 81, 87.75, 95.6, 103]

powers = [200,195,190,193,187,185,183,182,181,180,179,178,177,176,175,174,173,
172,171,170,169,168,167,166,165,164,163,162,161]


# Functions
#  TODO: take into account the refereee start, ping and stop signals
def referee_callback(data):
    global allowed_to_play, state, allowed_to_play
    if data.data:
        state = looking_for_ball
    else:
        allowed_to_play = False
    #  allowed_to_paly = data.data...


# TODO: get basket information
def cam_callback(data):
    global ball_x, ball_y, ball_in_sight, basket_in_sight, basket_x, basket_y, basket_width
    #rospy.loginfo(data.data)
    parsed_data = data.data.split("--")
    if parsed_data[0] == 'green':
        if float(parsed_data[1]) < 0:
            if ball_in_sight == True:
                ball_in_sight = False
                #rospy.loginfo("Ball lost")
            #rospy.loginfo(data.data)
            #rospy.loginfo("%s %d %d", ball_in_sight, ball_x, ball_y)
        else:
            ball_x = float(parsed_data[1])
            ball_y = float(parsed_data[2])
            if ball_in_sight == False:
                ball_in_sight = True
                #rospy.loginfo("Ball found")
            #rospy.loginfo("%s %d %d", ball_in_sight, ball_x, ball_y)
    if parsed_data[0] == 'orange':
        if float(parsed_data[1]) < 0:
            basket_in_sight = False
        else:
            basket_x = float(parsed_data[1])
            basket_y = float(parsed_data[2])
            basket_width = float(parsed_data[3])
            #rospy.loginfo("basket width: %s", basket_width)
            basket_in_sight = True


# TODO: make turning speed proportional to offset
def center_ball():
    if ball_in_sight:
        if threshold_x1 <= ball_x <= threshold_x2:
            stop_rotating()
        else:
            if ball_x < threshold_x1:
                turn_left_state(max_turn_speed)
                # turn_left_state(max_turn_speed * (cam_height * 0.8 ball_y)
                # turn_left_state(min([(center_x - ball_x) * 0.40, max_turn_speed]))
            elif ball_x > threshold_x2:
                turn_right_state(max_turn_speed)
                #rospy.loginfo(min([(ball_x - center_x) * 0.20, max_turn_speed]))
                # turn_right_state(min([(ball_x - center_x) * 0.40, max_turn_speed]))


# TODO: make moving proportional to offset
def center_basket():
    if basket_in_sight:
        if threshold_x1 <= basket_x <= threshold_x2:
            stop_moving()
        else:
            if basket_x < threshold_x1:
                move_right_state(min([(center_x - basket_x) * 0.2, max_move_speed]))
            elif basket_x > threshold_x2:
                move_left_state(min([(basket_x - center_x) * 0.2, max_move_speed]))


# TODO: implement calculation
def calculate_thrower_speed():
    for i in range(len(widths)):
        if widths[i] > basket_width + (basket_width * 0.1):
            return powers[i]

    #return 140 + 150 - basket_width


# Predicate functions
def ball_is_caught():
    return ball_y > caught_lower_threshold


def ball_is_centered():
    return threshold_x1 <= ball_x <= threshold_x2


def basket_is_centered():
    return threshold_x1 <= basket_x <= threshold_x2

def transition_to_state(newstate):
    global state
    allowed_to_play = False
    rospy.loginfo(newstate)
    state = newstate


# States
#  TODO: add initial ball discovering rotation and maybe spatial mapping
def looking_for_ball():
    #rospy.loginfo("looking for ball state")
    #rospy.loginfo(ball_in_sight)
    if ball_in_sight:
        transition_to_state(moving_to_ball)
        #state = moving_to_ball
    else:
        # stop_moving()
        turn_left_state(10)


def moving_to_ball():
    global state
    #rospy.loginfo("moving to ball state")
    if ball_in_sight:
        center_ball()
        if not ball_is_caught():
            move_forward_state(10)
            pass
        else:
            #state = finding_basket
            pass
            transition_to_state(finding_basket)
    else:
        transition_to_state(looking_for_ball)
        #state = looking_for_ball


# Assuming the ball is found, the robot will twirl around the ball until both the ball and the basket are centered
def finding_basket():
    global state
    rospy.loginfo("basket %d %d %d", threshold_x1, basket_x + offset, threshold_x2)
    rospy.loginfo("ball %d %d %d", threshold_x1, ball_x + offset, threshold_x2)
    # rospy.loginfo(ball_in_sight, basket_in_sight, ball_is_centered(), basket_is_centered())
    if ball_in_sight and not basket_in_sight:
        # rospy.loginfo("basket %d %d %d", threshold_x1, basket_x + offset, threshold_x2)
        # rospy.loginfo("ball %d %d %d", threshold_x1, ball_x + offset, threshold_x2)
        move_left_state(10)
        center_ball()
    elif ball_in_sight and basket_in_sight:
        center_ball()
        center_basket()
        # rospy.loginfo("basket %d %d %d", threshold_x1, basket_x + offset, threshold_x2)
        # rospy.loginfo("ball %d %d %d", threshold_x1, ball_x + offset, threshold_x2)
        if ball_is_centered() and basket_is_centered():
            # rospy.loginfo("basket %d %d %d", threshold_x1, basket_x + offset, threshold_x2)
            # rospy.loginfo("ball %d %d %d", threshold_x1, ball_x + offset, threshold_x2)
            stop_moving()  # just in case
            stop_rotating()
            transition_to_state(throw_ball)
    else:
        transition_to_state(looking_for_ball)


def throw_ball():
    global state
    #rospy.loginfo("thowing ball state")
    set_thrower_speed(calculate_thrower_speed())
    move_forward_state(25)
    sleep(1)
    transition_to_state(looking_for_ball)

# This should be the initial state
def waiting_for_referee():
    # rospy.loginfo(ball_is_centered())
    #rospy.loginfo(ball_x)
    #sleep(0.1)
    pass

# Only for testing
def spinning_thrower():
    set_thrower_speed(calculate_thrower_speed())
    sleep(0.5)


def twirl():
    set_speeds(0,0,20)

state = looking_for_ball
# state = waiting_for_referee
rospy.Subscriber("balldistance", String, cam_callback)
rospy.Subscriber("referee", Bool, referee_callback)
init_robot_connection()

counter = 0
while not rospy.is_shutdown() and allowed_to_play:
    sleep(0.01)
    # rospy.loginfo("basket width: %d", basket_width)
    state()
    #if counter % 200 == 0:
        #rospy.loginfo("basket width: " + str(basket_width))
    #rospy.loginfo(state)

deinit_robot_connection()
