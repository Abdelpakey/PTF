import numpy as np
import cv2
from part3_utils import getOject
from part3_utils import getRectangularApproximation
from part3_utils import drawMatches

# set to appropriate number if multiple cameras are present
camera_id = 1
# set to 0 to select initial patch from camera image
read_patch_from_disk = 1
# name of the initial image file
init_img_name = 'part3.jpg'

filter_matches = 0
enable_blurring = 0
min_match_count = 10
curr_img_as_training = 1

# ORB parameters
nfeatures = 1000
scaleFactor = 1.2
nlevels = 12
edgeThreshold = 31
firstLevel = 0
WTA_K = 2
scoreType = cv2.ORB_HARRIS_SCORE
patchSize = 31
fastThreshold = 20

# FLANN parameters
table_number = 6
key_size = 12
multi_probe_level = 1
# table_number = 12
# key_size = 20
# multi_probe_level = 2


cap = cv2.VideoCapture()
if not cap.open(camera_id):
    print 'The Camera ', camera_id, ' could not be opened'
    exit()

orb = cv2.ORB_create(nfeatures=nfeatures, scaleFactor=scaleFactor, nlevels=nlevels,
                     edgeThreshold=edgeThreshold, firstLevel=firstLevel, WTA_K=WTA_K,
                     scoreType=scoreType, patchSize=patchSize, fastThreshold=fastThreshold)
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH,
                    table_number=table_number,
                    key_size=key_size,
                    multi_probe_level=multi_probe_level)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

if read_patch_from_disk:
    src_img = cv2.imread(init_img_name)  # queryImage
else:
    ret, src_img = cap.read()
    sel_pts = getOject(src_img)
    init_corners = np.asarray(sel_pts).astype(np.float64).T
    [min_x, min_y, max_x, max_y] = getRectangularApproximation(init_corners)
    src_img = src_img[int(min_y):int(max_y) + 1, int(min_x):int(max_x) + 1, :]

h, w, ch = src_img.shape
if enable_blurring:
    src_img_blurred = cv2.GaussianBlur(src_img, (3, 3), 3)
else:
    src_img_blurred = src_img
src_kp, src_desc = orb.detectAndCompute(src_img_blurred, None)

while True:
    ret, curr_img = cap.read()
    if enable_blurring:
        curr_img_blurred = cv2.GaussianBlur(curr_img, (3, 3), 3)
    else:
        curr_img_blurred = curr_img
    curr_kp, curr_desc = orb.detectAndCompute(curr_img_blurred, None)

    if curr_img_as_training:
        training_kp = curr_kp
        training_desc = curr_desc
        query_kp = src_kp
        query_desc = src_desc
    else:
        training_kp = src_kp
        training_desc = src_desc
        query_kp = curr_kp
        query_desc = curr_desc


    matches = flann.knnMatch(query_desc, training_desc, k=2)

    if filter_matches:
        good_matches = []
        for match in matches:
            if len(match) == 2:
                m = match[0]
                n = match[1]
                if m.distance < 0.7 * n.distance:
                    good_matches.append(match)
    else:
        good_matches = matches

    if len(good_matches) > min_match_count:
        src_pts = []
        dst_pts = []

        for match in good_matches:
            if curr_img_as_training:
                src_pt_id = match[0].queryIdx
                curr_pt_id = match[0].trainIdx
            else:
                src_pt_id = match[0].trainIdx
                curr_pt_id = match[0].queryIdx
            try:
                if match:
                    src_pts.append(src_kp[src_pt_id].pt)
                    dst_pts.append(curr_kp[curr_pt_id].pt)
                else:
                    continue
            except IndexError:
                print 'IndexError in match'
                exit()

        src_pts = np.float32(src_pts).reshape(-1, 1, 2)
        dst_pts = np.float32(dst_pts).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        # print 'dst: ',dst

        curr_img_annotated = cv2.polylines(curr_img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
    else:
        print "Not enough matches are found - %d/%d" % (len(good_matches), min_match_count)
        curr_img_annotated = curr_img
        matchesMask = None

    disp_img = drawMatches(src_img, src_kp, curr_img_annotated, curr_kp, good_matches, curr_img_as_training,
                           matchesMask, (0, 255, 0))

    cv2.imshow('Matched Features', disp_img)
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('r'):
        init_corners = np.asarray(sel_pts).astype(np.float64).T
        [min_x, min_y, max_x, max_y] = getRectangularApproximation(dst)
        src_img = curr_img[int(min_y):int(max_y) + 1, int(min_x):int(max_x) + 1, :]
        h, w, ch = src_img.shape
        if enable_blurring:
            src_img_blurred = cv2.GaussianBlur(src_img, (3, 3), 3)
        else:
            src_img_blurred = src_img
        src_kp, src_desc = orb.detectAndCompute(src_img_blurred, None)


