import os, sys, glob, re

from Misc import processArguments, sortKey

if __name__ == '__main__':
    params = {
        'dir_names': [],
        'out_name': '',
    }
    processArguments(sys.argv[1:], params)
    dir_names = params['dir_names']
    out_name = params['out_name']

    zip_path = os.path.join(dir_names)

    print('dir_names: ', dir_names)
    print('zip_path: ', zip_path)

    if not out_name:

        for _dir in dir_names[1:]:
            out_name = '{}_{}'.format(out_name, _dir) if out_name else _dir

    print('out_name: ', out_name)

    zip_cmd = 'zip -r {:s}'.format(out_name)
    zip_cmd = '{:s} {:s}'.format(zip_cmd, zip_path)

    print('\nrunning: {}\n'.format(zip_cmd))
    # subprocess.call(zip_cmd)
    os.system(zip_cmd)









