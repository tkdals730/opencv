import urllib.request
import os
import cv2

def download_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

# 사용할 샘플 이미지
img = cv2.imread(download_sample("smarties.png"), cv2.IMREAD_GRAYSCALE)