#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from std_msgs.msg import String
cap = cv2.VideoCapture(0)
pub = rospy.Publisher('balldistance', String, queue_size=10)
rospy.init_node('orange_ball_detector')

def ballDistanceInfo(string):
    pub.publish(string)


def distanceBalls(color, mask, frame):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        try:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            #rospy.loginfo(index % 10)
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                ballDistanceInfo("\""+color+"--"+str(x)+"--"+str(y)+"\"")
        except ZeroDivisionError:
            pass

    return




while not rospy.is_shutdown():
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV

    #lower_orange = np.array([5,100,140])
    #upper_orange = np.array([15,190,255])

    lower_orange = np.array([5, 90, 220])
    upper_orange = np.array([30, 255, 255])

    lower_green = np.array([60, 120, 0])
    upper_green = np.array([85, 240, 255])

    #HSV Color
    #lower_green = np.array([70, 100, 100])
    #upper_green = np.array([147, 100, 100])


    # Threshold the HSV image to get only blue colors
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask = mask_green + mask_orange
    #
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    distanceBalls("green", mask_green, frame)
    distanceBalls("orange", mask_orange, frame)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
