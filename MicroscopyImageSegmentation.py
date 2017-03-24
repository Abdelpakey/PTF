import numpy as np
import scipy.ndimage
import cv2
import math
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
import skimage.morphology
import watershed_old as watershed


def getLoGKernel(ksize, sigma):
    kernel = np.zeros([int(ksize), int(ksize)], dtype=np.float32)
    range = int(ksize / 2.0)
    const_1 = 1.0 / (np.pi * (sigma ** 4))
    const_2 = 1.0 / (2 * sigma * sigma)
    i = 0
    for x in xrange(-range, range):
        j = 0
        for y in xrange(-range, range):
            factor = (x * x + y * y) * const_2
            kernel[i, j] = const_1 * (1 - factor) * math.exp(-factor)
            j += 1
        i += 1
    return kernel


def applyLoG(img, ksize, sigma):
    img_gauss = cv2.GaussianBlur(img, (ksize, ksize), sigma, borderType=cv2.BORDER_REPLICATE)
    return cv2.Laplacian(img_gauss, -1, ksize, borderType=cv2.BORDER_REPLICATE)


# print matplotlib.__version__

sig = 2.5
min_scale = 3
max_scale = 5
use_builtin_log = 1
adaptive_gauss_sigma = 1
min_filter_size = 12
scatter_size = 40
scatter_col = 'r'
use_combined_minimum = 1
# contour_col = (255, 255, 255)
contour_col = (0, 0, 0)

marker_method = 0
watershed_method = 3

G_min_filter_size = 10
min_area = 10
max_area = 50
use_sobel_grad = 0
exclude_interior_contours = 1
show_grad_as_binary = 1
use_skimage_min = 0
skimage_max_peaks = np.inf

# img_name = 'coins.jpg'
img_name = 'lab7.bmp'

fig_id = 0
fig = []

I_rgb = cv2.imread(img_name).astype(np.float32)
I = cv2.cvtColor(I_rgb, cv2.COLOR_BGR2GRAY)

J = cv2.GaussianBlur(I, (int(2 * round(3 * sig) + 1), int(2 * round(3 * sig) + 1)), sig,
                     borderType=cv2.BORDER_REPLICATE)

print 'J.dtype: ', J.dtype

fig.append(plt.figure(fig_id))
fig_id += 1
plt.subplot(2, 1, 1)
plt.imshow(I)
plt.title('Input Image')
plt.subplot(2, 1, 2)
plt.imshow(J)
plt.title('Blurred Image')

# Cell centre detection by Blob detector and fine tuning by Otsu
[h, w] = I.shape
K = np.zeros([h, w, 3])
for scale in xrange(min_scale, max_scale + 1):
    kernel_size = int(2 * math.floor(3 * scale) + 1)
    print 'kernel_size: ', kernel_size
    if use_builtin_log:
        if adaptive_gauss_sigma:
            gauss_sigma = scale
        else:
            gauss_sigma = sig
        K[:, :, scale - min_scale] = applyLoG(J, kernel_size, gauss_sigma)
    else:
        log_kernel = getLoGKernel(kernel_size, scale)
        K[:, :, scale - min_scale] = cv2.filter2D(J, -1, log_kernel)

fig.append(plt.figure(fig_id))
fig_id += 1
plt.subplot(3, 1, 1)
level1 = K[:, :, 0]
plt.imshow(level1)
plt.title('Level 1')
plt.subplot(3, 1, 2)
level2 = K[:, :, 1]
plt.imshow(level2)
plt.title('Level 2')
plt.subplot(3, 1, 3)
level3 = K[:, :, 2]
plt.imshow(level3)
plt.title('Level 3')
fig[-1].suptitle('LoG Pyramid')
#
# fig.append(plt.figure(fig_id))
# fig_id += 1
# plt.imshow(K, extent=[0, 1, 0, 1])
# plt.title('K (LoG)')


# local maxima within the volume
if use_combined_minimum:
    lm = scipy.ndimage.filters.minimum_filter(K, min_filter_size)
    A = (K == lm)
