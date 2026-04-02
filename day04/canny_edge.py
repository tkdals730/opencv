import urllib.request
import os
import numpy as np 
import cv2 as cv 

def get_sample(filename, repo='opencv'):
    if not os.path.exists(filename):
        if repo == 'insightbook':
            url = f"https://raw.githubusercontent.com/dltpdn/insightbook.opencv_project_python/master/img/{filename}"
        else:  # opencv 공식
            url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

#img = cv.imread(get_sample('messi5.jpg', repo='opencv'))
img = cv.imread(get_sample('messi5.jpg'))
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# 가우시안 블러? 왜하는거지 근데?
blurred = cv.GaussianBlur(gray, (5,5), 1.5)

# 캐니엣지
edge = cv.Canny(blurred,00,150)

cv.imshow("Original", img)
#cv.imshow("Scaling", res)
#cv.imshow("Traslated", dst)
#cv.imshow("Rotated", dst)
cv.imshow("blurred", blurred)
cv.imshow("Canny", edge)

cv.waitKey(0)
cv.destroyAllWindows()