import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage.morphology
import watershed
import scipy.ndimage


def imregionalmin(img, size):
    return img == scipy.ndimage.filters.minimum_filter(img, size, mode='constant')

watershed_method = 0

img = cv2.imread('coins.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# noise removal
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# sure background area
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)
# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers + 1

# Now, mark the region of unknown with zero
markers[unknown == 255] = 0

print 'img.shape: ', img.shape
print 'markers.shape: ', markers.shape

print 'min(markers)', np.min(markers)
print 'max(markers)', np.max(markers)

sig = 3
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.uint8)
J = cv2.GaussianBlur(img_gray, (int(2 * round(3 * sig) + 1), int(2 * round(3 * sig) + 1)), sig,
                     borderType=cv2.BORDER_REPLICATE)
[Jy, Jx] = np.gradient(J)
G = np.square(Jx) + np.square(Jy)

# G_regional_min = imregionalmin(G, 3).astype(np.uint8)
# print 'min(G_regional_min)', np.min(G_regional_min)
# print 'max(G_regional_min)', np.max(G_regional_min)
# print 'G_regional_min:\n', G_regional_min
# G_ret, G_markers = cv2.connectedComponents(G_regional_min)

G_markers = watershed.getRegionalMinima(G)
# print 'G_markers:\n', G_markers
print 'min(G_markers)', np.min(G_markers)
print 'max(G_markers)', np.max(G_markers)

# G2 = np.loadtxt('watershed_ex.txt', dtype=np.uint8, delimiter='\t')
# print 'G2.shape: ', G2.shape
# print 'G2:\n', G2
#
# G_markers2 = watershed.getRegionalMinima(G2)
# print 'G_markers2:\n', G_markers2
# print 'min(G_markers2)', np.min(G_markers2)
# print 'max(G_markers2)', np.max(G_markers2)

if watershed_method == 0:
    L = watershed.iterative_check_min(G, G_markers)
    # L -= 2
elif watershed_method == 1:
    L = watershed.iterative_check_all(G, G_markers)
    # L -= 2
elif watershed_method == 2:
    L = watershed.recursive(G, G_markers)
    # L -= 2
elif watershed_method == 3:
    L = skimage.morphology.watershed(img_gray, markers)
    # L -= 2
else:
    L = cv2.watershed(img, markers)

print 'L:\n', L

print 'min(L)', np.min(L)
print 'max(L)', np.max(L)

img[markers == -1] = [255, 0, 0]

cv2.imshow('img', img)
cv2.waitKey(0)
