import cv2 as cv
import numpy as np
import urllib.request
import os

# ============================================================
# 전역 변수
# ============================================================
win_name = "Document Scanning"
img = None
draw = None
rows, cols = 0, 0
pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)

# ============================================================
# 마우스 콜백 함수
# ============================================================
def onMouse(event, x, y, flags, param):
    """
    마우스로 4개 점을 클릭하면:
    1. 클릭 위치에 초록색 원 표시
    2. 4개 점 수집 후 자동으로 좌상/우상/우하/좌하 판단
    3. 원근 변환 적용
    """
    global pts_cnt, draw, pts, img
    
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(draw, (x,y), 10, (0,255,0), -1) # 좌표에 초록색 동그라미 표시
        cv.imshow(win_name, draw)

        pts[pts_cnt] = [x,y]            # 마우스 좌표 저장
        pts_cnt+=1
        if pts_cnt == 4:                       # 좌표가 4개 수집됨 
            # 좌표 4개 중 상하좌우 찾기 ---② 
            sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(pts, axis = 1)       # 4쌍의 좌표 각각 x-y 계산

            topLeft = pts[np.argmin(sm)]         # x+y가 가장 값이 좌상단 좌표
            bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단 좌표
            topRight = pts[np.argmin(diff)]     # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = pts[np.argmax(diff)]   # x-y가 가장 큰 값이 좌하단 좌표

            # 변환 전 4개 좌표 
            pts1 = np.float32([topLeft, topRight, bottomRight , bottomLeft])

            # 변환 후 영상에 사용할 서류의 폭과 높이 계산 ---③ 
            w1 = abs(bottomRight[0] - bottomLeft[0])    # 상단 좌우 좌표간의 거리
            w2 = abs(topRight[0] - topLeft[0])          # 하당 좌우 좌표간의 거리
            h1 = abs(topRight[1] - bottomRight[1])      # 우측 상하 좌표간의 거리
            h2 = abs(topLeft[1] - bottomLeft[1])        # 좌측 상하 좌표간의 거리
            width = int(max([w1, w2]))                       # 두 좌우 거리간의 최대값이 서류의 폭
            height = int(max([h1, h2]))                      # 두 상하 거리간의 최대값이 서류의 높이
            
            # 변환 후 4개 좌표
            pts2 = np.float32([[0,0], [width-1,0], 
                                [width-1,height-1], [0,height-1]])

            # 변환 행렬 계산 
            mtrx = cv.getPerspectiveTransform(pts1, pts2)
            # 원근 변환 적용
            result = cv.warpPerspective(img, mtrx, (width, height))
            cv.imshow('scanned', result) 

        

# ============================================================

def get_sample(filename, repo='opencv'):
    if not os.path.exists(filename):
        if repo == 'insightbook':
            url = f"https://raw.githubusercontent.com/dltpdn/insightbook.opencv_project_python/master/img/{filename}"
        else:  # opencv 공식
            url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename
# 메인 실행
# ============================================================

# 이미지 로드 (파일 또는 웹캠)
img = cv.imread(get_sample('paper.jpg', repo='insightbook'))

if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

rows, cols = img.shape[:2]
draw = img.copy()

# 윈도우 표시 + 마우스 콜백 등록

cv.imshow(win_name, img)
cv.setMouseCallback(win_name, onMouse)    # 마우스 콜백 함수를 GUI 윈도우에 등록 ---④
cv.waitKey(0)
cv.destroyAllWindows()

# print("📝 사용법:")
# print("1. 이미지 위에 4개 점을 클릭하세요 (좌상단, 우상단, 우하단, 좌하단 순서 무관)")
# print("2. 4번째 점 클릭 후 자동으로 문서 스캔이 실행됩니다.")
# print("3. 'Scanned Document' 윈도우에서 결과를 확인하세요.")
#
# cv.waitKey(0)
# cv.destroyAllWindows()
