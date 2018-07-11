import os, sys, glob, re
import subprocess

from Misc import processArguments, sortKey

if __name__ == '__main__':
    params = {
        'list_file': '',
        'file_name': '',
        'root_dir': '',
        'out_name': '',
    }
    processArguments(sys.argv[1:], params)
    list_file = params['list_file']
    root_dir = params['root_dir']
    file_name = params['file_name']
    out_name = params['out_name']

    if list_file:
        if os.path.isdir(list_file):
            zip_paths = [os.path.join(list_file, name) for name in os.listdir(list_file) if
                         os.path.isdir(os.path.join(list_file, name))]
            zip_paths.sort(key=sortKey)
        else:
            zip_paths = [x.strip() for x in open(list_file).readlines() if x.strip()]
            if root_dir:
                zip_paths = [os.path.join(root_dir, name) for name in zip_paths]
    else:
        zip_paths = [file_name]

    zip_cmd = 'zip -r {:s}'.format(out_name)
    for zip_path in zip_paths:
        zip_cmd = '{:s} {:s}'.format(zip_cmd, zip_path)


    print('\nrunning: {}\n'.format(zip_cmd))
    # subprocess.call(zip_cmd)
    os.system(zip_cmd)




