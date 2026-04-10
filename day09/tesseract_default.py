import cv2
import numpy as np 
import pytesseract

# Tesseract 경로 설정 (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 이미지 로드
img = np.fromfile('01가0785.jpg', dtype=np.uint8)
img = cv2.imdecode(img, cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 기본 OCR
text = pytesseract.image_to_string(gray)
print(f"인식 결과: {text}")

# 상세 정보 (신뢰도 포함)
data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
print(f"신뢰도: {data['conf']}")  # 각 글자의 신뢰도