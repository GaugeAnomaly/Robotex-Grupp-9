#!/usr/bin/env python
import Tkinter as tk
import rospy
from std_msgs.msg import String
from robot_movements import *
rospy.init_node('mapper_node', anonymous=True)
# TODO: Add throwing functionality to node
init_robot_connection()

root = tk.Tk()
y_label = tk.Label(root, text="y-value: ")
y_label.grid()
speed_label = tk.Label(root, text="Speed: ")
speed_label.grid(row=1, column=0)
speed_entry = tk.Entry(root)
speed_entry.grid(row=1, column=1)
powers_l = []
powers = tk.Text(root, height=4, width=70)
powers.grid(row=2, columnspan=2)
powers.config(state=tk.DISABLED)
yvalues_l = []
yvalues = tk.Text(root, height=4, width=70)
yvalues.grid(row=3, columnspan=2)
yvalues.config(state=tk.DISABLED)

lower_basket_y = ""
current_speed = 0

def cam_callback(data):
    global lower_basket_y
    parsed_data = data.data.split("--")
    if parsed_data[0] == 'orange' and float(parsed_data[1]) >= 0:
        lower_basket_y = parsed_data[3] # change between y-value and width
        y_label["text"] = 'y_value: ' + lower_basket_y

rospy.Subscriber("balldistance", String, cam_callback)

def return_key_pressed(event):
    global current_speed
    es = int(speed_entry.get())
    if es != current_speed:
        current_speed = int(speed_entry.get())
    else:
        current_speed = 0

def update_thrower():
    if current_speed != 0:
        set_thrower_speed(current_speed)
    # rospy.loginfo("Thrower %i", current_speed)
    root.after(500, update_thrower)

def save_values():
    powers_l.append(int(speed_entry.get()))
    update_powers()

    yvalues_l.append(int(float(lower_basket_y)))
    update_yvalues()

def update_powers():
    powers.config(state=tk.NORMAL)
    powers.delete(1.0, tk.END)
    powers.insert(tk.END, str(powers_l))
    powers.config(state=tk.DISABLED)

def update_yvalues():
    yvalues.config(state=tk.NORMAL)
    yvalues.delete(1.0, tk.END)
    yvalues.insert(tk.END, str(yvalues_l))
    yvalues.config(state=tk.DISABLED)

def delete_last():
    global powers_l, yvalues_l

    powers_l = powers_l[:-1]
    update_powers()

    yvalues_l = yvalues_l[:-1]
    update_yvalues()

save_button = tk.Button(root, text="Save values", command=save_values)
save_button.grid(row=4, column=0)
delete_button = tk.Button(root, text="Delete last", command=delete_last)
delete_button.grid(row=4, column=1)
root.bind('<Return>', return_key_pressed)
root.after(1, update_thrower)
root.mainloop()
# deinit_robot_connection()
