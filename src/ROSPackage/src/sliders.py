#!/usr/bin/env python
import Tkinter
import rospy
from std_msgs.msg import String

rospy.init_node('sliders_node', anonymous=True)
pub = rospy.Publisher('slider_values', String, queue_size=1)

def print_value(val):
    pub.publish(str(val))

root = Tkinter.Tk()

scale = Tkinter.Scale(orient='horizontal', from_=0, to=128, command=print_value)
scale.pack()

root.mainloop()
