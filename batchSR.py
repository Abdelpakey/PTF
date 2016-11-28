import os
import zipfile
import sys
import subprocess
from Misc import getParamDict

if __name__ == '__main__':

    use_arch = 1
    arch_root_dir = './C++/MTF/log/archives'
    arch_name = 'resh_grid_rkl_eslm10rLMS25p10Ki5t_ssd_scv_rscv_zncc_ncc_ssim_spss_riu_50r_30i_4u_subseq10'
    in_arch_path = 'tracking_data'
    gt_root_dir = '../Datasets'
    tracking_root_dir = './C++/MTF/log/tracking_data'
    out_dir = './C++/MTF/log/success_rates'
    # list_fname = 'list.txt'
    list_fname = None
    list_in_arch = 0
    # list_fname = '{:s}/{:s}.txt'.format(arch_root_dir, arch_name)
    actor_ids = [0, 1, 2, 3]
    # actor_ids = [3]
    opt_gt_ssms = None
    opt_gt_ssms = ['0']

    write_to_bin = 1

    enable_subseq = 1
    n_subseq = 10

    reinit_from_gt = 1
    reinit_frame_skip = 5
    err_type = 0

    jaccard_err_thresh = 0.90

    if err_type == 2:
        # Jaccard error
        reinit_err_thresh = jaccard_err_thresh
        err_max = jaccard_err_thresh
        overflow_err = 1e3
    else:
        # MCD/CL error
        reinit_err_thresh = 20.0
        err_max = 20.0
        overflow_err = 1e3

    use_reinit_gt = 0
    err_min = 0
    err_res = 100
    write_err = 0
    overriding_seq_id = -1

    arg_id = 1
    if len(sys.argv) > arg_id:
        arch_name = sys.argv[arg_id]
        arg_id += 1
    if len(sys.argv) > arg_id:
        reinit_from_gt = int(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        reinit_frame_skip = int(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        reinit_err_thresh = float(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        arch_root_dir = sys.argv[arg_id]
        arg_id += 1
    if len(sys.argv) > arg_id:
        gt_root_dir = sys.argv[arg_id]
        arg_id += 1
    if len(sys.argv) > arg_id:
        tracking_root_dir = sys.argv[arg_id]
        arg_id += 1
    if len(sys.argv) > arg_id:
        out_dir = sys.argv[arg_id]
        arg_id += 1

    params_dict = getParamDict()
    actors = params_dict['actors']
    sequences = params_dict['sequences']

    # reinit gt only used with reinit tests
    # use_reinit_gt = use_reinit_gt or reinit_from_gt

    # sub sequence tests only run without reinitialization
    enable_subseq = enable_subseq and not reinit_from_gt

    arch_path = '{:s}/{:s}.zip'.format(arch_root_dir, arch_name)
    print 'Reading tracking data from zip archive: {:s}'.format(arch_path)
    arch_fid = zipfile.ZipFile(arch_path, 'r')

    # if not os.path.isfile(list_fname):
    # print 'List file for the batch job does  not exist:\n {:s}'.format(list_fname)

    file_list = None
    if list_fname is not None:
        if list_in_arch:
            file_list = arch_fid.open(list_fname, 'r').readlines()
        else:
            file_list = open('{:s}/{:s}'.format(arch_root_dir, list_fname), 'r').readlines()

            # exclude files corresponding to sub sequence runs if any
        file_list = [file_name for file_name in file_list
                     if '_init_' not in file_name and '.txt' in file_name]
        # file_list = [file_name for file_name in file_list if '.txt' in file_name]
        n_files = len(file_list)
        if opt_gt_ssms is not None and len(opt_gt_ssms) > 1 and len(opt_gt_ssms) != n_files:
            raise SyntaxError('Incorrect number of optimal GT specifiers given: {:d}'.format(len(opt_gt_ssms)))
        print 'Generating success rates for following {:d} files for all actors: \n'.format(n_files), file_list

    for actor_id in actor_ids:
        if list_fname is None or file_list is None:
            actor = actors[actor_id]
            if overriding_seq_id >= 0:
                seq_name = sequences[actor][overriding_seq_id]
            else:
                seq_name = sequences[actor][0]
            if reinit_from_gt:
                if reinit_err_thresh == int(reinit_err_thresh):
                    proc_file_path = '{:s}/reinit_{:d}_{:d}/{:s}/{:s}'.format(
                        in_arch_path, int(reinit_err_thresh), reinit_frame_skip, actor, seq_name)
                else:
                    proc_file_path = '{:s}/reinit_{:4.2f}_{:d}/{:s}/{:s}'.format(
                        in_arch_path, reinit_err_thresh, reinit_frame_skip, actor, seq_name)
            else:
                proc_file_path = '{:s}/{:s}/{:s}'.format(in_arch_path, actor, seq_name)

            path_list = [f for f in arch_fid.namelist() if f.startswith(proc_file_path)]
            file_list = [os.path.basename(path) for path in path_list]
            file_list = [file_name for file_name in file_list
                         if '_init_' not in file_name and '.txt' in file_name]
            n_files = len(file_list)
            if opt_gt_ssms is not None and len(opt_gt_ssms) > 1 and len(opt_gt_ssms) != n_files:
                raise SyntaxError('Incorrect number of optimal GT specifiers given: {:d}'.format(len(opt_gt_ssms)))
            print 'Generating success rates for following {:d} files for actor {:d}: \n'.format(n_files,
                                                                                                actor_id), file_list
        line_id = 0
        for line in file_list:
            line = line.rstrip()
            # line = line.rstrip('.txt')
            line = os.path.splitext(line)[0]
            print 'processing line: ', line
            words = line.split('_')
            mtf_sm = words[0]
            mtf_am = words[1]
            mtf_ssm = words[2]
            iiw = words[3]
            if opt_gt_ssms is None:
                opt_gt_ssm = mtf_ssm
                if opt_gt_ssm == '8' or opt_gt_ssm == 'c8' or opt_gt_ssm == 'l8' or opt_gt_ssm == 'sl3':
                    opt_gt_ssm = '0'
            elif len(opt_gt_ssms) > 1:
                opt_gt_ssm = opt_gt_ssms[line_id]
            else:
                opt_gt_ssm = opt_gt_ssms[0]

            arguments = '{:d} {:s} {:s} {:s} {:s}'.format(
                actor_id, mtf_sm, mtf_am, mtf_ssm, iiw)
            arguments = '{:s} {:s} {:s} {:s} {:s} {:s} {:s}'.format(
                arguments, arch_name, in_arch_path, arch_root_dir, gt_root_dir,
                tracking_root_dir, out_dir)
            arguments = '{:s} {:s} {:d} {:d} {:d} {:f} {:d} {:d} {:d}'.format(
                arguments, opt_gt_ssm, use_reinit_gt, reinit_from_gt, reinit_frame_skip,
                reinit_err_thresh, enable_subseq, n_subseq, overriding_seq_id)
            arguments = '{:s} {:f} {:f} {:d} {:d} {:d} {:f} {:d}'.format(
                arguments, err_min, err_max, err_res, err_type, write_err,
                overflow_err, write_to_bin)
            full_command = 'python successGeneralFast.py {:s}'.format(arguments)

            # full_command = \
            # 'python successGeneralFast.py {:d} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:d} {:d} {:d} {:f} {:d} {:d} {:f} {:f} {:d} {:d} {:d} {:f}'.format(
            # actor_id, mtf_sm, mtf_am, mtf_ssm, iiw, arch_name, in_arch_path, arch_root_dir, gt_root_dir,
            # tracking_root_dir, out_dir, opt_gt_ssm, use_reinit_gt, reinit_from_gt, reinit_frame_skip,
            # reinit_err_thresh, enable_subseq, n_subseq, err_min, err_max, err_res, err_type, write_err,
            # overflow_err)

            print 'running: {:s}'.format(full_command)
            subprocess.check_call(full_command, shell=True)
            # status = os.system(full_command)
            # if not status:
            # s = raw_input('Last command not completed successfully. Continue ?\n')
            # if s == 'n' or s == 'N':
            # sys.exit()
            line_id += 1