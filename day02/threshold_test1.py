import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import urllib.request
import os

# 창 생성 (namedWindow)

# 트랙바 생성
# — threshold (0~255, 초기값 127)
# — mode: 0=THRESH_BINARY, 1=THRESH_BINARY_INV

# 반복문
    # 트랙바 값 읽기 (getTrackbarPos)

    # 이진화 적용
    # — mode가 0이면 THRESH_BINARY, 1이면 THRESH_BINARY_INV

    # 원본 | 이진화 결과 나란히 표시
    # — np.hstack([img, thresh]) 또는 np.hstack([img, result])

    # 현재 임계값을 화면에 표시
    # — cv.putText(result, f'Thresh: {value}', ...)


def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

# 샘플 이미지 (그레이스케일로 읽기)
img = get_sample('sudoku.png')
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

def nothing(x):
    pass

cv.namedWindow('Trackbar')

#cv.createTrackbar('R', 'image', 0, 255, nothing)
#cv.createTrackbar('G', 'image', 0, 255, nothing)
#cv.createTrackbar('B', 'image', 0, 255, nothing)
cv.createTrackbar('H_min', 'Trackbar', 35, 179, nothing)
cv.createTrackbar('H_max', 'Trackbar', 85, 179, nothing)
cv.createTrackbar('S_min', 'Trackbar', 50, 255, nothing)
cv.createTrackbar('S_max', 'Trackbar', 255, 255, nothing)
cv.createTrackbar('V_min', 'Trackbar', 50, 255, nothing)
cv.createTrackbar('V_max', 'Trackbar', 255, 255, nothing)

assert img is not None, "file could not be read, check with os.path.exists()"

ret,thresh1 = cv.threshold(img,20,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,50,255,cv.THRESH_BINARY_INV)




titles = ['Original Image','BINARY','BINARY_INV']
images = [img, thresh1, thresh2]
 
for i in range(3):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
 


while(1):
    #cv.imshow('image', img)
    frame = img.copy()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #k = cv.waitKey(1) & 0xFF
    #if k == 27:
        #break
    
    #r = cv.getTrackbarPos('R', 'image')
    #g = cv.getTrackbarPos('G', 'image')
    #b = cv.getTrackbarPos('B', 'image')
    #s = cv.getTrackbarPos(switch, 'image')

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

    print(f"H: {h_min} - { h_max}, S: {s_min} - s{s_max}, V: {v_min}")

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

plt.show()