else:
    A = np.zeros(K.shape, dtype=np.bool)
    lm = scipy.ndimage.filters.minimum_filter(K[:, :, 0], min_filter_size)
    A[:, :, 0] = (K[:, :, 0] == lm)
    lm = scipy.ndimage.filters.minimum_filter(K[:, :, 1], min_filter_size)
    A[:, :, 1] = (K[:, :, 1] == lm)
    lm = scipy.ndimage.filters.minimum_filter(K[:, :, 2], min_filter_size)
    A[:, :, 2] = (K[:, :, 2] == lm)

# take minima within a range of scales and collapse those on x-y plane
B = np.sum(A, axis=2)

print 'min A: ', np.min(A)
print 'max A: ', np.max(A)
print 'min B: ', np.min(B)
print 'max B: ', np.max(B)

fig.append(plt.figure(fig_id))
fig_id += 1
plt.subplot(2, 2, 1)
level1 = A[:, :, 0]
# print 'min level1: ', np.min(level1)
# print 'max level1 ', np.max(level1)
plt.imshow(level1, cmap='Greys')
plt.title('Level 1')
plt.subplot(2, 2, 2)
level2 = A[:, :, 1]
# print 'min level1: ', np.min(level2)
# print 'max level1 ', np.max(level2)
plt.imshow(level2, cmap='Greys')
plt.title('Level 2')
plt.subplot(2, 2, 3)
level3 = A[:, :, 2]
# print 'min level1: ', np.min(level3)
# print 'max level1 ', np.max(level3)
plt.imshow(level3, cmap='Greys')
plt.title('Level 3')
plt.subplot(2, 2, 4)
plt.imshow(B, cmap='Greys')
# plt.title('Sum')
fig[-1].suptitle('Regional minima in the LoG Pyramid')

[y, x] = B.nonzero()
fig.append(plt.figure(fig_id))
fig_id += 1
plt.imshow(I)
# plt.hold(True)
plt.scatter(x, y, marker='.', color=scatter_col, s=scatter_size)
plt.xlim([0, I.shape[1]])
plt.ylim([0, I.shape[0]])
# plt.plot(x, y, marker='.', color='r'])
# plt.hold(False)
plt.grid(b=False)
plt.title('Rough blobs detected in the image')

