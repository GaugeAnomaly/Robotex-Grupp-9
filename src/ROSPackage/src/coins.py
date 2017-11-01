#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from matplotlib import pyplot as plt
from std_msgs.msg import String
from time import sleep
cap = cv2.VideoCapture(0)
pub = rospy.Publisher('test1', String, queue_size=10)
rospy.init_node('test2')


while not rospy.is_shutdown():
    sleep(0.08)
    # Take each frame
    _, frame = cap.read()

    img = frame
    img = cv2.medianBlur(img,5)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    cimg=img
    rospy.loginfo('before houghcircles')
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)
    rospy.loginfo('after houghcircles')
    circles = np.uint16(np.around(circles))
    rospy.loginfo('after rounding')
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    rospy.loginfo('after for loop')
    cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()

        



