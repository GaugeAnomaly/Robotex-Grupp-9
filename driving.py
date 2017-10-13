from time import sleep
import math

robot_speed = 1
wheel_angle1 = -60
wheel_angle2 = 60
wheel_angle3 = 180

def set_speed(x, y, z):
    return

def get_speed():
    return 0, 0, 0

def rotation_time(deg, motor_speed):
    return 0.5

def rotate_left(deg):
    motor_speed = 10
    set_speed(motor_speed, motor_speed, motor_speed)
    sleep(rotation_time(deg, motor_speed))
    set_speed(0, 0, 0)

def rotate_right(deg):
    motor_speed = -10
    set_speed(motor_speed, motor_speed, motor_speed)
    sleep(rotation_time(deg, motor_speed))
    set_speed(0, 0, 0)

def move(deg, dist):
    speed1 = robot_speed / math.cos(math.radians(wheel_angle1))
    speed2 = robot_speed / math.cos(math.radians(wheel_angle2))
    speed3 = robot_speed / math.cos(math.radians(wheel_angle3))
    set_speed(speed1, speed2, speed3)
    return 

def move_forward(dist):
    move(0, dist)
    
def move_left(dist):
    move(270, dist)
    
def move_right(dist):
    move(90, dist)
    
def move_backward(dist):
    move(180, dist)