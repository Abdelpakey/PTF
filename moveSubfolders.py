import glob
from Misc import processArguments
import sys, os, shutil

params = {
    'src_dir': '.',
    'dst_dir': '',
}

processArguments(sys.argv[1:], params)
src_dir = params['src_dir']
dst_dir = params['dst_dir']

if not dst_dir:
    dst_dir = src_dir

subfolders = [f for f in glob.iglob(src_dir + '/**/', recursive=True) if os.path.isdir(f) and
              not 'annotations' in f and f != 'bin']

for src in subfolders:
    print('moving {}'.format(src))
    try:
        shutil.move(src, dst_dir)
    except shutil.Error:
        print('Failure')
        continue
    except FileNotFoundError:
        print('Failure')
        continue
