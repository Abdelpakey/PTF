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

src_dir = os.path.abspath(src_dir)
dst_dir = os.path.abspath(dst_dir)

subfolders = [os.path.abspath(f) for f in glob.iglob(src_dir + '/**/', recursive=True) if os.path.isdir(f) and
              not 'annotations' in f and f != 'bin']

for src in subfolders:
    if src_dir == src or dst_dir == src:
        continue

    print('moving {}'.format(src))
    try:
        shutil.move(src, dst_dir)
    except shutil.Error:
        print('Failure')
        continue
    except FileNotFoundError:
        print('Failure')
        continue
    except OSError:
        print('Failure')
        continue
