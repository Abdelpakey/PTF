import os
import sys

if __name__ == '__main__':
    filename = 'folder_list.txt'

    if not os.path.isfile(filename):
        print 'File containing the folder list not found'
        sys.exit()

    folder_root_dir = 'folders_from_list'
    if not os.path.exists(folder_root_dir):
        os.mkdir(folder_root_dir)

    data_file = open(filename, 'r')
    lines = data_file.readlines()
    data_file.close()

    for folder_name in lines:
        folder_name = folder_name.strip()
        if len(folder_name) <= 1:
            print 'Skipping: ', folder_name
            continue
        folder_path = '{:s}/{:s}'.format(folder_root_dir, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

