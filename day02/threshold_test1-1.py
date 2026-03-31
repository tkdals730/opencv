import cv2 as cv
import numpy as np
import urllib.request
import os

def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

def nothing(x):
    pass

# 샘플 이미지 다운로드 + 그레이스케일로 읽기
get_sample('sudoku.png')
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

assert img is not None, "file could not be read, check with os.path.exists()"

# 창 생성
cv.namedWindow('Trackbar')

# 트랙바 생성
cv.createTrackbar('threshold', 'Trackbar', 127, 255, nothing)
cv.createTrackbar('mode', 'Trackbar', 0, 1, nothing)   # 0=BINARY, 1=BINARY_INV

while True:
    # 트랙바 값 읽기
    value = cv.getTrackbarPos('threshold', 'Trackbar')
    mode = cv.getTrackbarPos('mode', 'Trackbar')

    # mode에 따라 threshold 방식 선택
    if mode == 0:
        thresh_type = cv.THRESH_BINARY
        mode_text = 'THRESH_BINARY'
    else:
        thresh_type = cv.THRESH_BINARY_INV
        mode_text = 'THRESH_BINARY_INV'

    # 이진화 적용
    ret, result = cv.threshold(img, value, 255, thresh_type)

    # putText를 쓰려면 컬러 이미지로 바꾸는 게 편함
    result_color = cv.cvtColor(result, cv.COLOR_GRAY2BGR)
    img_color = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    # 현재 threshold 값 표시
    cv.putText(result_color, f'Thresh: {value}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.putText(result_color, f'Mode: {mode_text}', (10, 65),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 원본 | 결과 나란히 붙이기
    combined = np.hstack([img_color, result_color])

    cv.imshow('Original | Result', combined)

    # q 누르면 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()