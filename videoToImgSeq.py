import os
import cv2
import sys
# import numpy as np
from Misc import processArguments

params = {
    'db_root_dir': 'N:\Datasets',
    'actor': 'ISL',
    'seq_name': 'DJI_0002',
    'vid_fmt': 'mov',
    'show_img': 0,
    'n_frames': 2000,
    'roi': [1821,231,2373,467]
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

    roi_enabled = False

    if roi is not None:
        xmin, ymin, xmax, ymax = roi
        if xmax > xmin and ymax > ymin:
            print('Using roi: ', roi)
            roi_enabled = True

    print 'actor: ', actor
    print 'seq_name: ', seq_name

    src_fname = db_root_dir + '/' + actor + '/' + seq_name + '.' + vid_fmt

    dst_dir = db_root_dir + '/' + actor + '/Images/' + seq_name

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    print 'Reading video file: {:s}'.format(src_fname)
    cap = cv2.VideoCapture()
    if not cap.open(src_fname):
        raise StandardError('The video file ' + src_fname + ' could not be opened')

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Frame {:d} could not be read'.format(frame_id + 1))
            break
        if roi_enabled:
            frame = frame[roi[1]:roi[3], roi[0]:roi[2], :]
        curr_img = cv2.imwrite(dst_dir + '/image{:06d}.jpg'.format(frame_id + 1), frame)
        if show_img:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == 27:
                break
        frame_id += 1
        if n_frames > 0 and frame_id >= n_frames:
            break
        sys.stdout.write('\rDone {:d}/{:d} frames'.format(
            frame_id + 1, n_frames))
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()


