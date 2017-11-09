"""import numpy as np
import cv2
from time import sleep
cap = cv2.VideoCapture(0)


sleep(0.01)
#while(True):
# Capture frame-by-frame
ret, frame = cap.read()

# Our operations on the frame come here
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Display the resulting frame
cv2.imshow('pic', frame)
cv2.imshow('frame',gray)
if cv2.waitKey(1) & 0xFF == ord('q'):
    pass
while True: pass
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()"""

from cv2 import *
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
gray = cvtColor(img, COLOR_BGR2HSV)
if s:    # frame captured without any errors
    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
    imshow("cam-test",gray)
    waitKey(0)
    destroyWindow("cam-test")
    imwrite("asdfgh.jpg",gray) #save image
