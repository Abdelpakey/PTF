import os
import sys

file_ext = ''
out_file = 'list.txt'
folder_name = '.'

arg_id = 1
if len(sys.argv) > arg_id:
    file_ext = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    out_file = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    folder_name = sys.argv[arg_id]
    arg_id += 1

print('Looking for files with extension {:s} in sub folders of {:s}'.format(file_ext, folder_name))

subfolders = [name for name in os.listdir(folder_name) if os.path.isdir(os.path.join(folder_name, name))]
total_files = 0
files = []
out_fid = open(out_file, 'w')
for subfolder in subfolders:
    subfolders_path = os.path.join(folder_name, subfolder)
    src_files = [f for f in os.listdir(subfolders_path) if os.path.isfile(os.path.join(subfolders_path, f))]
    if file_ext:
        src_files = [f for f in src_files if f.endswith(file_ext)]
    n_files = len(src_files)
    total_files += n_files
    print('{}:\t{}\t{}'.format(subfolder, n_files, total_files))
    for f in src_files:
        out_fid.write(os.path.join(subfolders_path, f) + '\n')
out_fid.close()
print('total_files: {}'.format(total_files))





