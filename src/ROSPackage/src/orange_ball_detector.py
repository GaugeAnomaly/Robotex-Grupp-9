#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from std_msgs.msg import String
from time import sleep
from math import *
cap = cv2.VideoCapture(0)
# cap.set(13, 0.6)
pub = rospy.Publisher('balldistance', String, queue_size=2)
rospy.init_node('orange_ball_detector')
rate = rospy.Rate(60)
cam_width = 640
cam_height = 480

caught_lower_threshold = int(cam_height * 0.70)
speedy_caught_lower_threshold = int(cam_height * 0.6)
## Ball centering variables
offset = 30
center_x = cam_width / 2
center_y = cam_height / 2
threshold_x1 = center_x - int(cam_width / 100) + offset
threshold_x2 = center_x + int(cam_width / 100) + offset
ball_threshold_x1 = center_x - int(cam_width / 40) + offset
ball_threshold_x2 = center_x + int(cam_width / 40) + offset
toktok_threshold_x1 = center_x - int(cam_width / 5) + offset
toktok_threshold_x2 = center_x + int(cam_width / 5) + offset

ball_threshold_low = int(cam_height * 20 / 24)
ball_threshold_high = int(cam_height / 6)

basket_threshold_low = int(cam_height * 2 / 6)

def slider_callback(data):
    global lower_green, upper_green
    parsed_data = data.data.split(" ")
    lower_green = np.array([int(parsed_data[0]), int(parsed_data[2]), int(parsed_data[4])])
    upper_green = np.array([int(parsed_data[1]), int(parsed_data[3]), int(parsed_data[5])])
    # rospy.loginfo(string)

rospy.Subscriber("slider_values", String, slider_callback)

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
        # c = max(cnts, key=cv2.contourArea)
        c = None
        center = None
        m_area = 0
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            moms = cv2.moments(cnt)
            try:
                cent = (int(moms["m10"] / moms["m00"]), int(moms["m01"] / moms["m00"]))
                if area >= m_area and cent[1] > ball_threshold_high and cent[1] < ball_threshold_low:
                    m_area = area
                    c = cnt
                    center = cent
            except ZeroDivisionError:
                pass
        if c is not None:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box)
            (p1, p2, p3, p4) = box
            width = max(abs(p1[0] - p2[0]), abs(p1[0] - p3[0]))
            dim1 = max(hypot(p1[0] - p2[0], p1[1] - p2[1]), hypot(p1[0] - p4[0], p1[1] - p4[1]))
            dim2 = min(hypot(p1[0] - p2[0], p1[1] - p2[1]), hypot(p1[0] - p4[0], p1[1] - p4[1]))
            try:
                # only proceed if the radius meets a minimum size
                #rospy.loginfo(index % 10)
                if radius > 3: # and (0.75 < dim1 / dim2 < 1.25)
                    # rospy.loginfo(width)
                    #sorted(box, key=lambda s: s[1])
                    #width = abs(box[0][1] - box[3][1])
                    for (x, y) in box:
            		          cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
                    #rospy.loginfo(width)
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, center, int(radius),
                               (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    ballDistanceInfo(color+"--"+str(center[0])+"--"+str(center[1])+"--"+str(width))
                else:
                    ballDistanceInfo(color+"--"+str(-1)+"--"+str(-1)+"--"+str(-1))
            except ZeroDivisionError:
                pass
    else:
        ballDistanceInfo(color+"--"+str(-1)+"--"+str(-1)+"---1")
    return


def distanceBaskets(color, mask, frame):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        # c = max(cnts, key=cv2.contourArea)
        c = None
        center = None
        m_area = 0
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            moms = cv2.moments(cnt)
            try:
                cent = (int(moms["m10"] / moms["m00"]), int(moms["m01"] / moms["m00"]))
                if area >= m_area and cent[1] < basket_threshold_low:
                    m_area = area
                    c = cnt
                    center = cent
            except ZeroDivisionError:
                pass
        if c is not None:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box)
            try:
                # only proceed if the radius meets a minimum size
                #rospy.loginfo(index % 10)
                if radius > 10:
                    (p1, p2, p3, p4) = box
                    # width = abs(p1[0] - p2[0])
                    width = max(abs(p1[0] - p2[0]), abs(p1[0] - p3[0]))
                    # rospy.loginfo(width)
                    for (x, y) in box:
            		          cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
                    #rospy.loginfo(width)
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, center, int(radius),
                               (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (255, 0, 255), -1)
                    ballDistanceInfo(color+"--"+str(center[0])+"--"+str(center[1])+"--"+str(width))
                else:
                    ballDistanceInfo(color+"--"+str(-1)+"--"+str(-1)+"--"+str(-1))
            except ZeroDivisionError:
                pass
    else:
        ballDistanceInfo(color+"--"+str(-1)+"--"+str(-1)+"---1")
    return

