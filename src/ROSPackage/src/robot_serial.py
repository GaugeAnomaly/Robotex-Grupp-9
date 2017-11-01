import serial
ser = None

def init_robot_connection():
    global ser
    ser = serial.Serial('/dev/ttyACM0')


def deinit_robot_connection():
    ser.close()


def serial_write(string):
    ser.write(str.encode(string))


def serial_read(nOfChars):
    return ser.read(nOfChars)


def is_serial_open():
    return ser.is_open
