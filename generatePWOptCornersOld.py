import distanceUtils
from distanceGrid import *
import time
import os
from Misc import getParamDict

if __name__ == '__main__':

    db_root_path = 'E:/UofA/Thesis/#Code/Datasets'
    actor = 'Human'

    params_dict = getParamDict()
    param_ids = readDistGridParams()

    tracker_types = params_dict['tracker_types']
    grid_types = params_dict['grid_types']
    inc_types = params_dict['inc_types']
    filter_types = params_dict['filter_types']
    sequences = params_dict['sequences']
    opt_types = params_dict['opt_types']

    seq_id = param_ids['seq_id']
    grid_id = param_ids['grid_id']
    appearance_id = param_ids['appearance_id']
    inc_id = param_ids['inc_id']
    tracker_id = param_ids['tracker_id']
    start_id = param_ids['start_id']
    filter_id = param_ids['filter_id']
    kernel_size = param_ids['kernel_size']
    opt_id = param_ids['opt_id']

    mi_bins = param_ids['mi_bins']
    scv_bins = param_ids['scv_bins']
    ccre_bins = param_ids['ccre_bins']

    dof = param_ids['dof']

    write_img_data = 0
    write_track_data = 1
    write_gt_data = 0
    write_dist_data = 1
    use_jaccard_error = 0

    std_resx = 50
    std_resy = 50
    grid_res = 10

    tx_res = grid_res
    ty_res = grid_res
    theta_res = grid_res
    scale_res = grid_res
    a_res = grid_res
    b_res = grid_res
    v1_res = grid_res
    v2_res = grid_res

    common_thresh = 1.0

    trans_thr = common_thresh
    theta_thresh, scale_thresh = [np.pi / 32, common_thresh]
    a_thresh, b_thresh = [common_thresh, common_thresh]
    v1_thresh, v2_thresh = [common_thresh, common_thresh]

    tx_min, tx_max = [-trans_thr, trans_thr]
    ty_min, ty_max = [-trans_thr, trans_thr]
    theta_min, theta_max = [-theta_thresh, theta_thresh]
    scale_min, scale_max = [-scale_thresh, scale_thresh]
    a_min, a_max = [-a_thresh, a_thresh]
    b_min, b_max = [-b_thresh, b_thresh]
    v1_min, v1_max = [-v1_thresh, v1_thresh]
    v2_min, v2_max = [-v2_thresh, v2_thresh]

    tx_vec = np.linspace(tx_min, tx_max, tx_res)
    ty_vec = np.linspace(ty_min, ty_max, ty_res)
    theta_vec = np.linspace(theta_min, theta_max, theta_res)
    scale_vec = np.linspace(scale_min, scale_max, scale_res)
    a_vec = np.linspace(a_min, a_max, a_res)
    b_vec = np.linspace(b_min, b_max, b_res)
    v1_vec = np.linspace(v1_min, v1_max, v1_res)
    v2_vec = np.linspace(v2_min, v2_max, v2_res)

    tx_vec = np.insert(tx_vec, np.argwhere(tx_vec >= 0)[0, 0], 0).astype(np.float64)
    ty_vec = np.insert(ty_vec, np.argwhere(ty_vec >= 0)[0, 0], 0).astype(np.float64)
    theta_vec = np.insert(theta_vec, np.argwhere(theta_vec >= 0)[0, 0], 0).astype(np.float64)
    scale_vec = np.insert(scale_vec, np.argwhere(scale_vec >= 0)[0, 0], 0).astype(np.float64)
    a_vec = np.insert(a_vec, np.argwhere(a_vec >= 0)[0, 0], 0).astype(np.float64)
    b_vec = np.insert(b_vec, np.argwhere(b_vec >= 0)[0, 0], 0).astype(np.float64)
    v1_vec = np.insert(v1_vec, np.argwhere(v1_vec >= 0)[0, 0], 0).astype(np.float64)
    v2_vec = np.insert(v2_vec, np.argwhere(v2_vec >= 0)[0, 0], 0).astype(np.float64)

    arg_id = 1
    if len(sys.argv) > arg_id:
        seq_id = int(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        filter_id = int(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        inc_type = sys.argv[arg_id]
        arg_id += 1
    if len(sys.argv) > arg_id:
        write_gt_data = int(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        write_track_data = int(sys.argv[arg_id])
        arg_id += 1
    if len(sys.argv) > arg_id:
        use_pre_opt = int(sys.argv[arg_id])
        arg_id += 1

    if seq_id >= len(sequences):
        print 'Invalid dataset_id: ', seq_id
        sys.exit()
    if filter_id >= len(filter_types):
        print 'Invalid filter_id: ', filter_id
        sys.exit()
    if opt_id >= len(opt_types):
        print 'Invalid opt_id: ', opt_id
        sys.exit()

    seq_name = sequences[seq_id]
    filter_type = filter_types[filter_id]
    opt_type = opt_types[opt_id]
    inc_type = inc_types[inc_id]

    print 'seq_id: ', seq_id
    print 'seq_name: ', seq_name
    print 'inc_type: ', inc_type
    print 'filter_type: ', filter_type
    print 'kernel_size: ', kernel_size
    print 'opt_type: ', opt_type

    src_folder = db_root_path + '/' + actor + '/' + seq_name

    ground_truth_fname = db_root_path + '/' + actor + '/' + seq_name + '.txt'
    ground_truth = readTrackingData(ground_truth_fname)
    no_of_frames = ground_truth.shape[0]
    print 'no_of_frames: ', no_of_frames

    end_id = no_of_frames

    init_corners = np.asarray([ground_truth[0, 0:2].tolist(),
                               ground_truth[0, 2:4].tolist(),
                               ground_truth[0, 4:6].tolist(),
                               ground_truth[0, 6:8].tolist()]).T

    std_pts, std_corners = getNormalizedUnitSquarePts(std_resx, std_resy)
    std_pts_hm = util.homogenize(std_pts)
    std_corners_hm = util.homogenize(std_corners)
    (init_corners_norm, init_norm_mat) = getNormalizedPoints(init_corners)
    init_hom_mat = np.mat(util.compute_homography(std_corners, init_corners_norm))
    init_pts_norm = util.dehomogenize(init_hom_mat * std_pts_hm)
    init_pts = util.dehomogenize(init_norm_mat * util.homogenize(init_pts_norm))

    init_img = cv2.imread(src_folder + '/frame{:05d}.jpg'.format(1))
    init_img_gs = cv2.cvtColor(init_img, cv2.cv.CV_BGR2GRAY).astype(np.float64)
    if filter_type != 'none':
        init_img_gs = applyFilter(init_img_gs, filter_type, kernel_size)

    n_pts = std_resx * std_resy
    init_pixel_vals = np.mat([util.bilin_interp(init_img_gs, init_pts[0, pt_id], init_pts[1, pt_id]) for pt_id in
                              xrange(n_pts)])

    if start_id > 1:
        curr_corners = np.asarray([ground_truth[start_id - 1, 0:2].tolist(),
                                   ground_truth[start_id - 1, 2:4].tolist(),
                                   ground_truth[start_id - 1, 4:6].tolist(),
                                   ground_truth[start_id - 1, 6:8].tolist()]).T

        (curr_corners_norm, curr_norm_mat) = getNormalizedPoints(curr_corners)
        curr_hom_mat = np.mat(util.compute_homography(std_corners, curr_corners_norm))
        curr_pts_norm = util.dehomogenize(curr_hom_mat * std_pts_hm)
        curr_pts = util.dehomogenize(curr_norm_mat * util.homogenize(curr_pts_norm))
    else:
        curr_corners = init_corners
        curr_corners_norm = init_corners_norm
        curr_norm_mat = init_norm_mat
        curr_hom_mat = init_hom_mat
        curr_pts = init_pts

    gt_col = (0, 0, 0)
    trans_col = (255, 255, 255)
    rs_col = (0, 0, 255)
    shear_col = (0, 255, 0)
    proj_col = (255, 255, 0)

    show_gt = 1
    show_trans = 1
    show_rs = 1
    show_shear = 1
    show_proj = 1

    window_name = 'Piecewise Optimization'
    cv2.namedWindow(window_name)

    if filter_type != 'none':
        track_img_folder = 'Tracked Images/' + seq_name + '_' + filter_type + str(
            kernel_size) + '/' + inc_type + '_' + opt_type + str(dof)
        track_data_folder = 'Tracking Data/' + seq_name + '_' + filter_type + str(
            kernel_size) + '/' + inc_type + '_' + opt_type + str(dof)
        dist_folder = 'Distance Data/#PW/' + seq_name + '_' + filter_type + str(
            kernel_size) + '/' + inc_type + '_' + opt_type + str(dof)
    else:
        track_img_folder = 'Tracked Images/' + seq_name + '/' + inc_type + '_' + opt_type + str(dof)
        track_data_folder = 'Tracking Data/' + seq_name + '/' + inc_type + '_' + opt_type + str(dof)
        dist_folder = 'Distance Data/#PW/' + seq_name + '/' + inc_type + '_' + opt_type + str(dof)

    if not os.path.exists(track_img_folder):
        os.makedirs(track_img_folder)

    if not os.path.exists(track_data_folder):
        os.makedirs(track_data_folder)

    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)
        os.makedirs(dist_folder + '/trans')
        os.makedirs(dist_folder + '/rs')
        os.makedirs(dist_folder + '/shear')
        os.makedirs(dist_folder + '/proj')

    if write_dist_data:
        np.savetxt(dist_folder + '/trans/tx_vec.txt', tx_vec)
        np.savetxt(dist_folder + '/trans/ty_vec.txt', ty_vec)
        np.savetxt(dist_folder + '/rs/scale_vec.txt', scale_vec)
        np.savetxt(dist_folder + '/rs/theta_vec.txt', theta_vec)
        np.savetxt(dist_folder + '/shear/a_vec.txt', a_vec)
        np.savetxt(dist_folder + '/shear/b_vec.txt', b_vec)
        np.savetxt(dist_folder + '/proj/v1_vec.txt', v1_vec)
        np.savetxt(dist_folder + '/proj/v2_vec.txt', v2_vec)

    track_errors = []
    track_params = []
    gt_params = []

    for frame_id in xrange(start_id, end_id):

        print 'frame_id: ', frame_id
        err_text = ''
        frame_err = []
        frame_params = []
        pw_opt_mat = np.identity(3)

        # ret, curr_img = cap.read()
        curr_img = cv2.imread(src_folder + '/frame{:05d}.jpg'.format(frame_id + 1))
        if curr_img is None:
            break
        curr_img_gs = cv2.cvtColor(curr_img, cv2.cv.CV_BGR2GRAY).astype(np.float64)
        if filter_type != 'none':
            curr_img_gs = applyFilter(curr_img_gs, filter_type, kernel_size)

        gt_corners = np.asarray([ground_truth[frame_id, 0:2].tolist(),
                                 ground_truth[frame_id, 2:4].tolist(),
                                 ground_truth[frame_id, 4:6].tolist(),
                                 ground_truth[frame_id, 6:8].tolist()]).T
        (gt_corners_norm, gt_norm_mat) = getNormalizedPoints(gt_corners)

        if write_gt_data:
            gt_hom_mat = np.mat(util.compute_homography(curr_corners_norm, gt_corners_norm))
            tx_gt, ty_gt, theta_gt, scale_gt, a_gt, b_gt, v1_gt, v2_gt = getHomographyParamsInverse(gt_hom_mat)
            gt_params.append([tx_gt, ty_gt, theta_gt, scale_gt, a_gt, b_gt, v1_gt, v2_gt])

        if show_gt:
            drawRegion(curr_img, gt_corners, gt_col, 1)
            cv2.putText(curr_img, "Actual", (int(gt_corners[0, 0]), int(gt_corners[1, 0])),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, gt_col)

        # print 'gt_corners: ', gt_corners
        start_time = time.clock()

        # pw_hom_mat = curr_hom_mat
        # pw_std_pts = std_pts
        # pw_std_corners_hm = std_corners_hm

        if inc_type == 'fc':
            # curr_pixel_vals = np.mat(
            # [util.bilin_interp(curr_img_gs, curr_pts[0, pt_id], curr_pts[1, pt_id]) for pt_id in
            # xrange(n_pts)])

            if dof >= 2:
                # ------------------------------------ TRANSLATION ------------------------------------#

                trans_dist_grid = getTransDistanceGridPre(std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                          init_pixel_vals, tx_vec, ty_vec, getSSDPoints)

                if write_dist_data:
                    trans_dist_grid.tofile(dist_folder + '_trans/dist_grid_' + str(frame_id) + '.bin')
                trans_dist_grid[trans_dist_grid < 0] = float("inf")
                row_id, col_id = getIndexOfMinimum(trans_dist_grid)
                tx = tx_vec[row_id]
                ty = ty_vec[col_id]
                trans_opt_mat = getTranslationMatrix(tx, ty)
                frame_params.append(tx)
                frame_params.append(ty)

                pw_opt_mat = trans_opt_mat
                trans_hom_mat = curr_hom_mat * pw_opt_mat
                trans_opt_corners = util.dehomogenize(curr_norm_mat * trans_hom_mat * std_corners_hm)
                curr_corners = trans_opt_corners

                trans_error = math.sqrt(np.sum(np.square(trans_opt_corners - gt_corners)) / 4)
                frame_err.append(trans_error)
                err_text = err_text + 'trans: {:7.4f} '.format(trans_error)

                # pw_hom_mat = trans_hom_mat
                # pw_std_pts = trans_std_pts
                # pw_std_corners_hm = trans_std_corners_hm


                print 'trans:: tx: ', tx, 'ty: ', ty, 'dist:', trans_dist_grid[
                    row_id, col_id], 'error:', trans_error
                if show_trans:
                    drawRegion(curr_img, trans_opt_corners, trans_col, 1)
                    cv2.putText(curr_img, "Trans", (int(trans_opt_corners[0, 0]), int(trans_opt_corners[1, 0])),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, trans_col)
                    # cv2.imshow(window_name, curr_img)
                    # cv2.waitKey(0)

            if dof >= 4:
                # ------------------------------------ ROTATION-SCALING ------------------------------------#

                if opt_type == 'pre':
                    pw_std_pts = util.dehomogenize(pw_opt_mat * std_pts_hm)
                    rs_dist_grid = getRSDistanceGridComp(pw_std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                         init_pixel_vals,
                                                         scale_vec, theta_vec, getSSDPoints)
                elif opt_type == 'post':
                    pw_hom_mat = curr_hom_mat * pw_opt_mat
                    rs_dist_grid = getRSDistanceGridComp(std_pts, pw_hom_mat, curr_norm_mat, curr_img_gs,
                                                         init_pixel_vals,
                                                         scale_vec, theta_vec, getSSDPoints)
                elif opt_type == 'independent':
                    rs_dist_grid = getRSDistanceGridComp(std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                         init_pixel_vals,
                                                         scale_vec, theta_vec, getSSDPoints)

                if write_dist_data:
                    rs_dist_grid.tofile(dist_folder + '_rs/dist_grid_' + str(frame_id) + '.bin')

                rs_dist_grid[rs_dist_grid < 0] = float("inf")
                row_id, col_id = getIndexOfMinimum(rs_dist_grid)
                scale = scale_vec[row_id]
                theta = theta_vec[col_id]
                rot_opt_mat = getRotationMatrix(theta)
                scale_opt_mat = getScalingMatrix(scale)
                frame_params.append(scale)
                frame_params.append(theta)

                # rs_std_pts_hm = scale_opt_mat * rot_opt_mat * trans_std_pts_hm
                # rs_std_pts = util.dehomogenize(rs_std_pts_hm)
                # rs_std_corners_hm = scale_opt_mat * rot_opt_mat * trans_std_corners_hm

                if opt_type == 'pre' or opt_type == 'independent':
                    pw_opt_mat = scale_opt_mat * rot_opt_mat * pw_opt_mat
                elif opt_type == 'post':
                    pw_opt_mat = pw_opt_mat * scale_opt_mat * rot_opt_mat

                rs_hom_mat = curr_hom_mat * pw_opt_mat
                rs_opt_corners = util.dehomogenize(curr_norm_mat * rs_hom_mat * std_corners_hm)
                curr_corners = rs_opt_corners

                rs_error = math.sqrt(np.sum(np.square(rs_opt_corners - gt_corners)) / 4)
                frame_err.append(rs_error)
                err_text = err_text + 'rs: {:7.4f} '.format(rs_error)
                print 'rs:: theta: ', theta, 'scale: ', scale, 'dist:', rs_dist_grid[row_id, col_id], 'error:', rs_error

                # pw_hom_mat = rs_hom_mat
                # pw_std_pts = rs_std_pts
                # pw_std_corners_hm = rs_std_corners_hm
                # print 'rs_opt_corners: ', rs_opt_corners
                if show_rs:
                    drawRegion(curr_img, rs_opt_corners, rs_col, 1)
                    cv2.putText(curr_img, "RS", (int(rs_opt_corners[0, 0]), int(rs_opt_corners[1, 0])),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, rs_col)
                    # cv2.imshow(window_name, curr_img)
                    # cv2.waitKey(0)

            if dof >= 6:
                # ------------------------------------ SHEAR ------------------------------------#

                if opt_type == 'pre':
                    pw_std_pts = util.dehomogenize(pw_opt_mat * std_pts_hm)
                    shear_dist_grid = getShearDistanceGridComp(pw_std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                               init_pixel_vals,
                                                               a_vec, b_vec, getSSDPoints)
                elif opt_type == 'post':
                    pw_hom_mat = curr_hom_mat * pw_opt_mat
                    shear_dist_grid = getShearDistanceGridComp(std_pts, pw_hom_mat, curr_norm_mat, curr_img_gs,
                                                               init_pixel_vals,
                                                               a_vec, b_vec, getSSDPoints)
                elif opt_type == 'independent':
                    shear_dist_grid = getShearDistanceGridComp(std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                               init_pixel_vals,
                                                               a_vec, b_vec, getSSDPoints)

                if write_dist_data:
                    shear_dist_grid.tofile(dist_folder + '_shear/dist_grid_' + str(frame_id) + '.bin')

                shear_dist_grid[shear_dist_grid < 0] = float("inf")
                row_id, col_id = getIndexOfMinimum(shear_dist_grid)
                a = a_vec[row_id]
                b = b_vec[col_id]
                shear_opt_mat = getShearingMatrix(a, b)
                frame_params.append(a)
                frame_params.append(b)

                # shear_std_pts_hm = shear_opt_mat * util.homogenize(rs_std_pts)
                # shear_std_pts = util.dehomogenize(shear_std_pts_hm)
                # shear_std_corners_hm = shear_opt_mat * rs_std_corners_hm

                if opt_type == 'pre' or opt_type == 'independent':
                    pw_opt_mat = shear_opt_mat * pw_opt_mat
                elif opt_type == 'post':
                    pw_opt_mat = pw_opt_mat * shear_opt_mat

                shear_hom_mat = curr_hom_mat * pw_opt_mat
                shear_opt_corners = util.dehomogenize(curr_norm_mat * shear_hom_mat * std_corners_hm)
                curr_corners = shear_opt_corners

                shear_error = math.sqrt(np.sum(np.square(shear_opt_corners - gt_corners)) / 4)
                frame_err.append(shear_error)
                err_text = err_text + 'shear: {:7.4f} '.format(shear_error)

                # pw_hom_mat = shear_hom_mat
                # pw_std_pts = shear_std_pts
                # pw_std_corners_hm = shear_std_corners_hm

                print 'shear:: a: ', a, 'b: ', b, 'dist:', shear_dist_grid[
                    row_id, col_id], 'error:', shear_error

                # print 'shear_opt_corners: ', shear_opt_corners

                if show_shear:
                    drawRegion(curr_img, shear_opt_corners, shear_col, 1)
                    cv2.putText(curr_img, "Shear", (int(shear_opt_corners[0, 0]), int(shear_opt_corners[1, 0])),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, shear_col)
                    # cv2.imshow(window_name, curr_img)
                    # cv2.waitKey(0)

            if dof == 8:
                # ------------------------------------ PROJECTION ------------------------------------#

                if opt_type == 'pre':
                    pw_std_pts = util.dehomogenize(pw_opt_mat * std_pts_hm)
                    proj_dist_grid = getProjDistanceGridComp(pw_std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                             init_pixel_vals,
                                                             v1_vec, v2_vec, getSSDPoints)
                elif opt_type == 'post':
                    pw_hom_mat = curr_hom_mat * pw_opt_mat
                    proj_dist_grid = getProjDistanceGridComp(std_pts, pw_hom_mat, curr_norm_mat, curr_img_gs,
                                                             init_pixel_vals,
                                                             v1_vec, v2_vec, getSSDPoints)
                elif opt_type == 'independent':
                    proj_dist_grid = getProjDistanceGridComp(std_pts, curr_hom_mat, curr_norm_mat, curr_img_gs,
                                                             init_pixel_vals,
                                                             v1_vec, v2_vec, getSSDPoints)

                if write_dist_data:
                    proj_dist_grid.tofile(dist_folder + '_proj/dist_grid_' + str(frame_id) + '.bin')

                proj_dist_grid[proj_dist_grid < 0] = float("inf")
                row_id, col_id = getIndexOfMinimum(proj_dist_grid)
                v1 = v1_vec[row_id]
                v2 = v2_vec[col_id]
                proj_opt_mat = getProjectionMatrix(v1, v2)
                frame_params.append(v1)
                frame_params.append(v2)

                # proj_std_pts_hm = proj_opt_mat * util.homogenize(pw_std_pts)
                # proj_std_pts = util.dehomogenize(proj_std_pts_hm)
                # proj_std_corners_hm = proj_opt_mat * pw_std_corners_hm

                if opt_type == 'pre' or opt_type == 'independent':
                    pw_opt_mat = proj_opt_mat * pw_opt_mat
                elif opt_type == 'post':
                    pw_opt_mat = pw_opt_mat * proj_opt_mat

                proj_hom_mat = curr_hom_mat * pw_opt_mat
                proj_opt_corners = util.dehomogenize(curr_norm_mat * proj_hom_mat * std_corners_hm)
                curr_corners = proj_opt_corners

                proj_error = math.sqrt(np.sum(np.square(proj_opt_corners - gt_corners)) / 4)
                frame_err.append(proj_error)
                err_text = err_text + 'proj: {:7.4f} '.format(proj_error)

                print 'proj:: v1: ', v1, 'v2: ', v2, 'dist:', proj_dist_grid[row_id, col_id], 'error:', proj_error
                # print 'proj_opt_corners: ', proj_opt_corners
                if show_proj:
                    drawRegion(curr_img, proj_opt_corners, proj_col, 1)
                    cv2.putText(curr_img, "Proj", (int(proj_opt_corners[0, 0]), int(proj_opt_corners[1, 0])),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, proj_col)
                    # cv2.imshow(window_name, curr_img)
                    # cv2.waitKey(0)

            cv2.putText(curr_img, err_text, (5, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255))
            if write_track_data:
                track_errors.append(frame_err)
                track_params.append(frame_params)
        else:
            curr_corners = gt_corners

        end_time = time.clock()
        curr_time = end_time - start_time
        curr_fps = 1.0 / curr_time
        # print 'curr_time: ', curr_time, 'secs'

        fname = '{:s}/frame{:05d}.jpg'.format(track_img_folder, frame_id)
        # print 'fname: ', fname
        cv2.imwrite(fname, curr_img)
        cv2.imshow(window_name, curr_img)
        key = cv2.waitKey(1)
        if key == 27:
            break

        # curr_corners = gt_corners
        curr_corners_norm, curr_norm_mat = getNormalizedPoints(curr_corners)

        try:
            curr_hom_mat = np.mat(util.compute_homography(std_corners, curr_corners_norm))
        except:
            print 'Error: SVD did not converge while computing homography for: \n', curr_corners_norm
            break
        curr_pts_norm = util.dehomogenize(curr_hom_mat * std_pts_hm)
        curr_pts = util.dehomogenize(curr_norm_mat * util.homogenize(curr_pts_norm))

    if write_track_data:
        np.savetxt('{:s}/track_errors.txt'.format(track_data_folder), np.array(track_errors), fmt='%13.8f',
                   delimiter='\t')
        np.savetxt('{:s}/track_params.txt'.format(track_data_folder), np.array(track_params), fmt='%12.8f',
                   delimiter='\t')
    if write_gt_data:
        np.savetxt('{:s}/gt_params.txt'.format(track_data_folder), np.array(gt_params), fmt='%12.8f', delimiter='\t')