def draw_helper_lines(frame):
    # basket Threshold lines - light blue
    cv2.line(frame, (threshold_x1, 0), (threshold_x1, cam_height), (255,255,0))
    cv2.line(frame, (threshold_x2, 0), (threshold_x2, cam_height), (255,255,0))
    # ball Threshold lines -
    cv2.line(frame, (ball_threshold_x1, 0), (ball_threshold_x1, cam_height), (255,180,180))
    cv2.line(frame, (ball_threshold_x2, 0), (ball_threshold_x2, cam_height), (255,180,180))
    # Lowest center of basket - purple
    cv2.line(frame, (0, basket_threshold_low), (cam_width, basket_threshold_low), (255, 0, 255))
    # Ball thresholds - yellow
    cv2.line(frame, (0, ball_threshold_low), (cam_width, ball_threshold_low), (0, 255, 255))
    cv2.line(frame, (0, ball_threshold_high), (cam_width, ball_threshold_high), (0, 255, 255))
    # Toktok thresholds
    cv2.line(frame, (toktok_threshold_x1, 0), (toktok_threshold_x1, cam_height), (0, 255, 255))
    cv2.line(frame, (toktok_threshold_x2, 0), (toktok_threshold_x2, cam_height), (0, 255, 255))
    #Ball is caught
    cv2.line(frame, (0, caught_lower_threshold), (cam_width, caught_lower_threshold), (0, 0, 255))
    cv2.line(frame, (0, speedy_caught_lower_threshold), (cam_width, speedy_caught_lower_threshold), (0, 0, 255))


#lower_orange = np.array([5,100,140])
#upper_orange = np.array([15,190,255])
# basket blue
lower_blue = np.array([30, 50, 00])
upper_blue = np.array([60, 160, 140])
# lower_blue = np.array([48, 122, 33])
# upper_blue = np.array([108, 209, 208])


# basket magenta
# lower_orange = np.array([0, 100, 75])
# upper_orange = np.array([25, 255, 150])
#
# # basket magenta 2
# lower_magenta2 = np.array([155, 100, 150])
# upper_magenta2 = np.array([180, 255, 240])

# basket magenta
lower_magenta = np.array([0, 190, 140])
upper_magenta = np.array([20, 220, 210])

# ball
lower_green = np.array([32, 194, 125])
upper_green = np.array([118, 255, 255])
# lower_green = np.array([38, 194, 4])
# upper_green = np.array([57, 255, 229])


while not rospy.is_shutdown():
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV

    # Threshold the HSV image to get only blue colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    # mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_magenta = cv2.inRange(hsv, lower_magenta , upper_magenta)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    # mask_magenta2 = cv2.inRange(hsv, lower_magenta2, upper_magenta2)
    # mask_orange = cv2.erode(mask_orange, None, iterations=1)
    # mask_orange = cv2.dilate(mask_orange, None, iterations=1)
    # mask_green = cv2.erode(mask_green, None, iterations=2)
    # mask_green = cv2.dilate(mask_green, None, iterations=2)

    mask_basket = mask_blue
    mask_ball = mask_green
    # mask_basket = mask_orange + mask_magenta2

    mask_ball = cv2.erode(mask_ball, None, iterations=1)
    mask_ball = cv2.dilate(mask_ball, None, iterations=1)

    mask_basket = cv2.erode(mask_basket, None, iterations=1)
    mask_basket = cv2.dilate(mask_basket, None, iterations=2)

    mask = mask_ball

    distanceBalls("green", mask_ball, frame)
    distanceBaskets("orange", mask_basket, frame)
    draw_helper_lines(frame)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    rate.sleep()
cv2.destroyAllWindows()
