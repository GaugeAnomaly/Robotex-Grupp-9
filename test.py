import serial
from math import cos
import math
ser = serial.Serial('/dev/ttyACM0')
robot_speed = 20

def set_speed(sp1, sp2, sp3):
    ser.write(str.encode('sd0:{}:{}:{}\n'.format(sp1, sp2, sp3)))


def set_speeds_for_direction(angle):
    global robot_speed
    speed1 = robot_speed * cos(math.degrees(angle - 240))
    speed2 = robot_speed * cos(math.degrees(angle + 60))
    speed3 = robot_speed * cos(math.degrees(angle - 90))

direction = 0
delta_dir= 0.1
while True:
    set_speeds_for_direction(direction)
    direction += delta_dir