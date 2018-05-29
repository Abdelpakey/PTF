import os
import cv2
import sys
import numpy as np
from Misc import processArguments

params = {
    'src_path': '/home/abhineet/N/Datasets/617',
    'img_fname': 'sample.jpg',
    'width': 1920,
    'height': 1080,
    'min_height_ratio': 0.5,
    'speed': 1.0,
    'show_img': 0,
    'quality': 3,
    'resize': 0,
    'mode': 0,
}

if __name__ == '__main__':
    processArguments(sys.argv[1:], params)
    src_path = params['src_path']
    img_fname = params['img_fname']
    width = params['width']
    height = params['height']
    min_height_ratio = params['min_height_ratio']
    speed = params['speed']
    show_img = params['show_img']
    quality = params['quality']
    resize = params['resize']
    mode = params['mode']

    print('Reading source images from: {}'.format(src_path))

    # img_exts = ('.jpg', '.bmp', '.jpeg', '.png', '.tif', '.tiff', '.gif')
    # src_file_list = [k for k in os.listdir(src_path) if os.path.splitext(k.lower())[1] in img_exts]

    # total_frames = len(src_file_list)
    # if total_frames <= 0:
    #     raise SystemError('No input frames found')
    # print('total_frames: {}'.format(total_frames))
    # src_file_list.sort()

    # total_frames = len(src_file_list)
    # print('total_frames after sorting: {}'.format(total_frames))
    # sys.exit()

    aspect_ratio = float(width) / float(height)
    min_height = int(height * min_height_ratio)

    _pause = 0

    img_id = 0

    if resize:
        print('Resizing images to {}x{}'.format(width, height))

    src_img_fname = os.path.join(src_path, img_fname)
    src_img = cv2.imread(src_img_fname)
    img_fname_no_ext = os.path.splitext(img_fname)[0]

    if src_img is None:
        raise SystemError('Source image could not be read from: {}'.format(src_img_fname))

    src_height, src_width, n_channels = src_img.shape
    src_aspect_ratio = float(src_width) / float(src_height)

    start_row = start_col = 0

    if mode == 0:
        if src_aspect_ratio == aspect_ratio:
            dst_width = src_width
            dst_height = src_height
            start_row = start_col = 0
        elif src_aspect_ratio > aspect_ratio:
            dst_width = src_width
            dst_height = int(src_width / aspect_ratio)
            start_row = int((dst_height - src_height) / 2.0)
            start_col = 0
        else:
            dst_height = src_height
            dst_width = int(src_height * aspect_ratio)
            start_col = int((dst_width - src_width) / 2.0)
            start_row = 0
    else:
        if src_aspect_ratio == aspect_ratio:
            dst_width = width
            dst_height = height
        elif src_aspect_ratio > aspect_ratio:
            # too tall
            dst_height = int(height)
            dst_width = int(height * src_aspect_ratio)
        else:
            # too wide
            dst_width = int(width)
            dst_height = int(width / aspect_ratio)

    end_row = dst_height
    end_col = dst_width

    # src_img = np.zeros((height, width, n_channels), dtype=np.uint8)
    src_img_ar = np.zeros((dst_height, dst_width, n_channels), dtype=np.uint8)
    src_img_ar[start_row:start_row + src_height, start_col:start_col + src_width, :] = src_img

    target_width = dst_width
    target_height = dst_height

    cv2.namedWindow(img_fname)

    direction = -1

    while True:
        temp = src_img_ar[start_row:end_row + src_height, start_col:end_col, :]
        dst_img = cv2.resize(temp, (width, height))

        cv2.imshow(img_fname, dst_img)
        k = cv2.waitKey(1 - _pause)
        if k == 27:
            break
        elif k == 32:
            _pause = 1 - _pause

        target_height = target_height + direction*speed
        target_width = int(target_height*aspect_ratio)

        end_row = target_height

        col_diff = int((dst_width - target_width)/2.0)
        start_col += col_diff
        end_col -= col_diff

    cv2.destroyWindow(img_fname)
