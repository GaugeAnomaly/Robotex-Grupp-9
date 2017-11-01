#!/usr/bin/env python
import cv2
from time import sleep
import numpy as np
cap = cv2.VideoCapture(0)
#import rospy
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,320);
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240);
while True:
    _, output = cap.read()
    lower_green = np.array([40, 100, 0])
    upper_green = np.array([85, 240, 255])
    hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=4)
    output = cv2.bitwise_and(output, output, mask=mask_green)
    
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 4, 5, minRadius=10, maxRadius=70)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        print("Here")
        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 5)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print(x, y, r)
    cv2.imshow('frame', output)
    cv2.imshow('greenmask', mask_green)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
