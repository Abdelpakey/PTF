__author__ = 'Tommy'

tracker_configs = {}
out_dirs = {}

# compare GT DOFs
config_id = 0
out_dirs[config_id] = 'comparing_gt_dof'
tracker_configs[config_id] = [
    {'sm': 'opt_gt', 'am': 'ccre25r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'Homography', 'col': 'red'},
    {'sm': 'opt_gt', 'am': 'lscv50r30i4u', 'ssm': '6', 'iiw': 0, 'legend': 'Affine', 'col': 'green'},
    {'sm': 'opt_gt', 'am': 'rscv50r30i4u', 'ssm': '4', 'iiw': 0, 'legend': 'Similitude', 'col': 'orange'},
    {'sm': 'opt_gt', 'am': 'rscv50r30i4u', 'ssm': '3', 'iiw': 0, 'legend': 'Isometry', 'col': 'magenta'},
    {'sm': 'opt_gt', 'am': 'rscv50r30i4u', 'ssm': '3s', 'iiw': 0, 'legend': 'Transcaling', 'col': 'purple'},
    {'sm': 'opt_gt', 'am': 'scv50r30i4u', 'ssm': '2', 'iiw': 0, 'legend': 'Translation', 'col': 'cyan'}
]

# compare variants of LK
config_id = 1
out_dirs[config_id] = 'comparing_lk_rscv'
tracker_configs[config_id] = [
    {'sm': 'falk', 'am': 'rscv', 'ssm': '8', 'iiw': 1, 'legend': 'FALK/RSCV', 'col': 'red'},
    {'sm': 'ialk', 'am': 'rscv', 'ssm': '8', 'iiw': 1, 'legend': 'IALK/RSCV', 'col': 'green'},
    {'sm': 'fclk', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'FCLK/RSCV', 'col': 'orange'},
    {'sm': 'iclk', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK/RSCV', 'col': 'cyan'},
    {'sm': 'esm', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'ESM/RSCV', 'col': 'magenta'},
    {'sm': 'nnic', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC/RSCV', 'col': 'black'}
]
config_id = 2
out_dirs[config_id] = 'comparing_lk2'
tracker_configs[config_id] = [
    {'sm': 'falkC1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 1, 'legend': 'FALK', 'col': 'red'},
    {'sm': 'ialkC1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 1, 'legend': 'IALK', 'col': 'green'},
    {'sm': 'fclkC1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'FCLK', 'col': 'orange'},
    {'sm': 'iclkI1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK', 'col': 'cyan'},
    {'sm': 'esmDJSSH', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ESM', 'col': 'magenta'},
    {'sm': 'nnic1kI1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC', 'col': 'black'}
]
config_id = 3
out_dirs[config_id] = 'comparing_8dof_rt_with_lt'
tracker_configs[config_id] = [
    {'sm': 'gt', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'Registration (8DOF)', 'col': 'green'},
    {'sm': 'dsst', 'am': 'ssd50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'Learning (3DOF)', 'col': 'red',
     'use_arch': 1, 'arch_name': 'dsst_kcf_rct_tld_cmt', 'in_arch_path': 'log/tracking_data'},
    {'sm': 'iclkI1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK', 'col': 'cyan'},
    {'sm': 'esmDJSSH', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ESM', 'col': 'magenta'},
    {'sm': 'nnic1kI1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC', 'col': 'black'}
]

# compare ssd like AMs
config_id = 4
out_dirs[config_id] = 'comparing_lk'
tracker_configs[config_id] = [
    {'sm': 'rklIC5gIC', 'am': 'ccre25r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'SSD', 'col': 'red'},
    {'sm': 'rklIC5gIC', 'am': 'lscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'lscv', 'col': 'green'},
    {'sm': 'rklIC5gIC', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'rscv', 'col': 'orange'},
    {'sm': 'rklIC5gIC', 'am': 'scv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'scv', 'col': 'cyan'},
    {'sm': 'rklIC5gIC', 'am': 'ssd50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ssd', 'col': 'magenta'},
    {'sm': 'rklIC5gIC', 'am': 'zncc50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'zncc', 'col': 'yellow'}
]

# compare nnic with esm/fc/fa using ncc
config_id = 5
out_dirs[config_id] = 'comparing_nnic_ncc'
tracker_configs[config_id] = [
    {'sm': 'nnic', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC/NCC', 'col': 'red'},
    {'sm': 'nesm', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'ESM/NCC', 'col': 'green'},
    {'sm': 'fclk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'FCLK/NCC', 'col': 'orange'},
    {'sm': 'falk', 'am': 'ncc', 'ssm': '8', 'iiw': 1, 'legend': 'FALK/NCC', 'col': 'cyan'},
    {'sm': 'iclk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK/NCC', 'col': 'magenta'},
    {'sm': 'ialk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'IALK/NCC', 'col': 'black'}
]
config_id = 6
out_dirs[config_id] = 'comparing_nnic_rscv'
tracker_configs[config_id] = [
    {'sm': 'nnic', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC/RSCV', 'col': 'red'},
    {'sm': 'nesm', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'ESM/RSCV', 'col': 'green'},
    {'sm': 'fclk', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'FCLK/RSCV', 'col': 'orange'},
    {'sm': 'falk', 'am': 'rscv', 'ssm': '8', 'iiw': 1, 'legend': 'FALK/RSCV', 'col': 'cyan'},
    {'sm': 'iclk', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK/RSCV', 'col': 'magenta'},
    {'sm': 'ialk', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'IALK/RSCV', 'col': 'black'}
]

# compare different SSMs
config_id = 7
out_dirs[config_id] = 'comparing_ssm'
tracker_configs[config_id] = [
    {'sm': 'nesm', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': '8DOF', 'col': 'red'},
    {'sm': 'nesm', 'am': 'rscv', 'ssm': '6', 'iiw': 0, 'legend': '6DOF', 'col': 'green'},
    {'sm': 'nesm', 'am': 'rscv', 'ssm': '4', 'iiw': 0, 'legend': '4DOF', 'col': 'orange'},
    {'sm': 'nesm', 'am': 'rscv', 'ssm': '2', 'iiw': 0, 'legend': '2DOF', 'col': 'cyan'},
    {'sm': 'nesm', 'am': 'ncc', 'ssm': '3', 'iiw': 0, 'legend': '3DOF', 'col': 'blue'},
    {'sm': 'nesm', 'am': 'rscv', 'ssm': 'l8', 'iiw': 0, 'legend': 'Lie 8DOF', 'col': 'black'}
]

# compare low dof registration with learning
config_id = 8
out_dirs[config_id] = 'comparing_2dof_rt_lt'
tracker_configs[config_id] = [
    {'sm': 'dsst', 'am': 'ssd50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'DSST', 'col': 'red',
      'use_arch': 1, 'arch_name': 'dsst_kcf_rct_tld_cmt', 'in_arch_path': 'log/tracking_data'},
    {'sm': 'kcf', 'am': 'ssd50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'KCF', 'col': 'green',
      'use_arch': 1, 'arch_name': 'dsst_kcf_rct_tld_cmt', 'in_arch_path': 'log/tracking_data'},
    {'sm': 'tld', 'am': 'ssd50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'TLD', 'col': 'magenta',
      'use_arch': 1, 'arch_name': 'dsst_kcf_rct_tld_cmt', 'in_arch_path': 'log/tracking_data'},
    {'sm': 'esmDJSSH2', 'am': 'ncc50r30i4u', 'ssm': '2', 'iiw': 1, 'legend': 'ESM', 'col': 'orange',
      'use_arch': 1, 'arch_name': 'robust__all_SMs__translation', 'in_arch_path': 'tracking_data'},
    {'sm': 'fclk', 'am': 'rscv', 'ssm': '2', 'iiw': 0, 'legend': 'FCLK', 'col': 'orange'},
    {'sm': 'falk', 'am': 'rscv', 'ssm': '2', 'iiw': 1, 'legend': 'FALK', 'col': 'cyan'},
    {'sm': 'nesm', 'am': 'rscv', 'ssm': 'l8', 'iiw': 0, 'legend': 'Lie 8DOF', 'col': 'black'}
]

# comparing different appearance models
config_id = 9
out_dirs[config_id] = 'comparing_am'
tracker_configs[config_id] = [
    {'sm': 'nesm', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'RSCV', 'col': 'red'},
    {'sm': 'nesm', 'am': 'scv', 'ssm': '8', 'iiw': 0, 'legend': 'SCV', 'col': 'green'},
    {'sm': 'nesm', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'NCC', 'col': 'orange',
    },
    {'sm': 'nesm', 'am': 'ssd', 'ssm': '8', 'iiw': 0, 'legend': 'SSD', 'col': 'cyan'},
    {'sm': 'fclk', 'am': 'rscv', 'ssm': '8', 'iiw': 0, 'legend': 'FCRSCV', 'col': 'magenta'},
    {'sm': 'fclk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'FCNCC', 'col': 'black'}
]

config_id = 10
out_dirs[config_id] = 'comparing_am_arch'
tracker_configs[config_id] = [
    {'sm': 'fclkC1', 'am': 'ssd50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'SSD', 'col': 'red',
     'arch_name': 'ssd_like_fc_ic_esm_nnic_fa_ia_aesm__50r__30i_4u'},
    {'sm': 'fclkC2', 'am': 'ncc50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NCC', 'col': 'green',
     'arch_name': 'robust_ic_fc_esm_nnic_fa_ia_aesm__50r__30i__4u'},
    {'sm': 'fclkC2', 'am': 'mi8b50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'MI', 'col': 'orange',
     'arch_name': 'robust_ic_fc_esm_nnic_fa_ia_aesm__50r__30i__4u'},
    {'sm': 'fclkC2', 'am': 'ccre8b50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'CCRE', 'col': 'cyan',
     'arch_name': 'robust_ic_fc_esm_nnic_fa_ia_aesm__50r__30i__4u'},
    {'sm': 'fclk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'FCNCC', 'col': 'black'}
]

config_id = 11
out_dirs[config_id] = 'comparing_learning_trackers'
tracker_configs[config_id] = [
    {'sm': 'dsst', 'am': 'miIN50r30i8b', 'ssm': '8', 'iiw': 0, 'legend': 'IN', 'col': 'red'},
    {'sm': 'kcf', 'am': 'rscv', 'ssm': '6', 'iiw': 0, 'legend': '6DOF', 'col': 'green'},
    {'sm': 'cmt', 'am': 'rscv', 'ssm': '4', 'iiw': 0, 'legend': '4DOF', 'col': 'orange'},
    {'sm': 'tld', 'am': 'rscv', 'ssm': '2', 'iiw': 0, 'legend': '2DOF', 'col': 'cyan'},
    {'sm': 'rct', 'am': 'rscv', 'ssm': '3', 'iiw': 0, 'legend': '3DOF', 'col': 'blue'}
]
config_id = 12
out_dirs[config_id] = 'comparing_sm_ssd_like'
tracker_configs[config_id] = [
    {'sm': 'nn1k', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NN1K', 'col': 'red',
     'arch_name': 'ssd_like__nn1k__50r'},
    {'sm': 'nn10k', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NN10K', 'col': 'green',
     'arch_name': 'ssd_like__nn5k10k'},
    {'sm': 'iclkI1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK', 'col': 'orange',
     'arch_name': 'ssd_like_fc_ic_esm_nnic_fa_ia_aesm__50r__30i_4u'},
    {'sm': 'nnic1kI1', 'am': 'rscv50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC', 'col': 'cyan',
     'arch_name': 'ssd_like_fc_ic_esm_nnic_fa_ia_aesm__50r__30i_4u'},
    {'sm': 'fclk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'FCNCC', 'col': 'black',
    }
]
config_id = 13
out_dirs[config_id] = 'comparing_sm_ccre'
tracker_configs[config_id] = [
    {'sm': 'nn1k', 'am': 'ccre8b50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NN1K', 'col': 'red',
     'arch_name': 'robust__nn1k__50r'},
    {'sm': 'nn10k', 'am': 'ccre8b50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NN10K', 'col': 'green',
     'arch_name': 'robust__nn5k10k'},
    {'sm': 'iclkI1', 'am': 'ccre8b50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'ICLK', 'col': 'orange',
     'arch_name': 'robust_ic_fc_esm_nnic_fa_ia_aesm__50r__30i__4u'},
    {'sm': 'nnic1kI1', 'am': 'ccre8b50r30i4u', 'ssm': '8', 'iiw': 0, 'legend': 'NNIC', 'col': 'cyan',
     'arch_name': 'robust_ic_fc_esm_nnic_fa_ia_aesm__50r__30i__4u'},
    {'sm': 'fclk', 'am': 'ncc', 'ssm': '8', 'iiw': 0, 'legend': 'FCNCC', 'col': 'black',
    }
]

config_id = 14
out_dirs[config_id] = 'dsst3'
tracker_configs[config_id] = [
     {'sm': 'dsst2', 'am': '50r30i4u', 'ssm': '4', 'iiw': 0, 'legend': 'DSST2', 'col': 'red'},
    {'sm': 'dsst3', 'am': '50r30i4u', 'ssm': '4', 'iiw': 0, 'legend': 'DSST3', 'col': 'green'},
     {'sm': 'dsst4', 'am': '50r30i4u', 'ssm': '4', 'iiw': 0, 'legend': 'DSST4', 'col': 'blue'}
]

config_id = 15
out_dirs[config_id] = 'Live'
tracker_configs[config_id] = [
     {'fname': 'rkl400636591_ncc_8_0', 'use-arch': 0, 'legend': 'Live', 'col': 'red'}
]

config_id = 16
out_dirs[config_id] = 'Live'
tracker_configs[config_id] = [
     {'sm': 'gt', 'am': '50r30i4u', 'ssm': '4', 'iiw': 0, 'legend': '', 'col': 'red'},
]