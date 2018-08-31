import os, sys
from datetime import datetime

from Misc import processArguments

if __name__ == '__main__':
    params = {
        'dir_names': [],
        'out_name': '',
        'postfix': '',
        'switches': '-r',
    }
    processArguments(sys.argv[1:], params)
    dir_names = params['dir_names']
    out_name = params['out_name']
    postfix = params['postfix']
    switches = params['switches']

    print('dir_names: ', dir_names)

    if len(dir_names) == 1:
        dir_names = dir_names[0].split('/')

    print('dir_names: ', dir_names)

    zip_path = ''
    for _dir in dir_names:
        zip_path = os.path.join(zip_path, _dir) if zip_path else _dir

    print('zip_path: ', zip_path)

    if not out_name:
        for _dir in dir_names:
            out_name = '{}_{}'.format(out_name, _dir) if out_name else _dir
    else:
        out_name = os.path.splitext(out_name)[0]
        
    if postfix:
        out_name = '{}_{}'.format(out_name, postfix)

    out_name.replace('.', '_')
    time_stamp = datetime.now().strftime("%y%m%d%H%M%S")
    out_name = '{}_{}.zip'.format(out_name, time_stamp)

    print('out_name: ', out_name)

    zip_cmd = 'zip {:s} {:s}'.format(switches, out_name)
    zip_cmd = '{:s} {:s}'.format(zip_cmd, zip_path)

    print('\nrunning: {}\n'.format(zip_cmd))
    # subprocess.call(zip_cmd)
    os.system(zip_cmd)

    mv_cmd = 'mv {:s} ~'.format(out_name)
    print('\nrunning: {}\n'.format(mv_cmd))
    # subprocess.call(zip_cmd)
    os.system(mv_cmd)