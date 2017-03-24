import numpy as np
import cv2

use_noisy_input = 0

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector_create()

fast.setThreshold(12)
fast.setType(cv2.FAST_FEATURE_DETECTOR_TYPE_5_8)
# fast.setType(cv2.FAST_FEATURE_DETECTOR_TYPE_7_12)
# fast.setType(cv2.FAST_FEATURE_DETECTOR_TYPE_9_16)

col = (0, 255, 0)

img = cv2.imread('bear_0_warped_c8_s28_frame00001.jpg', 0)
img2 = cv2.imread('bear_0_warped_c8_s28_frame00051.jpg', 0)
img_kp = np.copy(img)
img2_kp = np.copy(img2)
kp = fast.detect(img, None)
img_kp = cv2.drawKeypoints(img, kp, img_kp, color=col)
kp2 = fast.detect(img2, None)
img2_kp = cv2.drawKeypoints(img2, kp2, img2_kp, color=col)
print "Total Keypoints: ", len(kp), len(kp2)
cv2.imshow('img_kp', img_kp)
cv2.imshow('img2_kp', img2_kp)
cv2.imwrite('img_kp.png', img_kp)
cv2.imwrite('img2_kp.png', img2_kp)

img_noisy = cv2.imread('bear_0_warped_c8_s28_gauss_frame00001.jpg', 0)
img2_noisy = cv2.imread('bear_0_warped_c8_s28_gauss_frame00051.jpg', 0)
img_noisy_kp = np.copy(img_noisy)
img2_noisy_kp = np.copy(img2_noisy)
kp = fast.detect(img_noisy, None)
img_noisy_kp = cv2.drawKeypoints(img_noisy, kp, img_noisy_kp, color=col)
kp2 = fast.detect(img2_noisy, None)
img2_noisy_kp = cv2.drawKeypoints(img2_noisy, kp2, img2_noisy_kp, color=col)
print "Total Noisy Keypoints: ", len(kp), len(kp2)
cv2.imshow('img_noisy_kp', img_noisy_kp)
cv2.imshow('img2_noisy_kp', img2_noisy_kp)
cv2.imwrite('img2_noisy_kp.png', img2_noisy_kp)
cv2.imwrite('img_noisy_kp.png', img_noisy_kp)

if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
    exit()