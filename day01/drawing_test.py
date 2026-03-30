import numpy as np
import cv2 as cv

# 대각선( 좌상단 -> 우하단, 노란색, 두꼐 2)

# 타원 (캔버스 중앙, 가로 150 세로 80 흰색 )

# 삼각형


# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
# BGR
cv.line(img,(0,0),(511,511),(0, 255, 255),2)
# 네모
cv.rectangle(img,(384,0),(510,128),(0,255,0),3)
# 동그라미
cv.circle(img,(447,63), 63, (0,0,255), -1)
# 타원
cv.ellipse(img,(256,256),(150,80),0,0,180,255,-1)
# 폴리건????
pts = np.array([[250,15],[30,40],[70,20]], np.int32)
pts = pts.reshape((-1,1,2))
cv.polylines(img,[pts],True,(0,255,0))

font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA)

# 보여주는 명령어
cv.imshow("Drawing", img)
# 대기
cv.waitKey(0)
cv.destroyAllWindows()
