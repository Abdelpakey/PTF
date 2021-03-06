import fnmatch
import os
import sys

src_dir = '.'
src_substr = '4u'
dst_substr = ''
recursive_search = 1
include_folders = 0
replace_existing = 0
show_names = 1
add_as_prefix = 0
add_as_suffix = 0
remove_files = 0

arg_id = 1
if len(sys.argv) > arg_id:
    src_substr = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    dst_substr = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    recursive_search = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    include_folders = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    replace_existing = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    show_names = int(sys.argv[arg_id])
    arg_id += 1
if len(sys.argv) > arg_id:
    src_dir = sys.argv[arg_id]
    arg_id += 1

src_dir = os.path.abspath(src_dir)
dst_substr_orig = dst_substr

if src_substr == '__prefix__' or src_substr == '__pf__':
    src_substr = ''
    add_as_prefix = 1
elif src_substr == '__suffix__' or src_substr == '__sf__':
    src_substr = ''
    add_as_suffix = 1
elif src_substr == '__space__' or src_substr == '__sp__':
    src_substr = ' '
if dst_substr == '__remove__' or dst_substr == '__rm__':
    remove_files = 1
if dst_substr == '__space__' or dst_substr == '__sp__':
    dst_substr = ' '
if dst_substr == '__none__' or dst_substr == '__n__':
    dst_substr = ''
if dst_substr_orig == '__root__' or dst_substr_orig == '__rf__':
    dst_substr = 'root folder name'

if add_as_prefix:
    print 'Adding {:s} as prefix'.format(dst_substr)
elif add_as_suffix:
    print 'Adding {:s} as suffix'.format(dst_substr)
elif remove_files:
    print 'Searching for {:s} to remove in {:s}'.format(src_substr, src_dir)
else:
    print 'Searching for {:s} to replace with {:s} in {:s}'.format(src_substr, dst_substr, src_dir)
if recursive_search:
    print 'Searching for files recursively in all sub folders'
else:
    print 'Searching for files only in the top level folder'

if include_folders == 1:
    print 'Searching for folders too'
elif include_folders == 2:
    print 'Searching only for folders'
else:
    print 'Not searching for folders'

src_file_paths = []
for root, dirnames, filenames in os.walk(src_dir):
    if include_folders:
        for dirname in fnmatch.filter(dirnames, '*{:s}*'.format(src_substr)):
            src_file_paths.append(os.path.join(root, dirname))
    if include_folders != 2:
        for filename in fnmatch.filter(filenames, '*{:s}*'.format(src_substr)):
            src_file_paths.append(os.path.join(root, filename))
    if not recursive_search:
        break
print 'Found {:d} matches'.format(len(src_file_paths))
for src_path in src_file_paths:
    if remove_files:
        if show_names:
            print 'removing {:s}'.format(src_path)
        os.remove(src_path)
        continue

    if dst_substr_orig == '__root__' or dst_substr_orig == '__rf__':
        dst_substr = os.path.basename(os.path.dirname(src_path)) + '_'

    if add_as_prefix:
        dst_path = os.path.join(os.path.dirname(src_path), '{:s}{:s}'.format(dst_substr, os.path.basename(src_path)))
    elif add_as_suffix:
        dst_path = os.path.join(os.path.dirname(src_path), '{:s}{:s}'.format(os.path.basename(src_path), dst_substr))
    else:
        dst_path = src_path.replace(src_substr, dst_substr)

    src_fname_dir = os.path.dirname(src_path)
    dst_fname_dir = os.path.dirname(dst_path)
    #
    # if src_fname_dir != dst_fname_dir:
    # if show_names:
    # print 'renaming folder {:s} to {:s}'.format(src_fname_dir, dst_fname_dir)
    #         os.rename(src_fname_dir, dst_fname_dir)
    #     dst_fname = src_fname.replace(src_substr, dst_substr)

    if show_names:
        print 'renaming {:s} to {:s}'.format(src_path, dst_path)
    if os.path.exists(dst_path):
        if replace_existing:
            print 'Destination file: {:s} already exists. Removing it...'.format(dst_path)
            os.remove(dst_path)
        else:
            print 'Destination file: {:s} already exists. Skipping it...'.format(dst_path)
            continue
    os.rename(src_path, dst_path)
    # print matches
