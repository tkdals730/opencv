import cv2
import numpy as np
import os

# Cascade 분류기 로드 함수

def load_cascade(cascade_name='haarcascade_frontalface_default.xml'):

    """Haar Cascade 분류기 로드"""

    cascade_path = cv2.data.haarcascades + cascade_name

    cascade = cv2.CascadeClassifier(cascade_path)

    if cascade.empty():

        print(f"Error: {cascade_name} 로드 실패")

        return None

    return cascade

# 폴더 생성 함수

def create_folders(paths):

    """필요한 폴더 생성"""

    for path in paths:

        if not os.path.exists(path):

            os.makedirs(path)
