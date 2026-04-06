import cv2 as cv
import numpy as np

# 1단계: 이미지 로드
img = cv.imread('road_example2.jpg')
scale = 0.1
img_resized = cv.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))

gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)

# 2단계: 블러 + 캐니
blur = cv.GaussianBlur(gray, (5, 5), 0)
edges = cv.Canny(blur, 100, 200)

# 3단계: ROI 마스크 만들기
height, width = edges.shape
mask = np.zeros_like(edges)

# 도로 부분만 남기는 다각형 값하나씩 대입
roi = np.array([[
    (0, height-10 ),
    (width // 2 - 60, height // 2 + 70),
    (width // 2 + 60, height // 2 + 70),
    (width, height-10)
]], dtype=np.int32)

cv.fillPoly(mask, roi, 255)
roi_edges = cv.bitwise_and(edges, mask)

roi_points = roi.copy()

# ROI영역 시각화 파란선
roi_visual = img_resized.copy()
cv.polylines(roi_visual, roi_points, True, (255, 0, 0), 2)

cv.imshow('ROI Area', roi_visual)

# 4단계: 허프 직선 변환
lines = cv.HoughLinesP(
    roi_edges,
    1,
    np.pi / 180,
    threshold=20,
    minLineLength=30,
    maxLineGap=20
)

# 5단계: 기울기 필터링 후 그리기
result = img_resized.copy()

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # 0으로 나누기 방지
        if x2 == x1:
            continue

        slope = (y2 - y1) / (x2 - x1)

        # 너무 수평이거나 너무 수직에 가까운 선 제거
        if abs(slope) < 0.5:
            continue

        # 차선처럼 보이는 선만 그리기
        cv.line(result, (x1, y1), (x2, y2), (0, 255, 0), 3)

cv.imshow('Gray', gray)
cv.imshow('Edges', edges)
cv.imshow('ROI Edges', roi_edges)
cv.imshow('Lane Detection', result)
cv.waitKey(0)
cv.destroyAllWindows()