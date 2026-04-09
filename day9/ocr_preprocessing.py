import cv2
import numpy as np 
import pytesseract


# Tesseract 경로 설정 (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 번호판 이미지 가져오기 
img = np.fromfile('01가0785.jpg', dtype=np.uint8)
img = cv2.imdecode(img, cv2.IMREAD_COLOR)

# 1단계 : 그레이스케일 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Step1 : Grayscale', gray)

# 2단계 : CLAHE대비 최대화 
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
contrast = clahe.apply(gray)
cv2.imshow('Step2 : CLAHE', contrast)

# 3단계 : 적응형 임계처리
binary = cv2.adaptiveThreshold(contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 11)
cv2.imshow('Step3 : binary', binary)

# 4단계: 윤곽선 검출 및 필터링
contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

filtered = np.zeros_like(binary)
for contour in contours:
    area = cv2.contourArea(contour)
    if 100 < area < 500:
        cv2.drawContours(filtered, [contour], 0, 255, -1)
cv2.imshow('Step4 : filtered', filtered)


cv2.waitKey(0)
cv2.destroyAllWindows()