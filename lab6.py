import numpy as np
import scipy.ndimage
import cv2
import math
import matplotlib.pyplot as plt

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

# print cv2.__version__

sig = 2.5
min_scale = 3
max_scale = 5
use_builtin_log = 1
adaptive_gauss_sigma = 1
min_filter_size = 15
scatter_size = 40
scatter_col = 'r'


I_rgb = cv2.imread('Red11-93/Substack (11-93) red0005.bmp').astype(np.float32)
I = cv2.cvtColor(I_rgb, cv2.COLOR_BGR2GRAY)

J = cv2.GaussianBlur(I, (int(2 * round(3 * sig) + 1), int(2 * round(3 * sig) + 1)), sig,
                     borderType=cv2.BORDER_REPLICATE)
fig1 = plt.figure(1)
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

fig2 = plt.figure(2)
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
fig2.suptitle('LoG Pyramid')

# plt.figure(3)
# plt.imshow(K, extent=[0, 1, 0, 1])
# plt.title('K (LoG)')

# local maxima within the volume
lm = scipy.ndimage.filters.minimum_filter(K, min_filter_size)
A = (K == lm)
# take minima within a range of scales and collapse those on x-y plane
B = np.sum(A, axis=2)

print 'min A: ', np.min(A)
print 'max A: ', np.max(A)
print 'min B: ', np.min(B)
print 'max B: ', np.max(B)

fig3 = plt.figure(3)
# plt.subplot(2, 2, 1)
# level1 = A[:, :, 0]
# # print 'min level1: ', np.min(level1)
# # print 'max level1 ', np.max(level1)
# plt.imshow(level1, cmap='Greys')
# plt.title('Level 1')
# plt.subplot(2, 2, 2)
# level2 = A[:, :, 1]
# # print 'min level1: ', np.min(level2)
# # print 'max level1 ', np.max(level2)
# plt.imshow(level2, cmap='Greys')
# plt.title('Level 2')
# plt.subplot(2, 2, 3)
# level3 = A[:, :, 2]
# # print 'min level1: ', np.min(level3)
# # print 'max level1 ', np.max(level3)
# plt.imshow(level3, cmap='Greys')
# plt.title('Level 3')
# plt.subplot(2, 2, 4)
plt.imshow(1-B, cmap='Greys')
# plt.title('Sum')
fig3.suptitle('Regional minima in the LoG Pyramid')

[y, x] = B.nonzero()
fig4 = plt.figure(4)
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
t, B_otsu = cv2.threshold(J.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print 't: ', t
B = np.multiply(B, J >= t)

# cv2.imshow('B_otsu', B_otsu)
# cv2.imshow('B np.multiply', B.astype(np.float32))

[y, x] = B.nonzero()
fig5 = plt.figure(5)
plt.imshow(I)
# plt.hold(True)
plt.scatter(x, y, marker='.', color=scatter_col, s=scatter_size)
plt.xlim([0, I.shape[1]])
plt.ylim([0, I.shape[0]])
# plt.plot(x, y, marker='.', color='r')
# plt.hold(False)
plt.grid(b=False)
plt.title('Refined blobs detected in the image')

# fig6 = plt.figure(6)
# plt.hist(J.ravel(), 256, [0,256])

plt.show()