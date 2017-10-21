import serial
import curses

screen = curses.initscr()
ser = serial.Serial('/dev/ttyACM0')
screen.keypad(True)
curses.cbreak()
curses.noecho()

def set_speed(sp1, sp2, sp3):
    ser.write(str.encode('sd0:{}:{}:{}\n'.format(sp1, sp2, sp3)))

def process(c):
    if c == ord('w'):
        screen.addstr(0, 0, 'w')
    elif c == ord('a'):
        screen.addstr(0, 0, 'a')
    elif c == ord('s'):
        screen.addstr(0, 0, 's')
    elif c == ord('d'):
        screen.addstr(0, 0, 'd')
    elif c == ord('q'):
        screen.addstr(0, 0, 'q')
    elif c == ord('e'):
        screen.addstr(0, 0, 'e')
    elif c == ord('z'):
        screen.addstr(0, 0, 'z')
    elif c == ord('x'):
        screen.addstr(0, 0, 'x')
    elif c == curses.KEY_RIGHT:
        screen.addstr(0, 0, 'right')
        set_speed(-10,-10,-10)
    elif c == curses.KEY_LEFT:
        screen.addstr(0, 0, 'left')
        set_speed(10,10,10)
    elif c == curses.KEY_UP:
        screen.addstr(-10, 10, 'up')
    elif c == curses.KEY_DOWN:
        screen.addstr(0, 0, 'down')
        set_speed(10, -10, 0)
    else:
        pass

while True:
    x = screen.getch()
    process(x)
