| 용어 | 영문 | 뜻 |
|------|------|-----|
| 템플릿 매칭 | Template Matching | 템플릿 이미지를 큰 이미지 내에서 슬라이딩하며 유사도 계산 → 오브젝트 위치 탐지 |
| 매칭 방법 | Matching Method | 유사도 계산 방식: TM_SQDIFF, TM_CCORR, TM_CCOEFF 등 6가지 |
| 정규화 매칭 | Normalized Matching | TM_CCOEFF_NORMED → 조명 변화에 강한 정규화 버전 |
| 허프 변환 | Hough Transform | 이미지의 직선/원 같은 기하학적 형태를 자동으로 검출 |
| 극좌표 | Polar Coordinates | (ρ, θ) → 거리와 각도로 표현하는 좌표계 |
| 누산기 | Accumulator | 허프 변환에서 각 기하학적 형태의 "투표" 카운트 |
| 임계값 | Threshold | 누산기 값이 이 이상이어야 직선/원으로 인정 |
| 허프 직선 | Hough Lines | cv.HoughLines() → 극좌표 (ρ, θ)로 표현된 무한 직선 |
| 허프 선분 | Hough Lines P | cv.HoughLinesP() → 시작/끝 점 (x1, y1, x2, y2)로 표현 (더 실용적) |
| 허프 원 | Hough Circles | cv.HoughCircles() → 원의 중심 (x, y)과 반지름 r 검출 |
| 차선 인식 파이프라인 | Lane Detection Pipeline | 카메라 입력 → 전처리 → 에지 검출 → 허프 변환 → 차선 표시 |