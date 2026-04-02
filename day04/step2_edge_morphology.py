import cv2 as cv
import numpy as np
import os
import urllib.request

# 이미지 로드
def get_sample(filename, repo='opencv'):
    if not os.path.exists(filename):
        if repo == 'insightbook':
            url = f"https://raw.githubusercontent.com/dltpdn/insightbook.opencv_project_python/master/img/{filename}"
        else:  # opencv 공식
            url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename
img = cv.imread(get_sample('moon_gray.jpg', repo='insightbook'))

if img is None:
    print("❌ 이미지를 불러올 수 없습니다.")
    exit()

# 그레이스케일 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# ============================================================
# 1. Canny 에지 검출
# ============================================================
threshold1 = 50   # 낮은 임계값
threshold2 = 150  # 높은 임계값

threshold3 = 90   # 낮은 임계값
threshold4 = 180  # 높은 임계값
#
# Canny 에지 검출 적용
edges = cv.Canny(gray, threshold1, threshold2)
edgesv2 = cv.Canny(gray, threshold3, threshold4)

# ============================================================
# 2. 모폴로지 연산 — 열기 (Opening)
# ============================================================
# 커널 생성 (5x5 타원)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
#
# 열기 연산 (침식 후 팽창: 노이즈 제거)
edges_cleaned = cv.morphologyEx(edges, cv.MORPH_OPEN, kernel)
edges_cleaned2 = cv.morphologyEx(edgesv2, cv.MORPH_OPEN, kernel)
#
# 선택사항: 닫기 연산 (팽창 후 침식: 구멍 채우기)
edges_closed = cv.morphologyEx(edges_cleaned, cv.MORPH_CLOSE, kernel)
edges_closed2 = cv.morphologyEx(edges_cleaned2, cv.MORPH_CLOSE, kernel)

# ============================================================
# 3. 결과 비교 표시 thresh1, threshold2 사용
# ============================================================
# 원본 → Canny → 열기 → 닫기 순서로 4개 이미지 배열
canny_color = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
cleaned_color = cv.cvtColor(edges_cleaned, cv.COLOR_GRAY2BGR)
closed_color = cv.cvtColor(edges_closed, cv.COLOR_GRAY2BGR)
# ============================================================
# 3. 임계값 다르게 결과 비교 thresh3, threshold4 사용
# ============================================================
canny_color2 = cv.cvtColor(edgesv2, cv.COLOR_GRAY2BGR)
cleaned_color2 = cv.cvtColor(edges_cleaned2, cv.COLOR_GRAY2BGR)
closed_color2 = cv.cvtColor(edges_closed2, cv.COLOR_GRAY2BGR)


# 임계값 threshold1,threshold2 적용
top_row = np.hstack([img, canny_color])
bottom_row = np.hstack([cleaned_color])
result = np.hstack([top_row, bottom_row])

# 임계값 threshold3,threshold4 적용
top_row2 = np.hstack([img, canny_color2])
bottom_row2 = np.hstack([cleaned_color2])
result2 = np.hstack([top_row2, bottom_row2])

cv.putText(result, f'minThreshold: {threshold1}', (10, 30),
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv.putText(result, f'maxThreshold: {threshold2}', (10, 60),
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv.putText(result2, f'minThreshold: {threshold3}', (10, 30),
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv.putText(result2, f'maxThreshold: {threshold4}', (10, 60),
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


cv.imshow('Edge Detection + Morphology', result)
cv.imshow('diff threshold', result2)
cv.waitKey(0)
cv.destroyAllWindows()
