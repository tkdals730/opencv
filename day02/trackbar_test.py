# 응용: 트랙바로 HSV 범위 실시간 조절
# 트랙바 6개(H_min, H_max, S_min, S_max, V_min, V_max)를 만들어 웹캠 영상에서 원하는 색상만 실시간으로 필터링합니다.

# 웹캠 루프 안에서 트랙바 값을 읽어 cv2.inRange()에 적용
# 결과를 나란히 표시: 원본 | 마스크 | 필터링 결과



# 콜백 함수 (트랙바용 — 빈 함수)
# def nothing(x):
#     pass

# 창 생성 (namedWindow)

# 트랙바 6개 생성
# — H_min (0~179, 초기값 0)
# — H_max (0~179, 초기값 179)
# — S_min (0~255, 초기값 50)
# — S_max (0~255, 초기값 255)
# — V_min (0~255, 초기값 50)
# — V_max (0~255, 초기값 255)

# 웹캠 연결

# 반복문
    # 프레임 읽기

    # BGR → HSV 변환

    # 트랙바 6개의 현재 값 가져오기 (getTrackbarPos)

    # lower, upper 배열 만들기
    # — lower = np.array([H_min, S_min, V_min])
    # — upper = np.array([H_max, S_max, V_max])

    # inRange로 마스크 생성
    # bitwise_and로 필터링

    # 원본 | 마스크 | 결과 나란히 표시

    # 'q' → 종료

# 카메라 해제 + 창 닫기
