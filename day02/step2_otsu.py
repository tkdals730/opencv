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
    return filename

# 이미지 읽기 (그레이스케일)
get_sample('sudoku.png')
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

assert img is not None, "이미지를 읽지 못했습니다."

# 창 생성
cv.namedWindow('Trackbar')
cv.namedWindow('Compare')

# 트랙바 생성
# manual_thresh: 수동 임계값
# mode: 0=비교 보기, 1=비교 보기(같이 유지해도 됨)
cv.createTrackbar('manual_thresh', 'Trackbar', 127, 255, nothing)
cv.createTrackbar('mode', 'Trackbar', 0, 1, nothing)

while True:
    # 트랙바 값 읽기
    manual_thresh = cv.getTrackbarPos('manual_thresh', 'Trackbar')
    mode = cv.getTrackbarPos('mode', 'Trackbar')

    # 수동 이진화
    ret_manual, manual_th = cv.threshold(img, manual_thresh, 255, cv.THRESH_BINARY)

    # Otsu 자동 이진화
    ret_otsu, otsu_th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # putText를 위해 컬러로 변환
    img_color = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    manual_color = cv.cvtColor(manual_th, cv.COLOR_GRAY2BGR)
    otsu_color = cv.cvtColor(otsu_th, cv.COLOR_GRAY2BGR)

    # 화면에 글씨 표시
    cv.putText(img_color, 'Original', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv.putText(manual_color, f'Manual: {manual_thresh}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv.putText(otsu_color, f'Otsu: {ret_otsu:.0f}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # mode가 0이든 1이든 원본 | 수동 | Otsu 비교
    combined = np.hstack([img_color, manual_color, otsu_color])

    cv.imshow('Compare', combined)

    # 콘솔에도 출력
    print(f"Manual: {manual_thresh}, Otsu: {ret_otsu:.0f}", end='\r')

    # q → 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()