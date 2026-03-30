import cv2 as cv

# my_photo.png 읽기
img = cv.imread(r"C:\Users\405\project\opencv_programming\day01\my_photo.png")

if img is None:
    print("이미지를 불러오지 못했습니다.")
    exit()

# 이미지 높이(h), 너비(w) 가져오기
h, w = img.shape[:2]

# --- 하단 반투명 배경 바 ---
# 1) overlay = img.copy()
overlay = img.copy()

# 2) overlay 하단 80px 영역에 검정 사각형 채우기
cv.rectangle(overlay, (0, h-80), (w, h), (0, 0, 0), -1)

# 3) addWeighted로 img와 overlay를 50:50 합성
cv.addWeighted(overlay, 0.5, img, 0.5, 0, img)

# --- 텍스트 ---
font = cv.FONT_HERSHEY_SIMPLEX

# 이름 텍스트
cv.putText(img, 'YH', (20, h-35), font, 1.5, (255, 255, 255), 2, cv.LINE_AA)

# 소속 텍스트
cv.putText(img, 'asd', (20, h-10), font, 0.8, (255, 255, 255), 2, cv.LINE_AA)

# 결과 표시
cv.imshow("Drawing", img)

# 저장
cv.imwrite("my_id_card.png", img)

# 키 입력 대기
cv.waitKey(0)

# 창 닫기
cv.destroyAllWindows()