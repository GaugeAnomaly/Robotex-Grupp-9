import serial
from math import cos
import math
from time import sleep
#ser = serial.Serial('/dev/ttyACM0')
robot_speed = 20
speed1 = 0
speed2 = 0
speed3 = 0

rot_delta = 0

def set_speed(sp1, sp2, sp3):
    global direction
    #ser.write(str.encode('sd0:{}:{}:{}\n'.format(sp1, sp2, sp3)))
    print(direction)
    print(str.encode('sd0:{}:{}:{}\n'.format(sp1, sp2, sp3)))


def rotation_speed(angular_speed):
    global speed1, speed2, speed3, rot_delta
    speed1 -= rot_delta
    speed2 -= rot_delta
    speed3 -= rot_delta
    rot_delta = angular_speed
    speed1 += rot_delta
    speed2 += rot_delta
    speed3 += rot_delta


def set_speeds_for_direction(angle):
    global robot_speed, speed1, speed2, speed3
    speed1 = round(robot_speed * cos(math.radians(angle - 210)), 2)
    speed2 = round(robot_speed * cos(math.radians(angle - 330)), 2)
    speed3 = round(robot_speed * cos(math.radians(angle - 90)), 2)
    set_speed(speed1, speed2, speed3)

def do_cross():
    set_speeds_for_direction(0)
    sleep(1)
    set_speeds_for_direction(180)
    sleep(2)
    set_speeds_for_direction(0)
    sleep(1)
    set_speeds_for_direction(90)
    sleep(1)
    set_speeds_for_direction(270)
    sleep(2)
    set_speeds_for_direction(90)
    sleep(1)


direction = 0
delta_dir= 0.1
while True:
    set_speeds_for_direction(direction)
    sleep(0.005)
    direction += delta_dir