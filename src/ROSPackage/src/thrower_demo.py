from robot_movements import *
init_robot_connection()
from time import sleep
while True:
    x = input("Enter thrower speed: ")
    set_thrower_speed(int(x))
    sleep(0.2)
    set_thrower_speed(int(x))
deinit_robot_connection()
