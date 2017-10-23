import sys
import os

filter_string = 'magnet'
# 0: only at start
# 1: anywhere
filter_type = 0
in_fname = 'm.txt'
out_fname = 'filtered.txt'
arg_id = 1
if len(sys.argv) > arg_id:
    filter_string = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    filter_type = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    in_fname = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    out_fname = sys.argv[arg_id]
    arg_id += 1

if not os.path.isfile(in_fname):
    print 'Input file {:s} does not exist'.format(in_fname)
    exit(0)

if filter_type == 0:
    print 'Filtering lines starting with {:s} in {:s} to {:s}'.format(filter_string, in_fname, out_fname)
else:
    print 'Filtering lines containing {:s} in {:s} to {:s}'.format(filter_string, in_fname, out_fname)

out_fid = open(out_fname, 'w')
lines = open(in_fname, 'r').readlines()
n_filtered_lines = 0
for line in lines:
    retain_line = False
    if filter_type == 0:
        retain_line = line.startswith(filter_string)
    elif filter_type == 1:
        retain_line = filter_string in line
    if retain_line:
        out_fid.write(line)
        n_filtered_lines += 1
print 'Done filtering {:d} lines'.format(n_filtered_lines)
out_fid.close()
