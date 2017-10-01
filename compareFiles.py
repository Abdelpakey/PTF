import subprocess
import filecmp
import os
dir_1 = '/root/mdp_log'
dir_2 = '/root/mdp_tf_log'
filenames = [
    ['indices.txt', 'templates/indices.txt'],
    ['overlaps.txt', 'templates/overlaps.txt'],
    ['ratios.txt', 'templates/ratios.txt'],
    ['angles.txt', 'templates/angles.txt'],
    ['bb_overlaps.txt', 'templates/bb_overlaps.txt'],
    ['similarity.txt', 'templates/similarity.txt'],
    ['scores.txt', 'templates/scores.txt'],
    ['roi.txt', 'templates/roi.txt'],
    ['patterns.txt', 'templates/patterns.txt'],

]
for files in filenames:
    path_1  = '{:s}/{:s}'.format(dir_1, files[0])
    path_2 = '{:s}/{:s}'.format(dir_2, files[1])

    if not os.path.isfile(path_1):
        print '{:s} does not exist'.format(path_1)
        continue
    if not os.path.isfile(path_2):
        print '{:s} does not exist'.format(path_2)
        continue
    subprocess.call('dos2unix {:s}'.format(path_1), shell=True)
    subprocess.call('dos2unix {:s}'.format(path_2), shell=True)
    if not filecmp.cmp(path_1, path_2):
        print '\nFiles {:s} and {:s} are different\n'.format(path_1, path_2)
