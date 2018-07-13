import cv2
import sys
import os, shutil

from Misc import processArguments, sortKey, resizeAR

params = {
    'src_path': '.',
    'save_path': '',
    'img_ext': 'jpg',
    'show_img': 1,
    'del_src': 0,
    'start_id': 0,
    'n_frames': 0,
    'width': 0,
    'height': 0,
    'fps': 30,
    'codec': 'H264',
    'ext': 'mkv',
}

processArguments(sys.argv[1:], params)
src_path = params['src_path']
save_path = params['save_path']
img_ext = params['img_ext']
show_img = params['show_img']
del_src = params['del_src']
start_id = params['start_id']
n_frames = params['n_frames']
width = params['width']
height = params['height']
fps = params['fps']
codec = params['codec']
ext = params['ext']

print('Reading source images from: {}'.format(src_path))

img_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.tif']

src_path = os.path.abspath(src_path)
cap = cv2.VideoCapture()
if not cap.open(src_path):
    raise StandardError('The video file ' + src_path + ' could not be opened')

if cv2.__version__.startswith('3'):
    cv_prop = cv2.CAP_PROP_FRAME_COUNT
    h_prop = cv2.CAP_PROP_FRAME_HEIGHT
    w_prop = cv2.CAP_PROP_FRAME_WIDTH
else:
    cv_prop = cv2.cv.CAP_PROP_FRAME_COUNT
    h_prop = cv2.cv.CAP_PROP_FRAME_HEIGHT
    w_prop = cv2.cv.CAP_PROP_FRAME_WIDTH

total_frames = int(cap.get(cv_prop))
_height = int(cap.get(h_prop))
_width = int(cap.get(w_prop))

if n_frames <= 0:
    n_frames = total_frames
elif total_frames > 0 and n_frames > total_frames:
    raise AssertionError('Invalid n_frames {} for video with {} frames'.format(n_frames, total_frames))

if not save_path:
    save_path = os.path.join(os.path.dirname(src_path), os.path.splitext(os.path.basename(src_path))[0] + '.' + ext)

save_dir = os.path.dirname(save_path)
if save_dir and not os.path.isdir(save_dir):
    os.makedirs(save_dir)

if height <= 0 or width <= 0:
    height, width = _height, _width

fourcc = cv2.VideoWriter_fourcc(*codec)
video_out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

if video_out is None:
    raise IOError('Output video file could not be opened: {}'.format(save_path))

print('Saving {}x{} output video to {}'.format(width, height, save_path))

frame_id = start_id
pause_after_frame = 0
while True:

    ret, image = cap.read()
    if not ret:
        print('\nFrame {:d} could not be read'.format(frame_id + 1))
        break

    image = resizeAR(image, width, height)

    if show_img:
        cv2.imshow('frame', image)
        k = cv2.waitKey(1 - pause_after_frame) & 0xFF
        if k == ord('q') or k == 27:
            break
        elif k == 32:
            pause_after_frame = 1 - pause_after_frame

    video_out.write(image)

    frame_id += 1
    sys.stdout.write('\rDone {:d} frames '.format(frame_id - start_id))
    sys.stdout.flush()

    if n_frames > 0 and (frame_id - start_id) >= n_frames:
        break

    if frame_id >= total_frames:
        break

sys.stdout.write('\n')
sys.stdout.flush()

video_out.release()

if show_img:
    cv2.destroyAllWindows()
if del_src:
    print('Removing source folder {}'.format(src_path))
    shutil.rmtree(src_path)