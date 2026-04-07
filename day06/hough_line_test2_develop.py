import cv2 as cv
import numpy as np

# 이미지 로드
img = cv.imread('road_example2.jpg')
scale = 0.1
img_resized = cv.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))
gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)

# 전처리: 가우시안 블러 (노이즈 제거)
blurred = cv.GaussianBlur(gray, (5, 5), 0)

# 에지 검출
edges = cv.Canny(blurred, 100, 200, apertureSize=3)

# 모폴로지 연산: 에지 강화 (선택)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
# edges = cv.dilate(edges, kernel, iterations=1)  # 선의 굵기 증가

# 3단계: ROI 마스크 만들기
height, width = edges.shape
mask = np.zeros_like(edges)

# 도로 부분만 남기는 다각형 값하나씩 대입
roi = np.array([[
    (0, height-10 ),
    (width // 2 - 60, height // 2 + 60),
    (width // 2 + 60, height // 2 + 60),
    (width, height-10)
]], dtype=np.int32)

cv.fillPoly(mask, roi, 255)
roi_edges = cv.bitwise_and(edges, mask)

roi_points = roi.copy()

# ROI영역 시각화 파란선
roi_visual = img_resized.copy()
cv.polylines(roi_visual, roi_points, True, (255, 0, 0), 2)

cv.imshow('ROI Area', roi_visual)

# Hough Line Transform
lines = cv.HoughLinesP(roi_edges, 1, np.pi/180, threshold=50,
                       minLineLength=30, maxLineGap=10)

# 결과 표시
result = img_resized.copy()
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
    print(f"ROI 적용 후 검출된 직선: {len(lines)}개")
else:
    print("직선이 검출되지 않았습니다.")

cv.imshow('Original', gray)
cv.imshow('Edges', edges)
cv.imshow('Result', result)
cv.imshow('ROI Edges', roi_edges)
cv.waitKey(0)
cv.destroyAllWindows()