# remove spurious maxima by working with Otsu threshold
t, J_otsu = cv2.threshold(J.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print 't: ', t
B = np.multiply(B, J >= t)

# cv2.imshow('B_otsu', B_otsu)
# cv2.imshow('B np.multiply', B.astype(np.float32))

[y, x] = B.nonzero()
fig.append(plt.figure(fig_id))
fig_id += 1
plt.imshow(I)
# plt.hold(True)
plt.scatter(x, y, marker='.', color=scatter_col, s=scatter_size)
plt.xlim([0, I.shape[1]])
plt.ylim([0, I.shape[0]])
# plt.plot(x, y, marker='.', color='r')
# plt.hold(False)
plt.grid(b=False)
plt.title('Refined blobs detected in the image')

fig.append(plt.figure(fig_id))
fig_id += 1
plt.imshow(J_otsu, cmap='Greys')
plt.title('Otsu')

print 'n_refined_blobs: ', len(y)

np.savetxt('B.txt', B, fmt='%d', delimiter='\t')


# --------------------------- end of assignment 6 --------------------------- #

def imreconstruct(marker, mask):
    curr_marker = np.copy(marker).astype(mask.dtype)
    kernel = np.ones([3, 3])
    while True:
        next_marker = cv2.dilate(curr_marker, kernel, iterations=1)
        intersection = next_marker > mask
        next_marker[intersection] = mask[intersection]
        if np.array_equal(next_marker, curr_marker):
            return curr_marker
        curr_marker = np.copy(next_marker)
    return curr_marker


def imimposemin(marker, mask):
    fm = np.copy(mask)
    fm[marker] = -np.inf
    fm[np.invert(marker)] = np.inf
    if mask.dtype == np.float32 or mask.dtype == np.float64:
        range = float(np.max(mask) - np.min(mask))
        print 'range: ', range
        if range == 0:
            h = 0.1
        else:
            h = range * 0.001
    else:
        # Add 1 to integer images.
        h = 1
    print 'h: ', h
    fp1 = mask + h
    g = np.minimum(fp1, fm)
    return np.invert(imreconstruct(
        np.invert(fm.astype(np.uint8)), np.invert(g.astype(np.uint8))
    ).astype(np.uint8))


def imregionalmin(img, size):
    if use_skimage_min:
        return peak_local_max(np.invert(img), min_distance=size, indices=False,
                              exclude_border=False, num_peaks=skimage_max_peaks)
    else:
        return img == scipy.ndimage.filters.minimum_filter(img, size, mode='constant')

# Now segment cells by marker controlled watershed
# Marker controlled segmentation
if use_sobel_grad:
    Jx = cv2.Sobel(J, cv2.CV_32F, 1, 0, ksize=5)
    Jy = cv2.Sobel(J, cv2.CV_32F, 0, 1, ksize=5)
else:
    [Jy, Jx] = np.gradient(J)

G = np.square(Jx) + np.square(Jy)
# G[G > 0] = 1
fig.append(plt.figure(fig_id))
fig_id += 1
plt.subplot(2, 2, 1)
plt.imshow(1 - G, cmap='Greys')
plt.title('G')

print 'G.dtype', G.dtype
print 'B.dtype', B.dtype

G_rec = imreconstruct(B, G)
plt.subplot(2, 2, 2)
plt.imshow(1 - G_rec, cmap='Greys')
plt.title('G (reconstructed)')

G_imposed = imimposemin(B, G)
plt.subplot(2, 2, 3)
if show_grad_as_binary:
    plt.imshow(np.invert(G_imposed.astype(bool)), cmap='Greys')
else:
    plt.imshow(np.invert(G_imposed), cmap='Greys')
plt.title('G (min imposed)')

if marker_method == 0:
    G_imposed_min = imregionalmin(G_imposed, G_min_filter_size)
    plt.subplot(2, 2, 4)
    plt.imshow(np.invert(G_imposed_min.astype(np.uint8)), cmap='Greys')
    plt.title('G (min imposed regional min)')
    ret, markers = cv2.connectedComponents(G_imposed_min.astype(np.uint8))
elif marker_method == 1:
    plt.subplot(2, 2, 4)
    plt.imshow(np.invert(B.astype(np.bool)), cmap='Greys')
    plt.title('Refined blobs')
    ret, markers = cv2.connectedComponents(B.astype(np.uint8))
elif marker_method == 2:
    markers = watershed.getRegionalMinima(G)
else:
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(J_otsu.astype(np.uint8), cv2.MORPH_OPEN, kernel, iterations=2)
    fig.append(plt.figure(fig_id))
    fig_id += 1
    plt.subplot(2, 2, 1)
    plt.imshow(opening, cmap='Greys')
    plt.title('Opening B')

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    plt.subplot(2, 2, 2)
    plt.imshow(sure_bg, cmap='Greys')
    plt.title('sure background area : dilated opening')

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    plt.subplot(2, 2, 3)
    plt.imshow(sure_fg, cmap='Greys')
    plt.title('sure foreground area')

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    plt.subplot(2, 2, 4)
    plt.imshow(unknown, cmap='Greys')
    plt.title('unknown area')
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

print 'min(markers)', np.min(markers)
print 'max(markers)', np.max(markers)
print 'markers.dtype: ', markers.dtype

fig.append(plt.figure(fig_id))
fig_id += 1
plt.subplot(2, 2, 1)
plt.imshow(markers)
plt.title('markers')

# plt.subplot(2, 2, 3)
# plt.imshow(G_imposed_rgb)
# plt.title('G_imposed_rgb')

# G_ret, G_markers = cv2.connectedComponents(imregionalmin(G, 3).astype(np.uint8))
G2 = G_imposed
# G2 = G
G2_markers = watershed.getRegionalMinima(G2, G_min_filter_size)
if watershed_method <= 2:
    np.savetxt('G2_markers.txt', G2_markers, fmt='%d', delimiter='\t')
    np.savetxt('G.txt', G, fmt='%15.6f', delimiter='\t')
    plt.subplot(2, 2, 1)
    plt.imshow(G2_markers)
    plt.title('G2_markers')

print 'min(G_markers)', np.min(G2_markers)
print 'max(G_markers)', np.max(G2_markers)
if watershed_method == 0:
    L = watershed.iterative_check_min(G2, G2_markers, G_min_filter_size)
elif watershed_method == 1:
    L = watershed.iterative_check_all(G2, G2_markers)
elif watershed_method == 2:
    L = watershed.recursive(G2, G2_markers)
elif watershed_method == 3:
    L = skimage.morphology.watershed(G_imposed, markers)
else:
    G_imposed_rgb = cv2.cvtColor(G_imposed, cv2.COLOR_GRAY2BGR).astype(np.uint8)
    L = cv2.watershed(G_imposed_rgb, markers)
print 'min(L)', np.min(L)
print 'max(L)', np.max(L)

# plt.subplot(2, 2, 4)
# plt.imshow(G_imposed_rgb)
# plt.title('G_imposed_rgb (watershed)')

# I_rgb[L == -1] = (255, 0, 0)
# plt.subplot(2, 1, 1)
# plt.imshow(I_rgb)
# plt.title('I_rgb (watershed)')

plt.subplot(2, 2, 2)
plt.imshow(L)
plt.title('L (watershed)')

L_copy = np.copy(L).astype(np.int32)
img, contours, hierarchy = cv2.findContours(L_copy, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_NONE)
img_contours = cv2.drawContours(np.copy(J), contours, -1, (255, 255, 255), 1)
# fig.append(plt.figure(fig_id))
# fig_id += 1
# plt.imshow(img_contours)
# plt.title('img_contours')
# plt.figure(fig_id-2)
L_pruned = np.zeros(L.shape, dtype=np.int32)
contour_id = 0
pruned_contours = []
hierarchy = hierarchy[0]
print 'n_contours: ', len(contours)
print 'n_hierarchy: ', len(hierarchy)
# print hierarchy
n_pruned_contours = 0
for contour in contours:
    hrch = hierarchy[contour_id - 1]
    area = cv2.contourArea(contour)

    # print 'contour.dtype:', contour.dtype
    # print 'contour.shape:', contour.shape
    # print 'hrch.shape:', hrch.shape
    # print 'contour_id:', contour_id
    # cnt_x = contour[0, 0, 0]
    # cnt_y = contour[0, 0, 1]
    # print 'contour val:', L[cnt_y, cnt_x]
    # print 'area:', area

    if (exclude_interior_contours and hrch[3] >= 0) or (area > max_area or area < min_area):
        pass
    else:
        n_pruned_contours += 1
        L_pruned = cv2.drawContours(L_pruned, [contour], -1, (n_pruned_contours, n_pruned_contours, n_pruned_contours), -1)
        pruned_contours.append(contour)
    contour_id += 1
print 'n_pruned_contours: ', len(pruned_contours)

plt.subplot(2, 2, 3)
plt.imshow(L_pruned)
plt.title('L (pruned)')

# plt.subplot(2, 2, 3)
# plt.imshow(L_pruned, cmap='Greys')
# plt.title('L (pruned) GS')

I = cv2.drawContours(I, pruned_contours, -1, contour_col,  1)
plt.subplot(2, 2, 4)
plt.imshow(I)
plt.title('Pruned Contours')

# fig.append(plt.figure(fig_id))
# fig_id += 1
# plt.imshow(I)
# plt.title('I (drawContours)')

if marker_method == 0:
    seg_title = 'Segmentation with regional minima as markers using min filter size {:d}'.format(G_min_filter_size)
    if use_skimage_min:
        seg_title = '{:s} (skimage regional min)'.format(seg_title)
    else:
        seg_title = '{:s} (scipy regional min)'.format(seg_title)
elif marker_method == 1:
    seg_title = 'Segmentation with refined blobs as markers using filter size {:d}'.format(min_filter_size)
elif marker_method == 2:
    seg_title = 'Segmentation with simple regional minima as markers'.format(min_filter_size)
else:
    seg_title = 'Segmentation with OpenCV tutorial based markers'
if watershed_method == 0:
    seg_title = '{:s} (iterative watershed)'.format(seg_title)
elif watershed_method == 2:
    seg_title = '{:s} (recursive watershed)'.format(seg_title)
elif watershed_method == 3:
    seg_title = '{:s} (skimage watershed)'.format(seg_title)
elif watershed_method == 4:
    seg_title = '{:s} (cv2 watershed)'.format(seg_title)
fig[-1].suptitle(seg_title)




plt.show()