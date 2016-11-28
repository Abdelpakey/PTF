import sys
import os
import random

seq_prefix = 'Seq'
seq_root_dir = '.'
seq_start_id = 1
shuffle_files = 1

arg_id = 1
if len(sys.argv) > arg_id:
    seq_prefix = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    seq_start_id = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    shuffle_files = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    seq_root_dir = sys.argv[arg_id]
    arg_id += 1

print 'seq_prefix: {:s}'.format(seq_prefix)
print 'seq_start_id: {:d}'.format(seq_start_id)
print 'shuffle_files: {:d}'.format(shuffle_files)

src_file_names = [f for f in os.listdir(seq_root_dir) if os.path.isfile(os.path.join(seq_root_dir, f))]
if shuffle_files:
    print 'Shuffling files...'
    random.shuffle(src_file_names)

seq_id = seq_start_id
file_count = 1
n_files = len(src_file_names)
for src_fname in src_file_names:
    filename, file_extension = os.path.splitext(src_fname)
    src_path = os.path.join(seq_root_dir, src_fname)
    dst_path = os.path.join(seq_root_dir, '{:s}_{:d}{:s}'.format(seq_prefix, seq_id, file_extension))
    while os.path.exists(dst_path):
        seq_id += 1
        dst_path = os.path.join(seq_root_dir, '{:s}_{:d}{:s}'.format(seq_prefix, seq_id, file_extension))
    os.rename(src_path, dst_path)
    seq_id += 1
    if file_count % 10 == 0 or file_count == n_files:
        print 'Done {:d}/{:d}'.format(file_count, n_files)
    file_count += 1
