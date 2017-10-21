from time import sleep
from robot_movements import *

cam_width = 1000
cam_height = 1000

def ball_in_sight():  # returns true, if there is actually a large blob of pixels that make up the ball
    pass

def center_view_on_ball():  # if ball is close enough to the center, this function can just pass
    
    center_x = cam_width/2
    center_y = cam_height/2
    cor_x = 80
    cor_y = 90
    threshold_x1 = center_x - int(cam_width/16)
    threshold_x2 = center_x + int(cam_width/16)
    
    while True:
        if threshold_x1 <= cor_x <= threshold_x2:
            pass
        else:
            while True:
                if cor_x < threshold_x1:
                    turn_right(0.3)
                    if cor_x > threshold_x2:
                        turn_left(0.1)
                    else:
                        pass
                elif cor_x > threshold_x2:
                    turn_left(0.3)
                    if cor_x < threshold_x1:
                        turn_right(0.1)
                    else:
                        pass
                else:
                    break

lower_threshold = cam_height * 0.95

def ball_is_caught():
    cor_x = 80
    cor_y = 90
    while True:
        if cor_y <= lower_threshold:
            move_forward(0.3)
        elif cor_y >= lower_threshold:
            break

init_robot_connection()
ball_caught = False

while True:
    if not ball_in_sight():
        # This can also be turn_right(0.5)
        turn_left(0.5)  # takes time in seconds as argument
    else:
        while ball_in_sight() and not ball_caught:
            center_view_on_ball()  # only rotates to the correct position
            move_forward(0.3)  # also takes seconds
            if ball_is_caught():  # if the ball is very close to the front of the robot
                ball_caught = True
        if ball_caught and not ball_is_caught():  # if the ball was caught previously but not anymore
            ball_caught = False
