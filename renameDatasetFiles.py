import sys
import os
from Misc import getParamDict

params_dict = getParamDict()
actors = params_dict['actors']
sequences = params_dict['sequences']
seq_prefix = 'frame'
seq_start_id = 1

db_root_dir = '../Datasets'
actor_id = 13
seq_id = 9

arg_id = 1
if len(sys.argv) > arg_id:
    actor_id = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    seq_id = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    db_root_dir = sys.argv[arg_id]
    arg_id += 1

print 'seq_prefix: {:s}'.format(seq_prefix)
print 'seq_start_id: {:d}'.format(seq_start_id)

actor = actors[actor_id]
seq_name = sequences[actor][seq_id]
# seq_name = 'hexagon_task_fast_right_2'
seq_root_dir = db_root_dir + '/' + actor + '/' + seq_name
src_file_names = [f for f in os.listdir(seq_root_dir) if os.path.isfile(os.path.join(seq_root_dir, f))]

frame_id = seq_start_id
file_count = 1
n_files = len(src_file_names)
for src_fname in src_file_names:
    filename, file_extension = os.path.splitext(src_fname)
    src_path = os.path.join(seq_root_dir, src_fname)
    dst_path = os.path.join(seq_root_dir, '{:s}{:05d}{:s}'.format(seq_prefix, frame_id, file_extension))
    while os.path.exists(dst_path):
        frame_id += 1
        dst_path = os.path.join(seq_root_dir, '{:s}_{:d}{:s}'.format(seq_prefix, frame_id, file_extension))
    os.rename(src_path, dst_path)
    frame_id += 1
    if file_count % 10 == 0 or file_count == n_files:
        print 'Done {:d}/{:d}'.format(file_count, n_files)
    file_count += 1
