import os
import cv2
import sys, time, random, glob
import numpy as np
# from multiprocessing import Pool, Process
from Misc import processArguments, sortKey
import psutil

win_utils_available = 1
try:
    import winUtils
except ImportError as e:
    win_utils_available = 0
    print('Failed to import winUtils: {}'.format(e))
try:
    from ctypes import windll, Structure, c_long, byref

    # Get active window id
    # https://msdn.microsoft.com/en-us/library/ms633505
    winID = windll.user32.GetForegroundWindow()
    print "This is your current window ID: ", winID


    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]


    def queryMousePosition():
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt


    mousePos = queryMousePosition()
    print "mouse position x: ", mousePos.x, " y:", mousePos.y
except ImportError as e:
    mousePos = None

params = {
    'src_path': '.',
    'width': 1920,
    'height': 1080,
    'min_height_ratio': 0.40,
    'speed': 0.5,
    'show_img': 0,
    'quality': 3,
    'resize': 0,
    'mode': 0,
    'auto_progress': 0,
    'max_switches': 1,
    'max_duration': 30,
    'random_mode': 0,
    'recursive': 1,
    'fullscreen': 1,
    'reversed_pos': 0,
    'double_click_interval': 0.1,
}

if __name__ == '__main__':
    p = psutil.Process(os.getpid())
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

    processArguments(sys.argv[1:], params)
    src_path = params['src_path']
    _width = width = params['width']
    _height = height = params['height']
    min_height_ratio = params['min_height_ratio']
    speed = params['speed']
    show_img = params['show_img']
    quality = params['quality']
    resize = params['resize']
    mode = params['mode']
    auto_progress = params['auto_progress']
    max_switches = params['max_switches']
    max_duration = params['max_duration']
    random_mode = params['random_mode']
    recursive = params['recursive']
    fullscreen = params['fullscreen']
    reversed_pos = params['reversed_pos']
    double_click_interval = params['double_click_interval']

    old_speed = speed
    speed = 0
    monitors = [
        [0, 0],
        [-1920, 0],
        [0, -1080],
        [1920, 0],
    ]
    if mousePos is None:
        curr_monitor = 0
    else:
        curr_monitor = 0
        min_dist = np.inf
        for curr_id, monitor in enumerate(monitors):
            centroid_x = (monitor[0] + monitor[0] + 1920) / 2.0
            centroid_y = (monitor[1] + monitor[1] + 1080) / 2.0
            dist = (mousePos.x - centroid_x) ** 2 + (mousePos.y - centroid_y) ** 2
            if dist < min_dist:
                min_dist = dist
                curr_monitor = curr_id
    print('curr_monitor: ', curr_monitor)

    aspect_ratio = float(width) / float(height)
    direction = -1
    n_switches = 0
    start_time = end_time = 0
    src_start_row = src_start_col = src_end_row = src_end_col = 0

    lc_start_t = rc_start_t = None
    end_exec = 0

    img_id = 0
    if os.path.isdir(src_path):
        src_dir = src_path
        img_fname = None
    elif os.path.isfile(src_path):
        src_dir = os.path.dirname(src_path)
        img_fname = src_path
    else:
        raise IOError('Invalid source path: {}'.format(src_path))

    print('Reading source images from: {}'.format(src_dir))

    img_exts = ('.jpg', '.bmp', '.jpeg', '.png', '.tif', '.tiff', '.gif')

    if recursive:
        src_file_gen = [[os.path.join(dirpath, f) for f in filenames if
                         os.path.splitext(f.lower())[1] in img_exts]
                        for (dirpath, dirnames, filenames) in os.walk(src_dir)]
        src_file_list = [item for sublist in src_file_gen for item in sublist]

        # _src_file_list = list(src_file_gen)
        # src_file_list = []
        # for x in _src_file_list:
        #     src_file_list += x
    else:
        src_file_list = [os.path.join(src_dir, k) for k in os.listdir(src_dir) if
                         os.path.splitext(k.lower())[1] in img_exts]

    # src_file_list = [list(x) for x in src_file_list]
    # src_file_list = [x for x in src_file_list]

    # print('src_file_list: ', src_file_list)

    # for (dirpath, dirnames, filenames) in os.walk(src_dir):
    #     print()
    #     print('dirpath', dirpath)
    #     print('filenames', filenames)
    #     print('dirnames', dirnames)
    #     print()

    total_frames = len(src_file_list)
    if total_frames <= 0:
        raise SystemError('No input frames found')
    print('total_frames: {}'.format(total_frames))

    if img_fname is None:
        img_fname = src_file_list[img_id]

    try:
        # nums = int(os.path.splitext(img_fname)[0].split('_')[-1])
        src_file_list.sort(key=sortKey)
    except:
        src_file_list.sort()

    img_id = src_file_list.index(img_fname)

    if random_mode:
        print('Random mode enabled')
        src_file_list_rand = list(np.random.permutation(src_file_list))

    src_img_ar, start_row, end_row, start_col, end_col, dst_height, dst_width = [None] * 7
    target_height, target_width, min_height, start_col, end_col, height_ratio = [None] * 6


    def createWindow():
        global mode

        cv2.destroyWindow(win_name)

        if mode == 0:
            if fullscreen:
                cv2.namedWindow(win_name, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, 1)
            else:
                cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
                if win_utils_available:
                    # winUtils.hideBorder(monitors[curr_monitor][0], monitors[curr_monitor][1],
                    #                     width, height, win_name)
                    winUtils.hideBorder2(win_name)
            cv2.moveWindow(win_name, monitors[curr_monitor][0], monitors[curr_monitor][1])
        else:
            cv2.namedWindow(win_name)
            if win_utils_available:
                winUtils.hideBorder2(win_name)
            #     winUtils.hideBorder(monitors[2][0], monitors[2][1], width, height, win_name)
            # else:
            cv2.moveWindow(win_name, monitors[2][0], monitors[2][1])

        cv2.setMouseCallback(win_name, mouseHandler)


    def changeMode():
        global mode, height, aspect_ratio
        mode = 1 - mode

        if mode == 0:
            height = int(height / 2.0)
        else:
            height = int(2 * height)

        # print('changeMode :: height: ', height)
        aspect_ratio = float(width) / float(height)
        createWindow()
        loadImage()


    def loadImage(_type=0):
        global src_img_ar, start_row, end_row, start_col, end_col, dst_height, dst_width, n_switches, img_id, direction
        global target_height, target_width, min_height, start_col, end_col, height_ratio, img_fname, start_time
        global src_start_row, src_start_col, src_end_row, src_end_col, aspect_ratio

        aspect_ratio = float(width) / float(height)

        if _type == 1:
            # if random_mode:
            #     img_id += random.randint(1, total_frames)
            # else:
            img_id += 1
        elif _type == -1:
            # if random_mode:
            #     img_id -= random.randint(1, total_frames)
            # else:
            img_id -= 1

        if img_id >= total_frames:
            img_id -= total_frames
        elif img_id < 0:
            img_id += total_frames

        if random_mode:
            img_fname = src_file_list_rand[img_id]
        else:
            img_fname = src_file_list[img_id]

        # src_img_fname = os.path.join(src_dir, img_fname)
        src_img_fname = img_fname
        src_img = cv2.imread(src_img_fname)

        if src_img is None:
            raise SystemError('Source image could not be read from: {}'.format(src_img_fname))

        src_height, src_width, n_channels = src_img.shape
        if mode == 1 and src_height < src_width:
            src_img = np.rot90(src_img)
            src_height, src_width, n_channels = src_img.shape

        src_aspect_ratio = float(src_width) / float(src_height)

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

        # if mode == 0:
        # else:
        #     if src_aspect_ratio == aspect_ratio:
        #         dst_width = width
        #         dst_height = height
        #     elif src_aspect_ratio > aspect_ratio:
        #         # too tall
        #         dst_height = int(height)
        #         dst_width = int(height * src_aspect_ratio)
        #     else:
        #         # too wide
        #         dst_width = int(width)
        #         dst_height = int(width / aspect_ratio)

        # src_img = np.zeros((height, width, n_channels), dtype=np.uint8)

        src_start_row = start_row
        src_start_col = start_col
        src_end_row = start_row + src_height
        src_end_col = start_col + src_width

        src_img_ar = np.zeros((dst_height, dst_width, n_channels), dtype=np.uint8)
        src_img_ar[int(src_start_row):int(src_end_row), int(src_start_col):int(src_end_col), :] = src_img

        target_width = dst_width
        target_height = dst_height

        start_row = start_col = 0
        end_row = dst_height
        end_col = dst_width

        min_height = dst_height * min_height_ratio

        height_ratio = float(dst_height) / float(height)

        n_switches = 0
        direction = -1
        start_time = time.time()

        # print('height: ', height)
        # print('dst_height: ', dst_height)
        # print('dst_width: ', dst_width)


    # def motionStep(_direction):
    #     global target_height, direction, end_row, start_col, end_col
    #
    #     target_height = target_height + _direction * speed
    #
    #     if target_height < min_height:
    #         target_height = min_height
    #         _direction = 1
    #
    #     if target_height > dst_height:
    #         target_height = dst_height
    #         _direction = -1
    #
    #     target_width = target_height * aspect_ratio
    #
    #     # print('speed: ', speed)
    #     # print('min_height: ', min_height)
    #     # print('target_height: ', target_height)
    #     # print('target_width: ', target_width)
    #
    #     end_row = start_row + target_height
    #
    #     col_diff = (dst_width - target_width) / 2.0
    #     start_col = col_diff
    #     end_col = dst_width - col_diff
    #
    #     return _direction

    def increaseSpeed():
        global speed
        speed += 0.01
        print('speed: ', speed)


    def decreaseSpeed():
        global speed
        speed -= 0.01
        if speed < 0:
            speed = 0
        print('speed: ', speed)


    def mouseHandler(event, x, y, flags=None, param=None):
        global img_id, start_row, lc_start_t, rc_start_t, end_exec, fullscreen
        try:
            if event == cv2.EVENT_MBUTTONDBLCLK:
                end_exec = 1
            elif event == cv2.EVENT_RBUTTONDBLCLK:
                pass
                # fullscreen = 1 - fullscreen
                # createWindow()
                # if fullscreen:
                #     print('fullscreen mode enabled')
                # else:
                #     print('fullscreen mode disabled')
                # loadImage(-1)
            elif event == cv2.EVENT_LBUTTONDOWN:
                # if lc_start_t is None:
                #     lc_start_t = time.time()
                # else:
                #     lc_end_t = time.time()
                #     click_interval = lc_end_t - lc_start_t
                #     print('click_interval: ', click_interval)
                #     if click_interval < double_click_interval:
                #         lc_start_t = None
                loadImage(-1)
            elif event == cv2.EVENT_LBUTTONUP:
                pass
            elif event == cv2.EVENT_RBUTTONDOWN:
                # if  rc_start_t is None:
                #     rc_start_t = time.time()
                # else:
                #     rc_end_t = time.time()
                #     click_interval = rc_end_t - rc_start_t
                #     if click_interval < double_click_interval:
                #         end_exec = 1
                #     rc_start_t = None
                loadImage(1)
            elif event == cv2.EVENT_RBUTTONUP:
                pass
            elif event == cv2.EVENT_MBUTTONDOWN:
                loadImage()
            elif event == cv2.EVENT_MOUSEMOVE:
                pass
            elif event == cv2.EVENT_MOUSEWHEEL:
                print('flags: ', flags)
                # _delta = cv2.getMouseWheelDelta(flags)
                if flags > 0:
                    increaseSpeed()
                    # motionStep(1)
                else:
                    decreaseSpeed()
                    # motionStep(-1)
        except AttributeError as e:
            pass

    win_name = 'VWM'
    createWindow()
    loadImage()

    while True:
        temp = src_img_ar[int(start_row):int(end_row), int(start_col):int(end_col), :]

        # temp_height, temp_width, _ = temp.shape
        # temp_aspect_ratio = float(temp_width) / float(temp_height)
        # print('temp_height: ', temp_height)
        # print('temp_width: ', temp_width)
        # print('temp_aspect_ratio: ', temp_aspect_ratio)

        dst_img = cv2.resize(temp, (width, height))

        if mode == 0 and not fullscreen:
            temp_height, temp_width, _ = temp.shape
            temp_height_ratio = float(temp_height) / float(height)

            win_start_row = int(max(0, src_start_row - start_row) / temp_height_ratio)
            win_end_row = height - int(max(0, end_row - src_end_row) / temp_height_ratio)

            win_start_col = int(max(0, src_start_col - start_col) / temp_height_ratio)
            win_end_col = width - int(max(0, end_col - src_end_col) / temp_height_ratio)

            dst_img = dst_img[win_start_row:win_end_row, win_start_col:win_end_col, :]

            # print(':: reversed_pos: ', reversed_pos)

            if reversed_pos:
                cv2.moveWindow(win_name, monitors[curr_monitor][0] + width - dst_img.shape[1], monitors[curr_monitor][1])

            # if win_utils_available:
            #     winUtils.hideBorder2(win_name)

        cv2.imshow(win_name, dst_img)

        # winUtils.hideBorder2(win_name)
        # winUtils.show2(win_name)
        # if win_utils_available:
        #     winUtils.show(win_name, dst_img, 0)
        # else:
        #     cv2.imshow(win_name, dst_img)

        k = cv2.waitKey(1)

        if k == 27 or end_exec:
            break
        elif k == 13 or k == ord('m'):
            changeMode()
        elif k == ord('r'):
            random_mode = 1 - random_mode
            if random_mode:
                print('Random mode enabled')
                src_file_list_rand = list(np.random.permutation(src_file_list))
            else:
                print('Random mode disabled')
        elif k == ord('c'):
            auto_progress = 1 - auto_progress
            if auto_progress:
                print('Auto progression enabled')
            else:
                print('Auto progression disabled')
        elif k == ord('m'):
            max_switches -= 1
            if max_switches < 1:
                max_switches = 1
        elif k == ord('n'):
            max_switches += 1
        elif k == ord('1'):
            curr_monitor = 0
            cv2.moveWindow(win_name, monitors[0][0], monitors[0][1])
            # createWindow()
        elif k == ord('2'):
            curr_monitor = 1
            cv2.moveWindow(win_name, monitors[1][0], monitors[1][1])
            # createWindow()
        elif k == ord('3'):
            curr_monitor = 2
            cv2.moveWindow(win_name, monitors[2][0], monitors[2][1])
            # createWindow()
        elif k == ord('4'):
            curr_monitor = 3
            cv2.moveWindow(win_name, monitors[3][0], monitors[3][1])
            # createWindow()
        elif k == ord('+'):
            increaseSpeed()
        elif k == 32:
            if speed == 0:
                speed = old_speed
            else:
                old_speed = speed
                speed = 0
        elif k == ord('p') or k == ord('R'):
            reversed_pos = 1 - reversed_pos
            # print('reversed_pos: ', reversed_pos)
            if not reversed_pos:
                cv2.moveWindow(win_name, monitors[curr_monitor][0], monitors[curr_monitor][1])
        elif k == ord(','):
            height -= 5
            if height < 10:
                height = 10
            loadImage()
        elif k == ord('.'):
            height += 5
            loadImage()
        elif k == ord('<'):
            width -= 5
            if width < 10:
                width = 10
            loadImage()
        elif k == ord('>'):
            width += 5
            loadImage()
        elif k == ord('/'):
            height = _height
            loadImage()
        elif k == ord('?'):
            width = _width
            loadImage()
        elif k == ord('-'):
            decreaseSpeed()
        elif k == ord('i'):
            direction = -direction
        elif k == ord('s') or k == ord('l') or k == ord('R'):
            loadImage()
        elif k == 39 or k == ord('d'):
            loadImage(1)
        elif k == 40 or k == ord('a'):
            loadImage(-1)
        elif k == ord('F'):
            print(img_fname)
        elif k == ord('f') or k == ord('/') or k == ord('?'):
            fullscreen = 1 - fullscreen
            createWindow()
            if fullscreen:
                print('fullscreen mode enabled')
            else:
                print('fullscreen mode disabled')

        # direction = motionStep(direction)

        _speed = speed if mode == 0 else 2 * speed
        target_height = target_height + direction * _speed * height_ratio

        if target_height < min_height:
            target_height = min_height
            direction = 1

        if target_height > dst_height:
            target_height = dst_height
            n_switches += 1
            if auto_progress and n_switches >= max_switches:
                loadImage(1)
            else:
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

        if speed == 0 and auto_progress:
            end_time = time.time()
            if end_time - start_time >= max_duration:
                loadImage(1)

        # print('end_row: ', end_row)
        # print('start_col: ', start_col)
        # print('end_col: ', end_col)

        # print('\n')

    cv2.destroyWindow(win_name)
