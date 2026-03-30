import cv2 as cv
import glob

# 이미 저장된 capture_*.jpg 파일 개수 확인
existing_files = glob.glob("capture_*.jpg")
count = len(existing_files)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    frame = cv.flip(frame, 0)
    cv.imshow('frame', frame)

    key = cv.waitKey(1)

    if key == ord('q'):
        break

    if key == ord('c'):
        filename = f'capture_{count}.jpg'
        cv.imwrite(filename, frame)
        print(f"{filename} 저장!")
        count += 1

cap.release()
cv.destroyAllWindows()