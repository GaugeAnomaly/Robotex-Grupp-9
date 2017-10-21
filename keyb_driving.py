import curses
from robot_movements import *

screen = curses.initscr()
screen.keypad(True)
curses.cbreak()
curses.noecho()
init_robot_connection()

def process(c):
    if c == ord('w'):
        screen.addstr(0, 0, 'w')
        set_speeds_for_direction(0)
    elif c == ord('a'):
        screen.addstr(0, 0, 'a')
        set_speeds_for_direction(270)
    elif c == ord('s'):
        screen.addstr(0, 0, 's')
        set_speeds_for_direction(180)
    elif c == ord('d'):
        screen.addstr(0, 0, 'd')
        set_speeds_for_direction(90)
    elif c == ord('q'):
        screen.addstr(0, 0, 'q')
        set_speeds_for_direction(315)
    elif c == ord('e'):
        screen.addstr(0, 0, 'e')
        set_speeds_for_direction(45)
    elif c == ord('z'):
        screen.addstr(0, 0, 'z')
        set_speeds_for_direction(225)
    elif c == ord('c'):
        screen.addstr(0, 0, 'c')
        set_speeds_for_direction(135)
    elif c == curses.KEY_RIGHT:
        screen.addstr(0, 0, 'right')
        set_speeds(-10,-10,-10)
    elif c == curses.KEY_LEFT:
        screen.addstr(0, 0, 'left')
        set_speeds(10,10,10)
    elif c == curses.KEY_UP:
        screen.addstr(0, 0, 'up')
    elif c == curses.KEY_DOWN:
        screen.addstr(0, 0, 'down')
        set_speeds(10, -10, 0)
    else:
        pass

while True:
    x = screen.getch()
    process(x)
