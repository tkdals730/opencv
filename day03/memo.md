| 용어 | 뜻 | 한 줄 설명 |
|------|----|-----------|
| 컨투어 (Contour) | 물체의 외곽선 | 이진 이미지에서 검정(0)과 흰색(255)의 경계 |
| findContours() | 컨투어 찾기 | 이진 이미지에서 모든 외곽선을 찾아 리스트로 반환 |
| 모멘트 (Moment) | 형상의 중심/넓이 정보 | cv2.moments()로 계산되는 기하학적 특징값 |
| 중심좌표 (Centroid) | 물체의 무게중심 | 모멘트 M10, M01에서 계산: cx = M10/M00, cy = M01/M00 |
| 바운딩박스 (Bounding Box) | 물체를 감싸는 가장 작은 직사각형 | 물체의 위치와 크기를 빠르게 파악 |
| 면적 (Area) | 컨투어 내부의 픽셀 수 | cv2.contourArea() 또는 모멘트 M00 |
| 둘레 (Perimeter) | 컨투어의 외곽선 길이 | cv2.arcLength()로 계산 |
| 계층구조 (Hierarchy) | 컨투어 간의 포함 관계 | 부모-자식 관계: RETR_EXTERNAL vs RETR_TREE |
| RETR_EXTERNAL | 가장 바깥 컨투어만 | 내부 자식 컨투어는 무시 |
| RETR_TREE | 모든 컨투어와 계층 | 전체 포함 관계를 트리로 표현 |
| ROI (Region of Interest) | 관심 영역 | 이미지에서 처리하고 싶은 특정 부분만 잘라냄 |
| 히스토그램 (Histogram) | 밝기별 픽셀 수 그래프 | 이미지의 밝기 분포를 파악 |