#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Bool
from time import sleep, time

from robot_movements import *
from global_vars import *
rospy.init_node('autonomous_logic_node', anonymous=True)
rate = rospy.Rate(300)
#  If referee has given the start but not the stop command
allowed_to_play = True
#  Current coordinates of the main ball and the basket in sight
ball_x = -1
ball_y = -1
basket_x = -1
basket_y = -1
opposing_x = -1
opposing_y = -1
basket_width = 0
lower_basket_y = -1
#  Booleans that get updated via callbacks
basket_to_the_left = True
ball_in_sight = False
basket_in_sight = False
ball_caught = False
ball_centered = False
basket_centered = False
#  Maximum turning speed
max_turn_speed = 12
max_centering_turn_speed = 12
max_centering_move_speed = 12
max_move_speed = 12

sleep_time = 0.25
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
    global ball_x, ball_y, ball_in_sight, basket_in_sight, basket_x, basket_y
    global basket_width, ball_caught, ball_centered, basket_centered
    global opposing_x, opposing_y, basket_to_the_left, lower_basket_y
    #rospy.loginfo(data.data)
    parsed_data = data.data.split("--")
    if parsed_data[0] == 'green':
        # rospy.loginfo("%s %d %d", ball_in_sight, ball_x, ball_y)
        if float(parsed_data[1]) < 0:
            if ball_in_sight == True:
                ball_in_sight = False
                # rospy.loginfo("Ball found: %i, Ball caught: %i, Ball centered %i", ball_in_sight, ball_caught, ball_centered)
            #rospy.loginfo(data.data)
            # rospy.loginfo("%s %d %d", ball_in_sight, ball_x, ball_y)
        else:
            ball_x = float(parsed_data[1])
            ball_y = float(parsed_data[2])
            # rospy.loginfo("Ball in toktok: %i, in ball: %i, in basket: %i", in_toktok_threshold(ball_x), in_mid_threshold(ball_x), in_basket_threshold(ball_x))
            if ball_in_sight == False:
                ball_in_sight = True
                # rospy.loginfo("Ball found: %i, Ball caught: %i, Ball centered %i", ball_in_sight, ball_caught, ball_centered)
            if not ball_caught and ball_is_caught():
                ball_caught = True
                # rospy.loginfo("Ball found: %i, Ball caught: %i, Ball centered %i", ball_in_sight, ball_caught, ball_centered)
            elif ball_caught and not ball_is_caught():
                ball_caught = False
                # rospy.loginfo("Ball found: %i, Ball caught: %i, Ball centered %i", ball_in_sight, ball_caught, ball_centered)
            if ball_centered and not ball_is_centered():
                ball_centered = False
                # rospy.loginfo("Ball found: %i, Ball caught: %i, Ball centered %i", ball_in_sight, ball_caught, ball_centered)
            elif not ball_centered and ball_is_centered():
                ball_centered = True
                # rospy.loginfo("Ball found: %i, Ball caught: %i, Ball centered %i", ball_in_sight, ball_caught, ball_centered)
                if basket_is_centered():
                    pass
                    # rospy.loginfo("Basket and ball are centered")
            # rospy.loginfo("%d %d", ball_x, ball_y)
    elif parsed_data[0] == 'opposing':
        opposing_x = float(parsed_data[1])
        if opposing_x >= 0:
            if opposing_x < center_x and basket_to_the_left:
                basket_to_the_left = False
                # rospy.loginfo("Basket to the left %i, opposing_x: %d", basket_to_the_left, opposing_x)
            elif opposing_x >= center_x and not basket_to_the_left:
                basket_to_the_left = True
                # rospy.loginfo("Basket to the left %i, opposing_x: %d", basket_to_the_left, opposing_x)


    elif parsed_data[0] == 'orange':
        if float(parsed_data[1]) < 0:
            if basket_in_sight:
                if basket_x < center_x:
                    basket_to_the_left = True
                else:
                    basket_to_the_left = False
                # rospy.loginfo("Basket to the left %i", basket_to_the_left)
            basket_in_sight = False
        else:
            basket_x = float(parsed_data[1])
            basket_y = float(parsed_data[2])
            basket_width = float(parsed_data[3])
            lower_basket_y = int(parsed_data[4])
            # rospy.loginfo("Basket cords: %f %f, x1: %d x2: %d, Basket centered %i", basket_x, basket_y, threshold_x1, threshold_x2, basket_is_centered())
            basket_in_sight = True
            if basket_centered and not basket_is_centered():
                basket_centered = False

            elif not basket_centered and basket_is_centered():
                basket_centered = True
                if ball_is_centered():
                    pass


