import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 직접 저장한 이미지라면 get_sample 말고 그냥 읽기
img1_color = cv.imread('step2.png')
img2_color = cv.imread('step2_1.jpg')

if img1_color is None or img2_color is None:
    print("Error: 이미지를 찾을 수 없습니다.")
    exit()

img1 = cv.cvtColor(img1_color, cv.COLOR_BGR2GRAY)
img2 = cv.cvtColor(img2_color, cv.COLOR_BGR2GRAY)

print(f"img1 shape: {img1.shape}, img2 shape: {img2.shape}")

# SIFT
sift = cv.SIFT_create()

# 특징점/디스크립터
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

print(f"Keypoints found - img1: {len(kp1)}, img2: {len(kp2)}")

# FLANN
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)

# knn match
matches = flann.knnMatch(des1, des2, k=2)
print(f"Total matches: {len(matches)}")

# Lowe ratio test
good_matches = []
for pair in matches:
    if len(pair) == 2:
        m, n = pair
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

print(f"Good matches after Lowe's ratio test: {len(good_matches)}")

MIN_MATCH_COUNT = 10

if len(good_matches) >= MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

    if M is not None:
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, M)

        # 오른쪽 이미지에 파란 박스
        result_img = img2_color.copy()
        cv.polylines(result_img, [np.int32(dst)], True, (255, 0, 0), 3)

        matchesMask = mask.ravel().tolist()

        # inlier만 그리기
        res2 = cv.drawMatches(
            img1_color, kp1,
            result_img, kp2,
            good_matches, None,
            matchesMask=matchesMask,
            flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
        )

        plt.figure(figsize=(14, 8))
        plt.imshow(cv.cvtColor(res2, cv.COLOR_BGR2RGB))
        plt.title('Matching-Inlier')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        inlier_count = sum(matchesMask)
        outlier_count = len(matchesMask) - inlier_count
        print(f"Inliers: {inlier_count}, Outliers: {outlier_count}")

    else:
        print("Failed to compute homography")
else:
    print(f"Not enough matches ({len(good_matches)}/{MIN_MATCH_COUNT})")