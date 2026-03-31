import cv2 as cv 
import numpy as np 

cap = cv.VideoCapture(0)

while(1):

    _, frame = cap.read()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 포스트잇 컬러
    lower_yellow = np.array([20,85,85])
    upper_yellow = np.array([35,255,255])

    #lower_blue = np.array([110, 50, 50])
    #uppper_blue = np.array([130, 255, 255])

    mask = cv.inRange(hsv, lower_yellow, upper_yellow)

    res = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame',frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()