# TODO: make turning speed proportional to offset
def center_ball():
    if ball_in_sight:
        if ball_is_centered():
            stop_rotating()
        else:
            if ball_x < ball_threshold_x1:
                if toktok_threshold_x1 < ball_x < toktok_threshold_x2:
                    turn_left_state(4)
                else:
                    turn_left_state(13)
            elif ball_x > ball_threshold_x2:
                if toktok_threshold_x1 < ball_x < toktok_threshold_x2:
                    turn_right_state(4)
                else:
                    turn_right_state(13)


def center_ball2():
    if ball_in_sight:
        if ball_is_centered():
            stop_rotating()
        else:
            if ball_x < ball_threshold_x1:
                if toktok_threshold_x1 < ball_x < toktok_threshold_x2:
                    turn_left_state(8)
                else:
                    turn_left_state(15)
                # sleep(0.15)
                # stop_rotating()
                # turn_left_state(max_turn_speed * (cam_height * 0.8 ball_y)
                # turn_left_state(min([(center_x - ball_x) * 0.40, max_turn_speed]))
            elif ball_x > ball_threshold_x2:
                if toktok_threshold_x1 < ball_x < toktok_threshold_x2:
                    turn_right_state(8)
                else:
                    turn_right_state(15)


# TODO: make moving proportional to offset
def center_basket():
    if basket_in_sight:
        if threshold_x1 < basket_x < threshold_x2:
            stop_moving()
        else:
            if basket_x < threshold_x1:
                # move_right_state(min([(center_x - basket_x) * 0.2, max_move_speed]))
                if toktok_threshold_x1 < basket_x < toktok_threshold_x2:
                    move_rigth_state(10)
                else:
                    move_right_state(7)
                #sleep(sleep_time)
                #stop_moving()
            elif basket_x > threshold_x2:
                # move_left_state(min([(basket_x - center_x) * 0.2, max_move_speed]))
                if toktok_threshold_x1 < basket_x < toktok_threshold_x2:
                    move_left_state(10)
                else:
                    move_left_state(7)
                #sleep(sleep_time)
                #stop_moving()

def keep_distance():
    if ball_in_sight:
        if toktok_threshold_x1 < ball_x < toktok_threshold_x2 and not ball_is_caught():
            move_forward_state(max_move_speed)
            sleep(sleep_time)
        if ball_is_caught() and ball_y > ball_threshold_low:
            move_backward_state(max_move_speed)
            sleep(sleep_time)
            # stop_moving()

def lin_interp(x, x1, x2, y1, y2):
    factor = (x - x1) / (x2 - x1)
    return (y2 - y1) * factor + y1

def calculate_thrower_speed():
    # from 55px and lower offset=3
    # bigger offset = 2

    # offset = 0
    offset = 1
    if basket_width >= 95:
        return 160
    if basket_width <= 29:
        return 200
    if basket_width <= 78:
        offset = 2
    if basket_width <= 55:
        offset = 3

    rospy.loginfo(basket_width)

    for i in range(len(widths)):
        if widths[i] > basket_width: # + (basket_width * 0.1):
            return lin_interp(basket_width, widths[i-1], widths[i], powers[i-1], powers[i]) + offset + 1

    #return 140 + 150 - basket_width


# Predicate functions
def ball_is_caught():
    return ball_y > caught_lower_threshold

def speedy_ball_is_caught():
    return ball_y > speedy_caught_lower_threshold


def ball_is_centered():
    return ball_threshold_x1 <= ball_x <= ball_threshold_x2


def basket_is_centered():
    return threshold_x1 <= basket_x <= threshold_x2

def in_toktok_threshold(x):
    return toktok_threshold_x1 < x < toktok_threshold_x2

def in_mid_threshold(x):
    return ball_threshold_x1 < x < ball_threshold_x2

