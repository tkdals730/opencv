import cv2 as cv
import glob

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame. Exiting ...")
        break
    # 좌우 반전
    frame = cv.flip(frame, 1)
    cv.imshow('frame', frame)

    key = cv.waitKey(1)
    # 종료
    if key == ord('q'):
        break
    # 캡쳐
    if key == ord('c'):
        filename = 'my_photo.png'
        cv.imwrite(filename, frame)
        print(f"{filename} 저장!")
        break
        

cap.release()
cv.destroyAllWindows()