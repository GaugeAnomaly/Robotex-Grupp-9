from math import cos, radians
from time import sleep

from src.ROSPackage.src.robot_serial import *

speed1 = 0
speed2 = 0
speed3 = 0
rot_delta = 0
robot_speed = 30


def set_speeds(sp1, sp2, sp3):
    serial_write('sd0:{}:{}:{}\n'.format(sp1, sp2, sp3))


def set_thrower_speed(speed):
    serial_write('d:{}\n'.format(speed))

def set_speeds_for_direction(angle):
    global robot_speed, speed1, speed2, speed3
    speed1 = -round(robot_speed * cos(radians(angle - 210)), 2)
    speed2 = -round(robot_speed * cos(radians(angle - 330)), 2)
    speed3 = -round(robot_speed * cos(radians(angle - 90)), 2)
    set_speeds(speed1, speed2, speed3)


def rotation_speed(angular_speed):
    global speed1, speed2, speed3, rot_delta
    speed1 -= rot_delta
    speed2 -= rot_delta
    speed3 -= rot_delta
    rot_delta = angular_speed
    speed1 += rot_delta
    speed2 += rot_delta
    speed3 += rot_delta
    set_speeds(speed1, speed2, speed3)


def stop_moving():
    set_speeds(0, 0, 0)


def stop_rotating():
    rotation_speed(0)


def move_left(secs):
    set_speeds_for_direction(270)
    sleep(secs)
    stop_moving()


def move_right(secs):
    set_speeds_for_direction(90)
    sleep(secs)
    stop_moving()


def move_forward(secs):
    set_speeds_for_direction(0)
    sleep(secs)
    stop_moving()


def move_backward(secs):
    set_speeds_for_direction(180)
    sleep(secs)
    stop_moving()


def turn_left(secs):
    set_speeds(-5, -5, -5)
    sleep(secs)
    stop_rotating()


def turn_right(secs):
    set_speeds(5, 5, 5)
    sleep(secs)
    stop_rotating()


def move_left_state():
    set_speeds_for_direction(270)


def move_right_state():
    set_speeds_for_direction(90)


def move_forward_state():
    set_speeds_for_direction(0)


def move_backward_state():
    set_speeds_for_direction(180)


def turn_left_state(speed):
    set_speeds(-speed, -speed, -speed)


def turn_right_state(speed):
    set_speeds(speed, speed, speed)


if __name__ == '__main__':
    init_robot_connection()
    move_forward(0.5)
    deinit_robot_connection()
