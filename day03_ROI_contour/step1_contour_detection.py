import cv2 as cv
import numpy as np

# 이미지 로드 (그레이스케일)
img = cv.imread('./img/smarties.png')
img2 = img.copy()
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 또는 임계값으로 이진화
_, binary = cv.threshold(imgray, 240, 255, cv.THRESH_BINARY_INV)

# 컨투어 검출
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

# 칼라 이미지로 변환 (그리기용)
img_color = cv.cvtColor(imgray, cv.COLOR_GRAY2BGR)

# 모든 컨투어 그리기 초록색
cv.drawContours(img_color, contours, -1, (0, 255, 0), 2)

# 면적 필터링 (100~5000 픽셀 범위)
for cnt in contours:
    area = cv.contourArea(cnt)
    print(area)
    if 100 < area < 120:
        # 조건을 만족하는 컨투어를 파란색으로 그리기
        cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 2)

# 결과 표시
cv.imshow('Filtered Contours', img_color)
cv.imshow('binary', binary)
cv.imshow('orginal', img)
cv.waitKey(0)

cv.destroyAllWindows()