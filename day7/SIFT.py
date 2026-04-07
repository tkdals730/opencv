import numpy as np
import cv2 as cv
from sample_download import get_sample


img = cv.imread(get_sample('home.jpg', repo='opencv'))
gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
 
sift = cv.SIFT_create()
kp = sift.detect(gray,None)
kp, des = sift.compute(gray,kp)

# 위에 두개를 합친게 이거임
# kp, des = sift.detectAndCompute(gray,None)


print(kp)
# img=cv.drawKeypoints(gray,kp,img)
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
cv.imwrite('sift_keypoints2.jpg',img)