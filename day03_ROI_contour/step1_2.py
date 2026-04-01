import cv2 as cv
import numpy as np

img = cv.imread('./img/smarties.png')
if img is None:
    print("이미지 로드 실패")
    exit()

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# 초록색 범위
lower_green = np.array([35, 80, 80])
upper_green = np.array([85, 255, 255])

mask = cv.inRange(hsv, lower_green, upper_green)

# 컨투어 찾기
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

img2 = img.copy()

# 컨투어 그리기
for cnt in contours:
    area = cv.contourArea(cnt)
    print(area)
    if area > 300:
        cv.drawContours(img2, [cnt], 0, (0, 255, 0), 2)

cv.imshow("mask", mask)
cv.imshow("result", img2)
cv.waitKey(0)
cv.destroyAllWindows()