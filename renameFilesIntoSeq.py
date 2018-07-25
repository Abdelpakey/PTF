import sys
import os
import random
from Misc import sortKey

seq_prefix = 'Seq'
seq_root_dir = '.'
seq_start_id = 1
shuffle_files = 1
filename_fmt = 0
write_log = 1

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
    filename_fmt = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    _seq_root_dir = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    write_log = int(sys.argv[arg_id])
    arg_id += 1

if len(sys.argv) < 3:
    # extract start_id from name
    split_str = seq_prefix.split('_')
    seq_start_id = int(split_str[-1]) + 1
    seq_prefix = split_str[0]
    for _str in split_str[1:-1]:
        seq_prefix = '{}_{}'.format(seq_prefix, _str)

print 'seq_prefix: {:s}'.format(seq_prefix)
print 'seq_start_id: {:d}'.format(seq_start_id)
print 'shuffle_files: {:d}'.format(shuffle_files)
print 'file_fmt: {:d}'.format(filename_fmt)

_seq_root_dir = os.path.abspath(_seq_root_dir)

if os.path.isdir(_seq_root_dir):
    seq_root_dirs = [_seq_root_dir]
elif os.path.isfile(_seq_root_dir):
    seq_root_dirs = [x.strip() for x in open(_seq_root_dir).readlines() if x.strip()]
else:
    raise IOError('Invalid seq_root_dir: {}'.format(_seq_root_dir))

if write_log:
    log_dir = 'rseq_log'
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    print('Saving log to {}'.format(log_dir))

for seq_root_dir in seq_root_dirs:
    print 'Processing: {}'.format(seq_root_dir)
    src_file_names = [f for f in os.listdir(seq_root_dir) if os.path.isfile(os.path.join(seq_root_dir, f))]
    if shuffle_files:
        print 'Shuffling files...'
        random.shuffle(src_file_names)
    else:
        src_file_names.sort(key=sortKey)

    seq_id = seq_start_id
    file_count = 1
    n_files = len(src_file_names)

    if write_log:
        log_file = os.path.join(log_dir, '{}.txt'.format(os.path.basename(seq_root_dir)))
        log_fid = open(log_file, 'w')

    for src_fname in src_file_names:
        filename, file_extension = os.path.splitext(src_fname)
        src_path = os.path.join(seq_root_dir, src_fname)
        if filename_fmt == 0:
            dst_fname = '{:s}_{:d}{:s}'.format(seq_prefix, seq_id, file_extension)
        else:
            dst_fname = '{:s}{:06d}{:s}'.format(seq_prefix, seq_id, file_extension)
        dst_path = os.path.join(seq_root_dir, dst_fname)

        if src_path != dst_path:
            while os.path.exists(dst_path):
                seq_id += 1
                if filename_fmt == 0:
                    dst_fname = '{:s}_{:d}{:s}'.format(seq_prefix, seq_id, file_extension)
                else:
                    dst_fname = '{:s}{:06d}{:s}'.format(seq_prefix, seq_id, file_extension)
                dst_path = os.path.join(seq_root_dir, dst_fname)
            os.rename(src_path, dst_path)
        if write_log:
            log_fid.write('{}\t{}\n'.format(src_fname, dst_fname))
        seq_id += 1
        if file_count % 10 == 0 or file_count == n_files:
            print 'Done {:d}/{:d}'.format(file_count, n_files)
        file_count += 1
    if write_log:
        log_fid.close()
