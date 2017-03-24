import numpy as np

def getSmallestNeighborIndex(img, row, col):
    min_row_id = -1
    min_col_id = -1
    min_val = np.inf
    h, w = img.shape
    for row_id in xrange(row - 1, row + 2):
        if row_id < 0 or row_id >= h:
            continue
        for col_id in xrange(col - 1, col + 2):
            if col_id < 0 or col_id >= w:
                continue
            if row_id == row and col_id == col:
                continue
            if img[row_id, col_id] < min_val:
                min_row_id = row_id
                min_col_id = col_id
                min_val = img[row_id, col_id]
    return min_row_id, min_col_id


def getRegionalMinima(img):
    regional_minima = np.zeros(img.shape, dtype=np.int32)
    h, w = img.shape
    minimum_id = 1
    for row in xrange(h):
        for col in xrange(w):
            min_row, min_col = getSmallestNeighborIndex(img, row, col)
            if min_row < 0 or min_col < 0:
                raise LookupError('getRegionalMinima :: Smallest neighbor for ({:d}, {:d}) not found'.format(row, col))
            if img[row, col] <= img[min_row, min_col]:
                regional_minima[row, col] = minimum_id
                minimum_id += 1
    return regional_minima


def iterativeMinFollowing(img, markers):
    markers_copy = np.copy(markers).astype(np.int32)
    h, w = img.shape
    while True:
        n_unmarked_pix = 0
        for row in xrange(h):
            for col in xrange(w):
                if markers_copy[row, col] > 0:
                    continue
                [min_row, min_col] = getSmallestNeighborIndex(img, row, col)
                if min_row < 0 or min_col < 0:
                    raise LookupError(
                        'iterativeMinFollowing :: Smallest neighbor for ({:d}, {:d}) not found'.format(row, col))
                if markers_copy[min_row, min_col] > 0:
                    markers_copy[row, col] = markers_copy[min_row, min_col]
                if markers_copy[row, col] == 0:
                    n_unmarked_pix += 1
        print 'n_unmarked_pix: ', n_unmarked_pix
        if n_unmarked_pix == 0:
            break
    return markers_copy