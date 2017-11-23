#!/usr/bin/env python
import Tkinter
import rospy
from std_msgs.msg import String

rospy.init_node('sliders_node', anonymous=True)
pub = rospy.Publisher('slider_values', String, queue_size=1)

values = [0,0,0,0,0,0]

def print_values():
    pub.publish(" ".join(list(map(str, values))))


def set_value(index, val):
    global values
    values[index] = val
    print_values()

set_value1 = lambda x: set_value(0, x)
set_value2 = lambda x: set_value(1, x)
set_value3 = lambda x: set_value(2, x)
set_value4 = lambda x: set_value(3, x)
set_value5 = lambda x: set_value(4, x)
set_value6 = lambda x: set_value(5, x)


root = Tkinter.Tk()

scale = Tkinter.Scale(orient='horizontal', from_=0, to=180, length=500, label='h_low', command=set_value1)
scale.pack()
scale = Tkinter.Scale(orient='horizontal', from_=0, to=180, length=500, label='h_high', command=set_value2)
scale.pack()
scale = Tkinter.Scale(orient='horizontal', from_=0, to=255, length=500, label='s_low', command=set_value3)
scale.pack()
scale = Tkinter.Scale(orient='horizontal', from_=0, to=255, length=500, label='s_high', command=set_value4)
scale.pack()
scale = Tkinter.Scale(orient='horizontal', from_=0, to=255, length=500, label='v_low', command=set_value5)
scale.pack()
scale = Tkinter.Scale(orient='horizontal', from_=0, to=255, length=500, label='v_high', command=set_value6)
scale.pack()

root.mainloop()
