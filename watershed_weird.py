import numpy as np
import cv2


def getRegionalMinima(img):
    h, w = img.shape[:2]
    markers = np.zeros((h, w), np.int32)
    labels = 1  # local min pixel location
    # padding with the  pixel value
    img2 = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    for i in range(1, h + 1):
        for j in range(1, w + 1):
            min_8 = min(img2[i + 1, j], img2[i - 1, j], img2[i, j + 1], img2[i, j - 1], img2[i + 1, j + 1],
                        img2[i - 1, j - 1], img2[i + 1, j - 1], img2[i - 1, j + 1])
            #finding local min for pixels
            if img[i - 1, j - 1] <= min_8:
                markers[i - 1, j - 1] = labels
                labels += 1

    return markers


def iterativeMinFollowing(img, markers):
    h, w = img.shape[:2]
    img2 = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    output = markers.copy()
    labeled = 0
    while labeled < h * w:
        for i in range(h):
            for j in range(w):
                if output[i, j] != 0:
                    labeled += 1
                else:
                    x, y = trace(h, w, i + 1, j + 1, img2)
                    if output[x, y] != 0:
                        output[i, j] = output[x, y]
                        labeled += 1
        count = h * w - labeled
        print("remaing ", count)
    return output


def trace(h, w, i, j, img2):
    min_val = img2[i, j]
    x, y = i, j
    for a in range(i - 1, i + 2):
        for b in range(j - 1, j + 2):
            if img2[a, b] < min_val:
                min_val = img2[a, b]
                x, y = a, b
    return x - 1, y - 1
    
           
 