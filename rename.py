import fnmatch
import os
import sys

src_dir = '.'
src_substr = '4u'
dst_substr = ''
replace_existing = 0

arg_id = 1
if len(sys.argv) > arg_id:
    src_substr = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    dst_substr = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    replace_existing = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    src_dir = sys.argv[arg_id]
    arg_id += 1

if dst_substr == '__space__':
    dst_substr = ' '


print 'Searching for {:s} to replace with {:s} in {:s}'.format(src_substr, dst_substr, src_dir)
src_fnames = []
for root, dirnames, filenames in os.walk(src_dir):
    for filename in fnmatch.filter(filenames, '*{:s}*'.format(src_substr)):
        src_fnames.append(os.path.join(root, filename))
print 'Found {:d} matches'.format(len(src_fnames))
for src_fname in src_fnames:
    dst_fname = src_fname.replace(src_substr, dst_substr)
    if os.path.exists(dst_fname):
        if replace_existing:
            print 'Destination file: {:s} already exists. Removing it...'.format(dst_fname)
            os.remove(dst_fname)
        else:
            print 'Destination file: {:s} already exists. Skipping it...'.format(dst_fname)
    os.rename(src_fname, dst_fname)
    # print matches