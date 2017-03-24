import numpy as np
import cv2

# adapted from: https://gist.github.com/CannedYerins/11be0c50c4f78cad9549
def drawMatches(src_img, src_kp, curr_img, curr_kp, matches, curr_img_as_training, matchesMask, color=None):
    """Draws lines between matching keypoints of two images.
    Keypoints not in a matching pair are not drawn.
    Places the images side by side in a new image and draws circles
    around each keypoint, with line segments connecting matching pairs.
    You can tweak the r, thickness, and figsize values as needed.
    Args:
        img1: An openCV image ndarray in a grayscale or color format.
        kp1: A list of cv2.KeyPoint objects for img1.
        img2: An openCV image ndarray of the same format and with the same
        element type as img1.
        kp2: A list of cv2.KeyPoint objects for img2.
        matches: A list of DMatch objects whose trainIdx attribute refers to
        img1 keypoints and whose queryIdx attribute refers to img2 keypoints.
        color: The color of the circles and connecting lines drawn on the images.
        A 3-tuple for color images, a scalar for grayscale images.  If None, these
        values are randomly generated.
    """
    # We're drawing them side by side.  Get dimensions accordingly.
    # Handle both color and grayscale images.
    if len(src_img.shape) == 3:
        new_shape = (max(src_img.shape[0], curr_img.shape[0]), src_img.shape[1] + curr_img.shape[1], src_img.shape[2])
    elif len(src_img.shape) == 2:
        new_shape = (max(src_img.shape[0], curr_img.shape[0]), src_img.shape[1] + curr_img.shape[1])
    new_img = np.zeros(new_shape, type(src_img.flat[0]))
    # Place images onto the new image.
    new_img[0:src_img.shape[0], 0:src_img.shape[1]] = src_img
    new_img[0:curr_img.shape[0], src_img.shape[1]:src_img.shape[1] + curr_img.shape[1]] = curr_img

    # Draw lines between matches.  Make sure to offset kp coords in second image appropriately.
    r = 15
    thickness = 2
    if color:
        c = color
    for m, mask in zip(matches, matchesMask):
        if not m or not mask:
            continue
        # Generate random color for RGB/BGR and grayscale images as needed.
        if not color:
            c = np.random.randint(0, 256, 3) if len(src_img.shape) == 3 else np.random.randint(0, 256)
        # So the keypoint locs are stored as a tuple of floats.  cv2.line(), like most other things,
        # wants locs as a tuple of ints.

        if curr_img_as_training:
            end1 = tuple(np.round(src_kp[m[0].queryIdx].pt).astype(int))
            end2 = tuple(np.round(curr_kp[m[0].trainIdx].pt).astype(int) + np.array([src_img.shape[1], 0]))
        else:
            end1 = tuple(np.round(src_kp[m[0].trainIdx].pt).astype(int))
            end2 = tuple(np.round(curr_kp[m[0].queryIdx].pt).astype(int) + np.array([src_img.shape[1], 0]))
        cv2.line(new_img, end1, end2, c, thickness)
        # cv2.circle(new_img, end1, r, c, thickness)
        # cv2.circle(new_img, end2, r, c, thickness)

    return new_img


def getRectangularApproximation(corners_in):
    center_x = np.mean(corners_in[0, :])
    center_y = np.mean(corners_in[1, :])

    mean_width = (abs(corners_in[0, 0] - center_x) + abs(corners_in[0, 1] - center_x)
                  + abs(corners_in[0, 2] - center_x) + abs(corners_in[0, 3] - center_x)) / 2.0
    mean_height = (abs(corners_in[1, 0] - center_y) + abs(corners_in[1, 1] - center_y)
                   + abs(corners_in[1, 2] - center_y) + abs(corners_in[1, 3] - center_y)) / 2.0

    min_x = center_x - mean_width / 2.0
    max_x = center_x + mean_width / 2.0
    min_y = center_y - mean_height / 2.0
    max_y = center_y + mean_height / 2.0

    return [min_x, min_y, max_x, max_y]


def getOject(img, col=(0, 0, 255), title=None, line_thickness=1):
    annotated_img = img.copy()
    temp_img = img.copy()
    if title is None:
        title = 'Select the object to track'
    cv2.namedWindow(title)
    cv2.imshow(title, annotated_img)
    pts = []

    def drawLines(img, hover_pt=None):
        if len(pts) == 0:
            cv2.imshow(title, img)
            return
        for i in xrange(len(pts) - 1):
            cv2.line(img, pts[i], pts[i + 1], col, line_thickness)
        if hover_pt is None:
            return
        cv2.line(img, pts[-1], hover_pt, col, line_thickness)
        if len(pts) == 3:
            cv2.line(img, pts[0], hover_pt, col, line_thickness)
        elif len(pts) == 4:
            return
        cv2.imshow(title, img)

    def mouseHandler(event, x, y, flags=None, param=None):
        if len(pts) >= 4:
            return
        if event == cv2.EVENT_LBUTTONDOWN:
            pts.append((x, y))
            temp_img = annotated_img.copy()
            drawLines(temp_img)
        elif event == cv2.EVENT_LBUTTONUP:
            pass
        elif event == cv2.EVENT_RBUTTONDOWN:
            if len(pts) > 0:
                print 'Removing last point'
                del (pts[-1])
            temp_img = annotated_img.copy()
            drawLines(temp_img)
        elif event == cv2.EVENT_RBUTTONUP:
            pass
        elif event == cv2.EVENT_MBUTTONDOWN:
            pass
        elif event == cv2.EVENT_MOUSEMOVE:
            # if len(pts) == 0:
            # return
            temp_img = annotated_img.copy()
            drawLines(temp_img, (x, y))

    cv2.setMouseCallback(title, mouseHandler, param=[annotated_img, temp_img, pts])
    while len(pts) < 4:
        key = cv2.waitKey(1)
        if key == 27:
            exit()
    cv2.waitKey(250)
    cv2.destroyWindow(title)
    drawLines(annotated_img, pts[0])
    return pts