import os
import cv2
import numpy as np
import sys
from Misc import processArguments, getTrackingObject2

params = {
    'db_root_dir': 'N:\Datasets',
    'actor': 'ISL',
    'seq_name': 'DJI_0020',
    'vid_fmt': 'mov',
    'show_img': 1,
    'n_frames': 1000,
    'n_regions': 1,
    'remove_regions': 1,
    'vis_resize_factor': 1,
    'save_fmt': ('avi', 'XVID', 30)
}

if __name__ == '__main__':
    processArguments(sys.argv[1:], params)

    db_root_dir = params['db_root_dir']
    actor = params['actor']
    seq_name = params['seq_name']
    show_img = params['show_img']
    vid_fmt = params['vid_fmt']
    n_frames = params['n_frames']
    n_regions = params['n_regions']
    remove_regions = params['remove_regions']
    save_fmt = params['save_fmt']

    print 'actor: ', actor
    print 'seq_name: ', seq_name

    src_fname = db_root_dir + '/' + actor + '/' + seq_name + '.' + vid_fmt
    dst_fname = db_root_dir + '/' + actor + '/' + seq_name + '_masked.' + vid_fmt

    print('Reading video file: {:s}'.format(src_fname))
    cap = cv2.VideoCapture()
    if not cap.open(src_fname):
        raise StandardError('The video file ' + src_fname + ' could not be opened')

    ret, frame = cap.read()
    if not ret:
        raise StandardError('First frame could not be read')

    regions = []
    n_rows, n_cols, _ = frame.shape
    if remove_regions:
        frame_mask = np.zeros((n_rows, n_cols, 3), dtype=np.uint8)
        fill_col = (255, 255, 255)
        op_type = 'remove'
        line_col = (0, 0, 255)
    else:
        frame_mask = np.ones((n_rows, n_cols, 3), dtype=np.uint8)
        fill_col = (0, 0, 0)
        op_type = 'retain'
        line_col = (0, 255, 0)

    for i in range(n_regions):
        region = getTrackingObject2(frame, line_thickness=2, col=line_col,
                                    title='Select region {:d} to {:s}'.format(i + 1, op_type))
        corners = np.array(region, dtype=np.int32)
        cv2.fillConvexPoly(frame_mask, corners, fill_col)
        regions.append(region)

    # frame_mask = cv2.cvtColor(frame_mask, cv2.COLOR_GRAY2RGB)

    if show_img:
        cv2.imshow('Remove mask', frame_mask)
        cv2.waitKey(0)

    frame_mask = frame_mask.astype(np.bool)

    frame_size = (int(n_cols), int(n_rows))

    video_writer = cv2.VideoWriter()
    if cv2.__version__.startswith('3'):
        video_writer.open(filename=dst_fname, apiPreference=cv2.CAP_FFMPEG,
                          fourcc=cv2.VideoWriter_fourcc(*save_fmt[1]),
                          fps=int(save_fmt[2]), frameSize=frame_size)
    else:
        video_writer.open(filename=dst_fname, fourcc=cv2.cv.CV_FOURCC(*save_fmt[1]),
                          fps=save_fmt[2], frameSize=frame_size)

    if not video_writer.isOpened():
        print('Video file {:s} could not be opened'.format(dst_fname))
        exit(0)

    print('Writing video file: {:s}'.format(dst_fname))
    frame_id = 0
    while True:
        frame[frame_mask] = 0
        if show_img:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == 27:
                break
        video_writer.write(frame)
        frame_id += 1
        if n_frames > 0 and frame_id >= n_frames:
            break
        ret, frame = cap.read()
        if not ret:
            print('Frame {:d} could not be read'.format(frame_id + 1))
            break

        sys.stdout.write('\rDone {:d}/{:d} frames'.format(
            frame_id + 1, n_frames))
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()

    video_writer.release()
