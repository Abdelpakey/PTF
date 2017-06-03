import subprocess
import sys
import os

curr_path = os.path.dirname(os.path.realpath(__file__))
print 'curr_path: ', curr_path

src_dir = '.'
list_fname = 'list.txt'

arg_id = 1
if len(sys.argv) > arg_id:
    list_fname = sys.argv[arg_id]
    arg_id += 1
if len(sys.argv) > arg_id:
    src_dir = sys.argv[arg_id]
    arg_id += 1

list_path = src_dir + '/' + list_fname
lines = [line.rstrip('\n') for line in open(list_path)]

for line in lines:
    src, dst = line.split()
    command = 'python {:s}/rename.py {:s} {:s}'.format(curr_path, src, dst)
    subprocess.check_call(command, shell=True)
