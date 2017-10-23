import os
import cv2
import sys
# import numpy as np
from Misc import processArguments

params = {
    'db_root_dir': 'C:/Datasets',
    'actor': 'GRAM',
    'seq_name': 'ISL16F8J_TMC_SCU2DJ_2016-10-05_0700',
    'vid_fmt': 'mp4',
    'show_img': 0,
    'n_frames': 100
}

if __name__ == '__main__':
    processArguments(sys.argv[1:], params)

    db_root_dir = params['db_root_dir']
    actor = params['actor']
    seq_name = params['seq_name']
    show_img = params['show_img']
    vid_fmt = params['vid_fmt']
    n_frames = params['n_frames']

    print 'actor: ', actor
    print 'seq_name: ', seq_name

    src_fname = db_root_dir + '/' + actor + '/Images/' + seq_name + '.' + vid_fmt

    dst_dir = db_root_dir + '/' + actor + '/Images/' + seq_name

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    print 'Reading video from: {:s}'.format(src_fname)
    cap = cv2.VideoCapture()
    if not cap.open(src_fname):
        raise StandardError('The video file ' + src_fname + ' could not be opened')

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Frame {:d} could not be read'.format(frame_id + 1))
            break
        curr_img = cv2.imwrite(dst_dir + '/image{:06d}.jpg'.format(frame_id + 1), frame)
        if show_img:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == 27:
                break
        frame_id += 1
        if n_frames > 0 and frame_id >= n_frames:
            break
        if frame_id % 100 == 0:
            print 'Done {:d} frames'.format(frame_id)

