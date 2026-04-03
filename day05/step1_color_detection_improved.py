# 1.라이브러리 import
import cv2 as cv
import numpy as np
# 2.웹캠을 열기
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

def nothing(x):
    pass

# 트랙바 만들기
cv.namedWindow('Trackbar')
cv.createTrackbar('H_min', 'Trackbar', 35, 179, nothing)
cv.createTrackbar('H_max', 'Trackbar', 85, 179, nothing)
cv.createTrackbar('S_min', 'Trackbar', 50, 255, nothing)
cv.createTrackbar('S_max', 'Trackbar', 255, 255, nothing)
cv.createTrackbar('V_min', 'Trackbar', 50, 255, nothing)
cv.createTrackbar('V_max', 'Trackbar', 255, 255, nothing)

# 반복:
#   웹캠에서 프레임 읽기
while True:
    #   웹캠에서 프레임 읽기
    ret, frame = cap.read()
    

        # ROI 좌표 및 크기 설정 
    x = 300
    y = 100
    w = 50
    h = 50

    # ROI 추출 : [ 높이 시작 : 높이 끝, 너비 시작: 너비 끝 ]
    roi = frame[y:y+h, x:x+w]

    #   HSV 색공간으로 변환
    hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # 트랙바 값 읽기
    h_min = cv.getTrackbarPos('H_min', 'Trackbar')
    h_max = cv.getTrackbarPos('H_max', 'Trackbar')
    s_min = cv.getTrackbarPos('S_min', 'Trackbar')
    s_max = cv.getTrackbarPos('S_max', 'Trackbar')
    v_min = cv.getTrackbarPos('V_min', 'Trackbar')
    v_max = cv.getTrackbarPos('V_max', 'Trackbar')

    # 3.감지할 색상의 HSV 범위 설정
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    #   마스크 픽셀 면적 계산
#   면적과 임계값 비교하여 상태 결정
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 이진화 (Otsu 사용)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # 컨투어 검출
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 🔴 디버그 1: 검출된 전체 contour 개수
    print(f"\n[프레임 분석] 검출된 contour 개수: {len(contours)}")

    # 가장 큰 컨투어 찾기
    largest_cnt = None
    max_area = 0
    valid_count = 0  # 조건 만족하는 contour 개수

    for idx, cnt in enumerate(contours):
        area = cv.contourArea(cnt)
        # 🔴 디버그 2: 각 contour의 면적
        print(f"  contour[{idx}] 면적: {area:.1f}", end="")

        if area > 50:
            valid_count += 1
            print(f" ✓ (조건 만족)", end="")
        print()  # 줄 바꿈

        if area > max_area:
            max_area = area
            largest_cnt = cnt

    # 🔴 디버그 3: 조건 만족하는 contour 개수
    print(f"[조건 만족 (면적 > 50): {valid_count}개]")

    # 중심좌표 계산 (최소 크기 필터) - 루프 밖으로 이동!
    if largest_cnt is not None and max_area > 50:
        M = cv.moments(largest_cnt)
        # 🔴 디버그 4: moments 값
        print(f"[moments] m00={M['m00']:.1f}, m10={M['m10']:.1f}, m01={M['m01']:.1f}")

        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # 🔴 디버그 5: 중심점과 면적
            print(f"[빨간점 그림] 중심: ({cx}, {cy}), 면적: {max_area:.1f}")

            # 컨투어 그리기
            cv.drawContours(frame, [largest_cnt], 0, (0, 255, 0), 2)

            # 중심점 그리기 (빨강)
            cv.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

            # 좌표 표시
            cv.putText(frame, f'Center: ({cx}, {cy})', (10, 30),
                    cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(frame, f'Area: {max_area:.0f}', (10, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        print("[⚠️  조건 만족 contour 없음 - 빨간점 미표시]")
    
  
    
    
    #   마스크 생성 (특정 색상만 추출)
    mask = cv.inRange(hsv, lower, upper)

      # 마스크 픽셀 면적 계산
    area = cv.countNonZero(mask)

    # 임계값
    area_threshold = 500

    inverted = cv.bitwise_not(frame)
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (5,5))
    opened = cv.morphologyEx(inverted, cv.MORPH_OPEN, kernel)

     # 상태 결정
    if area > area_threshold:
        status = "DETECTED"
        color = (0, 255, 0)
    else:
        status = "NOT DETECTED"
        color = (0, 0, 255)

    # 터미널 출력
    print(f"Area: {area}, Status: {status}")

    # 화면 출력
    cv.putText(frame, f"Status: {status}", (10, 100),
            cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # 결과 화면
    result = cv.bitwise_and(roi, roi, mask=mask)

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    key = cv.waitKey(1)
    # q 누르면 종료
    if key & 0xFF == ord('q'):
        break



#   면적과 임계값 비교하여 상태 결정

    print(roi.shape)

    # ROI 영역에 사각형 그리기 
    cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

   
    #   상태를 터미널과 화면에 표시
    cv.imshow('frame',frame)
    cv.imshow('Mask',mask)
    cv.imshow('Result',result)
    cv.imshow("opening", opened)


# 리소스 해제
cap.release()
cv.destroyAllWindows()