def in_basket_threshold(x):
    return threshold_x1 < x < threshold_x2

def transition_to_state(newstate):
    global state
    set_speeds_for_direction(0, 0)
    stop_rotating()
    stop_moving()
    # rospy.loginfo(newstate)
    state = newstate


# States
#  TODO: add initial ball discovering rotation and maybe spatial mapping
def looking_for_ball():
    # rospy.loginfo("looking for ball state")
    # rospy.loginfo(ball_in_sight)
    if ball_in_sight:
        # rospy.loginfo("ball in sight")
        transition_to_state(moving_to_ball)
    else:
        # rospy.loginfo("ball not in sight")
        turn_left_state(20)
        # stop_rotating()


def moving_to_ball():
    #rospy.loginfo("moving to ball state")
    if ball_in_sight:
        center_ball()
        if not speedy_ball_is_caught() and toktok_threshold_x1 < ball_x < toktok_threshold_x2:
            move_forward_state(50)
            pass
        elif speedy_ball_is_caught() and toktok_threshold_x1 < ball_x < toktok_threshold_x2:
            stop_moving()
            stop_rotating()
            pass
            transition_to_state(finding_basket)
    else:
        transition_to_state(looking_for_ball)

def toktok_left():
    move_left_state(10)
    sleep(sleep_time)
    stop_moving()

def toktok_right():
    move_right_state(10)
    sleep(sleep_time)
    stop_moving()

def toktok():
    if basket_x <= threshold_x1:
        toktok_right()
    elif basket_x >= threshold_x2:
        toktok_left()

def toktok2_left():
    move_left_state(10)
    sleep(0.6)
    stop_moving()

def toktok2_right():
    move_right_state(10)
    sleep(0.6)
    stop_moving()

def toktok2():
    if basket_x <= threshold_x1:
        toktok2_right()
    elif basket_x >= threshold_x2:
        toktok2_left()

# Assuming the ball is found, the robot will twirl around the ball until both the ball and the basket are centered
def finding_basket():
    if ball_in_sight and not basket_in_sight:
        if basket_to_the_left:
            move_right_state(10)
        else:
            move_left_state(10)
        # sleep(sleep_time)
        # stop_moving()
        center_ball2()
        keep_distance()
    elif ball_in_sight and basket_in_sight:
        # if threshold_x1 <= basket_x <= threshold_x2:
        #     stop_moving()
        if toktok_threshold_x1 < basket_x < toktok_threshold_x2:
            toktok()
            # center_basket()
            center_ball()
            keep_distance()
        else:
            center_basket()
            center_ball2()
            keep_distance()
        if ball_is_centered() and basket_is_centered():
            # rospy.loginfo("basket %d %d %d", threshold_x1, basket_x + offset, threshold_x2)
            # rospy.loginfo("ball %d %d %d", threshold_x1, ball_x + offset, threshold_x2)
            stop_rotating()
            stop_moving()  # just in case
            sleep(0.3)
            if ball_is_centered() and basket_is_centered():
                transition_to_state(throw_ball)
    else:
        transition_to_state(looking_for_ball)


def throw_ball():
    global state
    # rospy.loginfo("Width: %i", basket_width)
    set_thrower_speed(calculate_thrower_speed())
    move_forward_state(25)
    sleep(1)
    transition_to_state(looking_for_ball)

# This should be the initial state
def waiting_for_referee():
    # rospy.loginfo(ball_is_centered())
    #rospy.loginfo(ball_x)
    #rospy.loginfo(ball_caught)
    # sleep(0.1)
    pass

# Only for testing
def spinning_thrower():
    set_thrower_speed(calculate_thrower_speed())
    sleep(0.5)

state = looking_for_ball
# state = waiting_for_referee
rospy.Subscriber("balldistance", String, cam_callback)
rospy.Subscriber("referee", Bool, referee_callback)
init_robot_connection()
sleep(8)
while not rospy.is_shutdown() and allowed_to_play:
    # sleep(0.01)
    # rospy.loginfo("basket width: %d", basket_width)
    # rospy.loginfo("Before")
    state()
    # rospy.loginfo("After")
    rate.sleep()
    #if counter % 200 == 0:
        #rospy.loginfo("basket width: " + str(basket_width))

deinit_robot_connection()
