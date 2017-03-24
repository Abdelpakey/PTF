import numpy as np
import cv2
import matplotlib.pyplot as plt


def smallest_neighbor_idx(img, row, col, visited):
    _min_row = []
    _min_col = []
    min_val = np.inf
    h, w = img.shape
    win_range = 1
    for i in xrange(row - win_range, row + win_range + 1):
        if i < 0 or i >= h:
            continue
        for j in xrange(col - win_range, col + win_range + 1):
            if j < 0 or j >= w:
                continue
            if i == row and j == col:
                continue
            if visited[i, j]:
                continue
            if img[i, j] < min_val:
                _min_row = [i]
                _min_col = [j]
                min_val = img[i, j]
            elif img[i, j] == min_val:
                _min_row.append(i)
                _min_col.append(j)


    # print 'smallest_neighbor_idx :: row, col: ', row, col
    # print 'smallest_neighbor_idx :: min_row, min_col: ', _min_row, _min_col
    return [_min_row, _min_col]

def getRegionalMinima(img):
    regional_minima = np.zeros(img.shape, dtype=np.int32)
    visited = np.zeros(img.shape)
    h, w = img.shape
    minimum_id = 1
    for row in xrange(h):
        for col in xrange(w):
            # visited[row, col] = 1
            min_row, min_col = smallest_neighbor_idx(img, row, col, visited)
            if not min_row or not min_col:
                raise LookupError('get_regional_minima :: Nearest neighbor for ({:d}, {:d}) not found'.format(row, col))
            for i, j in zip(min_row, min_col):
                if img[row, col] <= img[i, j]:
                    regional_minima[row, col] = minimum_id
                    minimum_id += 1
                    break
            # print 'row, col: ', row, col
            # print 'min_row, min_col: ', min_row, min_col

    return regional_minima

def iterativeMinFollowing(img, markers):
    # np.savetxt('markers.txt', markers, fmt='%d', delimiter='\t')
    # plt.imshow(markers)
    # plt.show()
    # markers_plot = plt.imshow(markers)
    visited = np.zeros(img.shape)
    markers = markers.astype(np.int32)

    h, w = img.shape
    while True:
        n_unmarked_pix = 0
        for row in xrange(h):
            for col in xrange(w):
                # print 'iterative_check_min :: markers:\n', markers
                if markers[row, col] > 0:
                    continue
                # visited[row, col] = 1
                [min_row, min_col] = smallest_neighbor_idx(img, row, col, visited)
                if not min_row or not min_col:
                    raise LookupError('Nearest neighbor for ({:d}, {:d}) not found'.format(row, col))
                for i, j in zip(min_row, min_col):
                    if markers[i, j] > 0:
                        markers[row, col] = markers[i, j]
                        break
                if markers[row, col] == 0:
                    # print 'row, col: ', row, col
                    # print 'min_row, min_col: ', min_row, min_col
                    n_unmarked_pix += 1
        # disp_markers = np.copy(markers)
        # disp_markers[disp_markers == 0] = 65535
        # cv2.imshow('markers', disp_markers)
        # if cv2.waitKey(1) == 27:
        #     break
        # markers_plot.set_data(markers)
        # plt.draw()
        # plt.imshow(markers)
        # plt.show()
        if n_unmarked_pix == 0:
            break
        print 'n_unmarked_pix: ', n_unmarked_pix

    [ys, xs] = np.nonzero(markers == 0)
    if ys and xs:
        gap = 3
        unmarked_id = 0
        np.set_printoptions(suppress=True, precision=5)
        for y, x in zip(ys, xs):
            start_y = max(0, y - gap)
            end_y = min(h - 1, y + gap)
            start_x = max(0, x - gap)
            end_x = min(w - 1, x + gap)
            print 'unmarked_id: {:d} ({:d}, {:d})'.format(unmarked_id, y, x)
            print 'markers:\n', markers[start_y:end_y+1, start_x:end_x+1]
            print 'img:\n', img[start_y:end_y+1, start_x:end_x+1]
            unmarked_id += 1
        print 'markers.shape: ', markers.shape
        print 'markers.dtype: ', markers.dtype
        print 'img.shape: ', img.shape
    return markers


def iterative_check_all(img, markers):
    print 'Running iterative watershed with all neighbors being checked'

    print 'markers.shape: ', markers.shape
    print 'img.shape: ', img.shape

    # np.savetxt('markers.txt', markers, fmt='%d', delimiter='\t')
    # plt.imshow(markers)
    # plt.show()
    h, w = img.shape
    while True:
        n_unmarked_pix = 0
        for row in xrange(h):
            start_row = row - 1
            end_row = row + 1
            for col in xrange(w):
                print 'iterative_check_all :: markers:\n', markers
                if markers[row, col] > 0:
                    continue
                start_col = col - 1
                end_col = col + 1
                if start_row >= 0:
                    if start_col >= 0 and markers[start_row, start_col] > 0:
                        markers[row, col] = markers[start_row, start_col]
                        continue
                    if markers[start_row, col] > 0:
                        markers[row, col] = markers[start_row, col]
                        continue
                    if end_col < w and markers[start_row, end_col] > 0:
                        markers[row, col] = markers[start_row, end_col]
                        continue

                if end_row < h:
                    if start_col >= 0 and markers[end_row, start_col] > 0:
                        markers[row, col] = markers[end_row, start_col]
                        continue
                    if markers[end_row, col] > 0:
                        markers[row, col] = markers[end_row, col]
                        continue
                    if end_col < w and markers[end_row, end_col] > 0:
                        markers[row, col] = markers[end_row, end_col]
                        continue
                if start_col >= 0 and markers[row, start_col] > 0:
                    markers[row, col] = markers[row, start_col]
                    continue
                if end_col < w and markers[row, end_col] > 0:
                    markers[row, col] = markers[row, end_col]
                    continue
                n_unmarked_pix += 1
        if n_unmarked_pix == 0:
            break
        print 'n_unmarked_pix: ', n_unmarked_pix
    return markers

