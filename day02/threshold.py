import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import urllib.request
import os

# 이미지 불러오기 
# github sample 주소 : https://github.com/opencv/opencv/tree/master/samples/data
def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

img = get_sample('gradient.png')
img = cv.imread('gradient.png', cv.IMREAD_GRAYSCALE)

assert img is not None, "file could not be read, check with os.path.exists()"
ret,thresh1 = cv.threshold(img,20,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,50,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,80,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,90,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,120,255,cv.THRESH_TOZERO_INV)
 
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
 
for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
 
plt.show()