import sys
filter_string = 'magnet'
in_fname = 'm.txt'
out_fname = 'filtered.txt'
arg_id = 1
if len(sys.argv) > arg_id:
    filter_string = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    in_fname = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    out_fname = sys.argv[arg_id]
    arg_id += 1

print 'Filtering lines starting with {:s} in {:s} to {:s}'.format(filter_string, in_fname, out_fname)

out_fid = open(out_fname, 'w')
lines = open(in_fname, 'r').readlines()
n_filtered_lines = 0
for line in lines:
    if line.startswith(filter_string):
        out_fid.write(line)
        n_filtered_lines += 1
print 'Done filtering {:d} lines'.format(n_filtered_lines)
out_fid.close()


