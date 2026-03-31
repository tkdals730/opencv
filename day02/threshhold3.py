import cv2 as cv
import numpy as np
import urllib.request
import os

def nothing(x):
    pass

def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)   # 컬러로 읽음

img = get_sample('sudoku.png')

assert img is not None, "이미지를 읽지 못했습니다."

cv.namedWindow('Trackbar')

cv.createTrackbar('H_min', 'Trackbar', 35, 179, nothing)
cv.createTrackbar('H_max', 'Trackbar', 85, 179, nothing)
cv.createTrackbar('S_min', 'Trackbar', 50, 255, nothing)
cv.createTrackbar('S_max', 'Trackbar', 255, 255, nothing)
cv.createTrackbar('V_min', 'Trackbar', 50, 255, nothing)
cv.createTrackbar('V_max', 'Trackbar', 255, 255, nothing)

while (1):
    frame = img.copy()   # 이미지 한 장을 계속 복사해서 사용

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    h_min = cv.getTrackbarPos('H_min', 'Trackbar')
    h_max = cv.getTrackbarPos('H_max', 'Trackbar')
    s_min = cv.getTrackbarPos('S_min', 'Trackbar')
    s_max = cv.getTrackbarPos('S_max', 'Trackbar')
    v_min = cv.getTrackbarPos('V_min', 'Trackbar')
    v_max = cv.getTrackbarPos('V_max', 'Trackbar')

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('Original', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Result', result)

    print(f"H: {h_min}-{h_max}, S: {s_min}-{s_max}, V: {v_min}-{v_max}", end='\r')

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()