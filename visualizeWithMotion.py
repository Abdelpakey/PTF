import os
import cv2
import sys
import numpy as np
from Misc import processArguments

params = {
    'src_path': './sample.jpg',
    'width': 1920,
    'height': 1080,
    'min_height_ratio': 0.40,
    'speed': 1.0,
    'show_img': 0,
    'quality': 3,
    'resize': 0,
    'mode': 0,
}

if __name__ == '__main__':
    processArguments(sys.argv[1:], params)
    src_path = params['src_path']
    width = params['width']
    height = params['height']
    min_height_ratio = params['min_height_ratio']
    speed = params['speed']
    show_img = params['show_img']
    quality = params['quality']
    resize = params['resize']
    mode = params['mode']

    monitors = [
        [0, 0],
        [-1920, 0],
        [0, -1080],
        [1920, 0],
    ]

    aspect_ratio = float(width) / float(height)
    _pause = 0
    direction = -1

    img_id = 0
    if os.path.isdir(src_path):
        src_dir = src_path
        img_fname = None
    elif os.path.isfile(src_path):
        src_dir = os.path.dirname(src_path)
        img_fname = os.path.basename(src_path)
    else:
        raise IOError('Invalid source path: {}'.format(src_path))

    print('Reading source images from: {}'.format(src_dir))

    img_exts = ('.jpg', '.bmp', '.jpeg', '.png', '.tif', '.tiff', '.gif')
    src_file_list = [k for k in os.listdir(src_dir) if os.path.splitext(k.lower())[1] in img_exts]
    total_frames = len(src_file_list)
    if total_frames <= 0:
        raise SystemError('No input frames found')
    print('total_frames: {}'.format(total_frames))
    src_file_list.sort()

    if img_fname is None:
        img_fname = src_file_list[img_id]
    else:
        img_id = src_file_list.index(img_fname)

    src_img_ar, start_row, end_row, start_col, end_col, dst_height, dst_width = [None] * 7
    target_height, target_width, min_height, start_col, end_col = [None] * 5


    def loadImage():
        global src_img_ar, start_row, end_row, start_col, end_col, dst_height, dst_width
        global target_height, target_width, min_height, start_col, end_col

        img_fname = src_file_list[img_id]

        src_img_fname = os.path.join(src_dir, img_fname)
        src_img = cv2.imread(src_img_fname)

        if src_img is None:
            raise SystemError('Source image could not be read from: {}'.format(src_img_fname))

        src_height, src_width, n_channels = src_img.shape
        src_aspect_ratio = float(src_width) / float(src_height)

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

        # src_img = np.zeros((height, width, n_channels), dtype=np.uint8)
        src_img_ar = np.zeros((dst_height, dst_width, n_channels), dtype=np.uint8)
        src_img_ar[start_row:start_row + src_height, start_col:start_col + src_width, :] = src_img

        target_width = dst_width
        target_height = dst_height

        start_row = start_col = 0
        end_row = dst_height
        end_col = dst_width

        min_height = dst_height * min_height_ratio


    def mouseHandler(event, x, y, flags=None, param=None):
        global img_id, _pause, start_row
        if event == cv2.EVENT_LBUTTONDOWN:
            img_id -= 1
            if img_id < 0:
                img_id = total_frames - 1
            loadImage()
        elif event == cv2.EVENT_LBUTTONUP:
            pass
        elif event == cv2.EVENT_RBUTTONDOWN:
            img_id += 1
            if img_id >= total_frames:
                img_id = 0
            loadImage()
        elif event == cv2.EVENT_RBUTTONUP:
            pass
        elif event == cv2.EVENT_MBUTTONDOWN:
            start_row = y
        elif event == cv2.EVENT_MOUSEMOVE:
            pass


    win_name = 'VWM'
    cv2.namedWindow(win_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(win_name, mouseHandler)

    loadImage()

    while True:
        temp = src_img_ar[int(start_row):int(end_row), int(start_col):int(end_col), :]

        # temp_height, temp_width, _ = temp.shape
        # temp_aspect_ratio = float(temp_width) / float(temp_height)
        # print('temp_height: ', temp_height)
        # print('temp_width: ', temp_width)
        # print('temp_aspect_ratio: ', temp_aspect_ratio)

        dst_img = cv2.resize(temp, (width, height))

        cv2.imshow(win_name, dst_img)
        k = cv2.waitKey(1 - _pause)

        if k == 27:
            break
        elif k == ord('1'):
            cv2.moveWindow(win_name, monitors[0][0], monitors[0][1])
        elif k == ord('2'):
            cv2.moveWindow(win_name, monitors[1][0], monitors[1][1])
        elif k == ord('3'):
            cv2.moveWindow(win_name, monitors[2][0], monitors[2][1])
        elif k == ord('4'):
            cv2.moveWindow(win_name, monitors[3][0], monitors[3][1])
        elif k == 32:
            _pause = 1 - _pause
        elif k == ord('+'):
            speed += 0.01
            print('speed: ', speed)
        elif k == ord('-'):
            speed -= 0.01
            if speed <= 0:
                speed = 0.01
            print('speed: ', speed)
        elif k == ord('i'):
            direction = -direction
        elif k == 39 or k == ord('d'):
            img_id += 1
            if img_id >= total_frames:
                img_id = 0
            loadImage()
        elif k == 40 or k == ord('a'):
            img_id -= 1
            if img_id < 0:
                img_id = total_frames - 1
            loadImage()

        target_height = target_height + direction * speed

        if target_height < min_height:
            target_height = min_height
            direction = 1

        if target_height > dst_height:
            target_height = dst_height
            direction = -1

        target_width = target_height * aspect_ratio

        # print('speed: ', speed)
        # print('min_height: ', min_height)
        # print('target_height: ', target_height)
        # print('target_width: ', target_width)

        end_row = start_row + target_height

        col_diff = (dst_width - target_width) / 2.0
        start_col = col_diff
        end_col = dst_width - col_diff

        # print('end_row: ', end_row)
        # print('start_col: ', start_col)
        # print('end_col: ', end_col)

        # print('\n')

    cv2.destroyWindow(win_name)
