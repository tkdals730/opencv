import numpy as np
import cv2 as cv

drawing = False
mode = True
ix, iy = -1, -1

img = np.zeros((512, 512, 3), np.uint8)
temp_img = img.copy()

def draw_shape(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, temp_img

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = img.copy()   # 원본 복사
            if mode:
                cv.rectangle(temp_img, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                cv.circle(temp_img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        else:
            cv.circle(img, (x, y), 5, (0, 0, 255), -1)

        temp_img = img.copy()

cv.namedWindow('image')
cv.setMouseCallback('image', draw_shape)

while True:
    cv.imshow('image', temp_img)
    k = cv.waitKey(1) & 0xFF

    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv.destroyAllWindows()