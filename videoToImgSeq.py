import os
import cv2
import sys


# import numpy as np
# from Misc import processArguments

def processArguments(args, params):
    # arguments specified as 'arg_name=argv_val'
    no_of_args = len(args)
    for arg_id in range(no_of_args):
        arg = args[arg_id].split('=')
        if len(arg) != 2 or not arg[0] in params.keys():
            print('Invalid argument provided: {:s}'.format(args[arg_id]))
            return
        if not arg[1] or not arg[0]:
            continue
        try:
            params[arg[0]] = type(params[arg[0]])(arg[1])
        except ValueError:
            print('Invalid argument value {} provided for {}'.format(arg[1], arg[0]))
            return


params = {
    'db_root_dir': 'N:\Datasets',
    'actor': 'ISL',
    'seq_name': 'DJI_0002',
    'vid_fmt': 'mov',
    'dst_dir': '',
    'show_img': 0,
    'n_frames': 0,
    'roi': None,
    'resize_factor': 1.0,
    'start_id': 0
}

if __name__ == '__main__':
    processArguments(sys.argv[1:], params)

    db_root_dir = params['db_root_dir']
    actor = params['actor']
    seq_name = params['seq_name']
    show_img = params['show_img']
    vid_fmt = params['vid_fmt']
    n_frames = params['n_frames']
    roi = params['roi']
    resize_factor = params['resize_factor']
    dst_dir = params['dst_dir']
    start_id = params['start_id']

    roi_enabled = False

    if roi is not None and isinstance(roi, (list, tuple)) and len(roi) == 4:
        xmin, ymin, xmax, ymax = roi
        if xmax > xmin and ymax > ymin:
            print('Using roi: ', roi)
            roi_enabled = True

    print('actor: ', actor)
    print('seq_name: ', seq_name)
    print('start_id: ', start_id)

    src_fname = os.path.join(db_root_dir, actor, seq_name + '.' + vid_fmt)
    print('Reading video file: {:s}'.format(src_fname))

    if not dst_dir:
        dst_dir = os.path.join(db_root_dir, actor, seq_name)
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    print('Writing image sequence to: {:s}'.format(dst_dir))

    cap = cv2.VideoCapture()
    if not cap.open(src_fname):
        raise StandardError('The video file ' + src_fname + ' could not be opened')

    if cv2.__version__.startswith('3'):
        cv_prop = cv2.CAP_PROP_FRAME_COUNT
    else:
        cv_prop = cv2.cv.CAP_PROP_FRAME_COUNT
    total_frames = int(cap.get(cv_prop))

    if n_frames <= 0:
        n_frames = total_frames
    elif total_frames > 0 and n_frames > total_frames:
        raise AssertionError('Invalid n_frames {} for video with {} frames'.format(n_frames, total_frames))

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('\nFrame {:d} could not be read'.format(frame_id + 1))
            break
        frame_id += 1
        if frame_id <= start_id:
            continue
        if roi_enabled:
            frame = frame[roi[1]:roi[3], roi[0]:roi[2], :]
        if resize_factor != 1:
            frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

        curr_img = cv2.imwrite(dst_dir + '/image{:06d}.jpg'.format(frame_id - start_id), frame)
        if show_img:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == 27:
                break
        if n_frames > 0 and (frame_id-start_id) >= n_frames:
            break
        sys.stdout.write('\rDone {:d}/{:d} frames'.format(
            (frame_id - start_id), n_frames))
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()
