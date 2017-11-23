#!/usr/bin/env python
import serial
import time
import rospy
from std_msgs.msg import Bool
pub = rospy.Publisher('referee', Bool, queue_size=2)
rospy.init_node('rf_node')
rate = rospy.Rate(200)
my_field = 'O'
my_letter = 'P'
my_ident = my_field + my_letter

while not rospy.is_shutdown():
    with serial.Serial('/dev/ttyACM0', timeout=1) as s:
        tdata = s.read()           # Wait forever for anything
        time.sleep(0.01)              # Sleep (or inWaiting() doesn't give the correct value)
        data_left = s.inWaiting()  # Get the number of characters ready to be read
        tdata += s.read(data_left) # Do the read and combine it with the first character
        cmd = tdata.decode()[5:17]
        ident = cmd[1:3]
        #print("Recieved: " + tdata.decode())
        #print("Identiy: " + ident)
        req = cmd.split("-")[0][3:]
        #print("Command: " + req)
        if ident == my_ident or ident == my_field + 'x':
            #print("Identity match, sending ACK")
            if req == 'START':
                pub.publish(True)
            if req == 'STOP':
                pub.publish(False)
            if ident == my_ident:
                s.write(str.encode("rf:a" + my_ident + "ACK------\n"))
            #print("rf:a"+ my_ident + "ACK------\n")
        rate.sleep()
