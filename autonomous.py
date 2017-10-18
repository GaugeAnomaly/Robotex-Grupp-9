from time import sleep

def init_robot_connection(): # inits the serial communications on for the robot
    pass


def ball_in_sight(): # returns true, if there is actually a large blob of pixels that make up the ball
    pass


def turn_left(seconds): # should include a sleep function somewhere
    pass


def center_view_on_ball(): # if ball is close enough to the center, this function can just pass
    pass


def drive_forward(seconds):
    pass


def ball_is_caught():
    pass



init_robot_connection()
ball_caught = False

while True:
    if not ball_in_sight():
        # This can also be turn_right(0.5)
        turn_left(0.5) # takes time in seconds as argument
    else:
        while ball_in_sight() and not ball_caught:
            center_view_on_ball() # only rotates to the correct position
            drive_forward(0.3) # also takes seconds
            if ball_is_caught(): # if the ball is very close to the front of the robot
                ball_caught = True
        if ball_caught and not ball_is_caught(): # if the ball was caught previously but not anymore
            ball_caught = False
