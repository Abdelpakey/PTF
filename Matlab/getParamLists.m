tracker_types = {
    'gt',...%0
    'esm',...%1
    'ic',...%2
    'nnic',...%3
    'pf',...%4
    'pw',...%5
    'ppw'...%6
    };
filter_types = {
    'none',...%0
    'gauss',...%1
    'box',...%2
    'norm_box',...%3
    'bilateral',...%4
    'median',...%5
    'gabor',...%6
    'sobel',...%7
    'scharr',...%8
    'LoG',...%9
    'DoG',...%10
    'laplacian',...%11
    'canny'%12
    };
inc_types = {'fc',...%0
    'ic',...%1
    'fa',...%2
    'ia'...%3
    };
pw_opt_types = {
    'pre',...%0
    'post',...%1
    'ind'%2
    };
error_types = {
    'mcd',...%0
    'cl',...%1
    'jaccard'%2
    };
grid_types = {
    'trans',...%0
    'rs',...%1
    'shear',...%2
    'proj',...%3
    'rtx',...%4
    'rty',...%5
    'stx',...%6
    'sty',...%7
    'trans2'%8
    };
appearance_models = {
    'ssd',...%0
    'scv',...%1
    'ncc'...%2
    'mi'...%3
    'ccre',...%4
    'hssd',...%5
    'jht',...%6
    'mi_old',...%7
    'ncc2',...%8
    'scv2',...%9
    'mi2',...%10
    'mssd',...%11
    'bmssd',...%12
    'bmi',...%13
    'crv',...%14
    'fkld',...%15
    'ikld',...%16
    'mkld',...%17
    'chis',...%18
    'ssim',...%19
    'fmaps'...%20
    };
sequences_tmt = {
    'nl_bookI_s3',...%0
    'nl_bookII_s3',...%1
    'nl_bookIII_s3',...%2
    'nl_cereal_s3',...%3
    'nl_juice_s3',...%4
    'nl_mugI_s3',...%5
    'nl_mugII_s3',...%6
    'nl_mugIII_s3',...%7
    'nl_bookI_s4',...%8
    'nl_bookII_s4',...%9
    'nl_bookIII_s4',...%10
    'nl_cereal_s4',...%11
    'nl_juice_s4',...%12
    'nl_mugI_s4',...%13
    'nl_mugII_s4',...%14
    'nl_mugIII_s4',...%15
    'nl_bus',...%16
    'nl_highlighting',...%17
    'nl_letter',...%18
    'nl_newspaper',...%19
    'nl_bookI_s1',...%20
    'nl_bookII_s1',...%21
    'nl_bookIII_s1',...%22
    'nl_cereal_s1',...%23
    'nl_juice_s1',...%24
    'nl_mugI_s1',...%25
    'nl_mugII_s1',...%26
    'nl_mugIII_s1',...%27
    'nl_bookI_s2',...%28
    'nl_bookII_s2',...%29
    'nl_bookIII_s2',...%30
    'nl_cereal_s2',...%31
    'nl_juice_s2',...%32
    'nl_mugI_s2',...%33
    'nl_mugII_s2',...%34
    'nl_mugIII_s2',...%35
    'nl_bookI_s5',...%36
    'nl_bookII_s5',...%37
    'nl_bookIII_s5',...%38
    'nl_cereal_s5',...%39
    'nl_juice_s5',...%40
    'nl_mugI_s5',...%41
    'nl_mugII_s5',...%42
    'nl_mugIII_s5',...%43
    'nl_bookI_si',...%44
    'nl_bookII_si',...%45
    'nl_cereal_si',...%46
    'nl_juice_si',...%47
    'nl_mugI_si',...%48
    'nl_mugIII_si',...%49
    'dl_bookI_s3',...%50
    'dl_bookII_s3',...%51
    'dl_bookIII_s3',...%52
    'dl_cereal_s3',...%53
    'dl_juice_s3',...%54
    'dl_mugI_s3',...%55
    'dl_mugII_s3',...%56
    'dl_mugIII_s3',...%57
    'dl_bookI_s4',...%58
    'dl_bookII_s4',...%59
    'dl_bookIII_s4',...%60
    'dl_cereal_s4',...%61
    'dl_juice_s4',...%62
    'dl_mugI_s4',...%63
    'dl_mugII_s4',...%64
    'dl_mugIII_s4',...%65
    'dl_bus',...%66
    'dl_highlighting',...%67
    'dl_letter',...%68
    'dl_newspaper',...%69
    'dl_bookI_s1',...%70
    'dl_bookII_s1',...%71
    'dl_bookIII_s1',...%72
    'dl_cereal_s1',...%73
    'dl_juice_s1',...%74
    'dl_mugI_s1',...%75
    'dl_mugII_s1',...%76
    'dl_mugIII_s1',...%77
    'dl_bookI_s2',...%78
    'dl_bookII_s2',...%79
    'dl_bookIII_s2',...%80
    'dl_cereal_s2',...%81
    'dl_juice_s2',...%82
    'dl_mugI_s2',...%83
    'dl_mugII_s2',...%84
    'dl_mugIII_s2',...%85
    'dl_bookI_s5',...%86
    'dl_bookII_s5',...%87
    'dl_bookIII_s5',...%88
    'dl_cereal_s5',...%89
    'dl_juice_s5',...%90
    'dl_mugI_s5',...%91
    'dl_mugIII_s5',...%92
    'dl_bookII_si',...%93
    'dl_cereal_si',...%94
    'dl_juice_si',...%95
    'dl_mugI_si',...%96
    'dl_mugIII_si',...%97
    'dl_mugII_si',...98
    'dl_mugII_s5',...99
    'nl_mugII_si',...100
    'robot_bookI',...101
    'robot_bookII',...102
    'robot_bookIII',...103
    'robot_cereal',...104
    'robot_juice',...105
    'robot_mugI',...106
    'robot_mugII',...107
    'robot_mugIII',...108
    };
sequences_ucsb={
    'bricks_dynamic_lighting',...%0
    'bricks_motion1',...%1
    'bricks_motion2',...%2
    'bricks_motion3',...%3
    'bricks_motion4',...%4
    'bricks_motion5',...%5
    'bricks_motion6',...%6
    'bricks_motion7',...%7
    'bricks_motion8',...%8
    'bricks_motion9',...%9
    'bricks_panning',...%10
    'bricks_perspective',...%11
    'bricks_rotation',...%12
    'bricks_static_lighting',...%13
    'bricks_unconstrained',...%14
    'bricks_zoom',...%15
    'building_dynamic_lighting',...%16
    'building_motion1',...%17
    'building_motion2',...%18
    'building_motion3',...%19
    'building_motion4',...%20
    'building_motion5',...%21
    'building_motion6',...%22
    'building_motion7',...%23
    'building_motion8',...%24
    'building_motion9',...%25
    'building_panning',...%26
    'building_perspective',...%27
    'building_rotation',...%28
    'building_static_lighting',...%29
    'building_unconstrained',...%30
    'building_zoom',...%31
    'mission_dynamic_lighting',...%32
    'mission_motion1',...%33
    'mission_motion2',...%34
    'mission_motion3',...%35
    'mission_motion4',...%36
    'mission_motion5',...%37
    'mission_motion6',...%38
    'mission_motion7',...%39
    'mission_motion8',...%40
    'mission_motion9',...%41
    'mission_panning',...%42
    'mission_perspective',...%43
    'mission_rotation',...%44
    'mission_static_lighting',...%45
    'mission_unconstrained',...%46
    'mission_zoom',...%47
    'paris_dynamic_lighting',...%48
    'paris_motion1',...%49
    'paris_motion2',...%50
    'paris_motion3',...%51
    'paris_motion4',...%52
    'paris_motion5',...%53
    'paris_motion6',...%54
    'paris_motion7',...%55
    'paris_motion8',...%56
    'paris_motion9',...%57
    'paris_panning',...%58
    'paris_perspective',...%59
    'paris_rotation',...%60
    'paris_static_lighting',...%61
    'paris_unconstrained',...%62
    'paris_zoom',...%63
    'sunset_dynamic_lighting',...%64
    'sunset_motion1',...%65
    'sunset_motion2',...%66
    'sunset_motion3',...%67
    'sunset_motion4',...%68
    'sunset_motion5',...%69
    'sunset_motion6',...%70
    'sunset_motion7',...%71
    'sunset_motion8',...%72
    'sunset_motion9',...%73
    'sunset_panning',...%74
    'sunset_perspective',...%75
    'sunset_rotation',...%76
    'sunset_static_lighting',...%77
    'sunset_unconstrained',...%78
    'sunset_zoom',...%79
    'wood_dynamic_lighting',...%80
    'wood_motion1',...%81
    'wood_motion2',...%82
    'wood_motion3',...%83
    'wood_motion4',...%84
    'wood_motion5',...%85
    'wood_motion6',...%86
    'wood_motion7',...%87
    'wood_motion8',...%88
    'wood_motion9',...%89
    'wood_panning',...%90
    'wood_perspective',...%91
    'wood_rotation',...%92
    'wood_static_lighting',...%93
    'wood_unconstrained',...%94
    'wood_zoom'%95
    };


sequences_lintrack = {
    'mouse_pad',...%0
    'phone',...%1
    'towel'%2
    };

sequences_lintrack_short = {
    'mouse_pad_1',...%0
    'mouse_pad_2',...%1
    'mouse_pad_3',...%2
    'mouse_pad_4',...%3
    'mouse_pad_5',...%4
    'mouse_pad_6',...%5
    'mouse_pad_7',...%6
    'phone_1',...%7
    'phone_2',...%8
    'phone_3',...%9
    'towel_1',...%10
    'towel_2',...%11
    'towel_3',...%12
    'towel_4'%13
    };

sequences_pami = {
    'acronis',...%0
    'bass',...%1
    'bear',...%2
    'board_robot',...%3
    'board_robot_2',...%4
    'book1',...%5
    'book2',...%6
    'book3',...%7
    'book4',...%8
    'box',...%9
    'box_robot',...%10
    'cat_cylinder',...%11
    'cat_mask',...%12
    'cat_plane',...%13
    'compact_disc',...%14
    'cube',...%15
    'dft_atlas_moving',...%16
    'dft_atlas_still',...%17
    'dft_moving',...%18
    'dft_still',...%19
    'juice',...%20
    'lemming',...%21
    'mascot',...%22
    'omni_magazine',...%23
    'omni_obelix',...%24
    'sylvester',...%25
    'table_top',...%26
    'tea'...%27
    };

sequences_cmt = {
    'board_robot',...%0
    'box_robot',...%1
    'cup_on_table',...%2
    'juice',...%3
    'lemming',...%4
    'liquor',...%5
    'sylvester',...%6
    'ball',...%7
    'car',...%8
    'car_2',...%9
    'carchase',...%10
    'dog1',...%11
    'gym',...%12
    'jumping',...%13
    'mountain_bike',...%14
    'person',...%15
    'person_crossing',...%16
    'person_partially_occluded',...%17
    'singer',...%18
    'track_running'%19
    };

sequences_metaio = {
    'bump_angle',...%0
    'bump_fast_close',...%1
    'bump_fast_far',...%2
    'bump_illumination',...%3
    'bump_range',...%4
    'grass_angle',...%5
    'grass_fast_close',...%6
    'grass_fast_far',...%7
    'grass_illumination',...%8
    'grass_range',...%9
    'isetta_angle',...%10
    'isetta_fast_close',...%11
    'isetta_fast_far',...%12
    'isetta_illumination',...%13
    'isetta_range',...%14
    'lucent_angle',...%15
    'lucent_fast_close',...%16
    'lucent_fast_far',...%17
    'lucent_illumination',...%18
    'lucent_range',...%19
    'macMini_angle',...%20
    'macMini_fast_close',...%21
    'macMini_fast_far',...%22
    'macMini_illumination',...%23
    'macMini_range',...%24
    'philadelphia_angle',...%25
    'philadelphia_fast_close',...%26
    'philadelphia_fast_far',...%27
    'philadelphia_illumination',...%28
    'philadelphia_range',...%29
    'stop_angle',...%30
    'stop_fast_close',...%31
    'stop_fast_far',...%32
    'stop_illumination',...%33
    'stop_range',...%34
    'wall_angle',...%35
    'wall_fast_close',...%36
    'wall_fast_far',...%37
    'wall_illumination',...%38
    'wall_range'%39
    };

sequences_vivid = {
    'pktest03',...%0
    'egtest01',...%1
    'egtest02',...%2
    'egtest03',...%3
    'egtest04',...%4
    'egtest05',...%5
    'pktest01',...%6
    'pktest02',...%7
    'redteam'%8
    };

sequences_vot = {
    'woman',...%0
    'ball',...%1
    'basketball',...%2
    'bicycle',...%3
    'bolt',...%4
    'car',...%5
    'david',...%6
    'diving',...%7
    'drunk',...%8
    'fernando',...%9
    'fish1',...%10
    'fish2',...%11
    'gymnastics',...%12
    'hand1',...%13
    'hand2',...%14
    'jogging',...%15
    'motocross',...%16
    'polarbear',...%17
    'skating',...%18
    'sphere',...%19
    'sunshade',...%20
    'surfing',...%21
    'torus',...%22
    'trellis',...%23
    'tunnel'%24
    };

sequences_vot16 = {
    'bag',...%0
    'ball1',...%1
    'ball2',...%2
    'basketball',...%3
    'birds1',...%4
    'birds2',...%5
    'blanket',...%6
    'bmx',...%7
    'bolt1',...%8
    'bolt2',...%9
    'book',...%10
    'butterfly',...%11
    'car1',...%12
    'car2',...%13
    'crossing',...%14
    'dinosaur',...%15
    'fernando',...%16
    'fish1',...%17
    'fish2',...%18
    'fish3',...%19
    'fish4',...%20
    'girl',...%21
    'glove',...%22
    'godfather',...%23
    'graduate',...%24
    'gymnastics1',...%25
    'gymnastics2',...%26
    'gymnastics3',...%27
    'gymnastics4',...%28
    'hand',...%29
    'handball1',...%30
    'handball2',...%31
    'helicopter',...%32
    'iceskater1',...%33
    'iceskater2',...%34
    'leaves',...%35
    'marching',...%36
    'matrix',...%37
    'motocross1',...%38
    'motocross2',...%39
    'nature',...%40
    'octopus',...%41
    'pedestrian1',...%42
    'pedestrian2',...%43
    'rabbit',...%44
    'racing',...%45
    'road',...%46
    'shaking',...%47
    'sheep',...%48
    'singer1',...%49
    'singer2',...%50
    'singer3',...%51
    'soccer1',...%52
    'soccer2',...%53
    'soldier',...%54
    'sphere',...%55
    'tiger',...%56
    'traffic',...%57
    'tunnel',...%58
    'wiper'...%59
    };

sequences_vtb = {
    'Basketball',...%0
    'Biker',...%1
    'Bird1',...%2
    'Bird2',...%3
    'BlurBody',...%4
    'BlurCar1',...%5
    'BlurCar2',...%6
    'BlurCar3',...%7
    'BlurCar4',...%8
    'BlurFace',...%9
    'BlurOwl',...%10
    'Board',...%11
    'Bolt',...%12
    'Bolt2',...%13
    'Box',...%14
    'Boy',...%15
    'Car1',...%16
    'Car2',...%17
    'Car4',...%18
    'Car24',...%19
    'CarDark',...%20
    'CarScale',...%21
    'ClifBar',...%22
    'Coke',...%23
    'Couple',...%24
    'Coupon',...%25
    'Crossing',...%26
    'Crowds',...%27
    'Dancer',...%28
    'Dancer2',...%29
    'David',...%30
    'David2',...%31
    'David3',...%32
    'Deer',...%33
    'Diving',...%34
    'Dog',...%35
    'Dog1',...%36
    'Doll',...%37
    'DragonBaby',...%38
    'Dudek',...%39
    'FaceOcc1',...%40
    'FaceOcc2',...%41
    'Fish',...%42
    'FleetFace',...%43
    'Football',...%44
    'Football1',...%45
    'Freeman1',...%46
    'Freeman3',...%47
    'Freeman4',...%48
    'Girl',...%49
    'Girl2',...%50
    'Gym',...%51
    'Human2',...%52
    'Human3',...%53
    'Human4',...%54
    'Human5',...%55
    'Human6',...%56
    'Human7',...%57
    'Human8',...%58
    'Human9',...%59
    'Ironman',...%60
    'Jogging',...%61
    'Jogging_2',...%62
    'Jump',...%63
    'Jumping',...%64
    'KiteSurf',...%65
    'Lemming',...%66
    'Liquor',...%67
    'Man',...%68
    'Matrix',...%69
    'Mhyang',...%70
    'MotorRolling',...%71
    'MountainBike',...%72
    'Panda',...%73
    'RedTeam',...%74
    'Rubik',...%75
    'Shaking',...%76
    'Singer1',...%77
    'Singer2',...%78
    'Skater',...%79
    'Skater2',...%80
    'Skating1',...%81
    'Skating2',...%82
    'Skating2_2',...%83
    'Skiing',...%84
    'Soccer',...%85
    'Subway',...%86
    'Surfer',...%87
    'Suv',...%88
    'Sylvester',...%89
    'Tiger1',...%90
    'Tiger2',...%91
    'Toy',...%92
    'Trans',...%93
    'Trellis',...%94
    'Twinnings',...%95
    'Vase',...%96
    'Walking',...%97
    'Walking2',...%98
    'Woman'%99
    };

sequences_trakmark = {
    'CV00_00',...%0
    'CV00_01',...%1
    'CV00_02',...%2
    'CV01_00',...%3
    'FS00_00',...%4
    'FS00_01',...%5
    'FS00_02',...%6
    'FS00_03',...%7
    'FS00_04',...%8
    'FS00_05',...%9
    'FS00_06',...%10
    'FS01_00',...%11
    'FS01_01',...%12
    'FS01_02',...%13
    'FS01_03',...%14
    'JR00_00',...%15
    'JR00_01',...%16
    'NC00_00',...%17
    'NC01_00',...%18
    'NH00_00',...%19
    'NH00_01'%20
    };

sequences_live = {
    'usb_cam',...%0
    'firewire_cam'...%1
    };

sequences_tmt_fine = {
    'fish_lure_left',...%0
    'fish_lure_right',...%1
    'fish_lure_fast_left',...%2
    'fish_lure_fast_right',...%3
    'key_task_left',...%4
    'key_task_right',...%5
    'key_task_fast_left',...%6
    'key_task_fast_right',...%7
    'hexagon_task_left',...%8
    'hexagon_task_right',...%9
    'hexagon_task_fast_left',...%10
    'hexagon_task_fast_right'%11
    };

sequences_tmt_fine_full = {
    'fish_lure_left',...%0
    'fish_lure_right',...%1
    'fish_lure_fast_left',...%2
    'fish_lure_fast_right',...%3
    'key_task_left',...%4
    'key_task_right',...%5
    'key_task_fast_left',...%6
    'key_task_fast_right',...%7
    'hexagon_task_left',...%8
    'hexagon_task_right',...%9
    'hexagon_task_fast_left',...%10
    'hexagon_task_fast_right',...%11
    'fish_lure_cam1',...%12
    'fish_lure_cam2',...%13
    'fish_lure_fast_cam1',...%14
    'fish_lure_fast_cam2',...%15
    'key_task_cam1',...%16
    'key_task_cam2',...%17
    'key_task_fast_cam1',...%18
    'key_task_fast_cam2',...%19
    'hexagon_task_cam1',...%20
    'hexagon_task_cam2',...%21
    'hexagon_task_fast_cam1',...%22
    'hexagon_task_fast_cam2',...%23
    };

sequences_mosaic = {
    'book_1',...%0
    'book_2',...%1
    'book_3',...%2
    'book_4',...%3
    'book_5',...%4
    'book_6',...%5
    'book_7',...%6
    'book_8',...%7
    'poster_1',...%8
    'poster_2',...%9
    'poster_3',...%10
    'poster_4',...%11
    'poster_5',...%12
    'poster_6',...%13
    'poster_7',...%14
    'poster_8',...%15
    'poster_9'%16
    };

sequences_misc = {
    'uav_sim',...%0
    'chess_board_1',...%1
    'chess_board_2',...%2
    'chess_board_3',...%3
    'chess_board_4'%4
    };

sequences_synthetic = {
    'bear',...%0
    'board_robot',...%1
    'book4',...%2
    'box',...%3
    'box_robot',...%4
    'building_dynamic_lighting',...%5
    'cat_cylinder',...%6
    'cube',...%7
    'dft_still',...%8
    'lemming',...%9
    'mission_dynamic_lighting',...%10
    'mouse_pad',...%11
    'nl_bookI_s3',...%12
    'nl_bus',...%13
    'nl_cereal_s3',...%14
    'nl_juice_s3',...%15
    'nl_letter',...%16
    'nl_mugI_s3',...%17
    'nl_newspaper',...%18
    'paris_dynamic_lighting',...%19
    'phone',...%20
    'sunset_dynamic_lighting',...%21
    'sylvester',...%22
    'towel',...%23
    'wood_dynamic_lighting'%24
    };


challenges = {
    'angle',...%0
    'fast_close',...%1
    'fast_far',...%2
    'range',...%3
    'illumination'...%4
    };

tmt_idx_all=1:length(sequences_tmt);
tmt_idx_nl=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, 'nl_')));
tmt_idx_dl=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, 'dl_')));

tmt_idx_s1=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_s1')));
tmt_idx_s2=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_s2')));
tmt_idx_s3=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_s3')));
tmt_idx_s4=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_s4')));
tmt_idx_s5=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_s5')));
tmt_idx_si=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_si')));

tmt_idx_bookI=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_bookI')));
tmt_idx_bookII=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_bookII')));
tmt_idx_bookIII=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_bookIII')));
tmt_idx_cereal=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_cereal')));
tmt_idx_juice=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_juice')));
tmt_idx_mugI=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_mugI')));
tmt_idx_mugII=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_mugII')));
tmt_idx_mugIII=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_mugIII')));

tmt_idx_bus=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_bus')));
tmt_idx_highlighting=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_highlighting')));
tmt_idx_newspaper=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_newspaper')));
tmt_idx_letter=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, '_letter')));
tmt_idx_composite=[tmt_idx_bus tmt_idx_highlighting tmt_idx_newspaper tmt_idx_letter];
tmt_idx_robot=tmt_idx_all(~cellfun('isempty',strfind(sequences_tmt, 'robot_')));


tmt_idxs={
    tmt_idx_all,...
    tmt_idx_nl,...
    tmt_idx_dl,...
    tmt_idx_s1,...
    tmt_idx_s2,...
    tmt_idx_s3,...
    tmt_idx_s4,...
    tmt_idx_s5,...
    tmt_idx_si,...
    tmt_idx_bookI,...
    tmt_idx_bookII,...
    tmt_idx_bookIII,...
    tmt_idx_cereal,...
    tmt_idx_juice,...
    tmt_idx_mugI,...
    tmt_idx_mugII,...
    tmt_idx_mugIII,...
    tmt_idx_bus,...
    tmt_idx_highlighting,...
    tmt_idx_newspaper,...
    tmt_idx_letter,...
    tmt_idx_composite,...
    tmt_idx_robot
    };

tmt_idx_types={
    'all',...%0
    'nl',...%1
    'dl',...%2
    's1',...%3
    's2',...%4
    's3',...%5
    's4',...%6
    's5',...%7
    'si',...%8
    'bookI',...%9
    'bookII',...%10
    'bookIII',...%11
    'cereal',...%12
    'juice',...%13
    'mugI',...%14
    'mugII',...%15
    'mugIII',...%16
    'bus',...%17
    'highlighting',...%18
    'newspaper',...%19
    'letter',...%20
    'composite',...%21
    'robot'%22
    };

ucsb_idx_all=1:length(sequences_ucsb);
ucsb_idx_bricks=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, 'bricks_')));
ucsb_idx_building=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, 'building_')));
ucsb_idx_mission=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, 'mission_')));
ucsb_idx_sunset=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, 'sunset_')));
ucsb_idx_paris=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, 'paris_')));
ucsb_idx_wood=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, 'wood_')));

ucsb_idx_dynamic_lighting=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_dynamic_lighting')));
ucsb_idx_motion1=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion1')));
ucsb_idx_motion2=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion2')));
ucsb_idx_motion3=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion3')));
ucsb_idx_motion4=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion4')));
ucsb_idx_motion5=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion5')));
ucsb_idx_motion6=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion6')));
ucsb_idx_motion7=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion7')));
ucsb_idx_motion8=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion8')));
ucsb_idx_motion9=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_motion9')));
ucsb_idx_unconstrained=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_unconstrained')));
ucsb_idx_zoom=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_zoom')));
ucsb_idx_rotation=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_rotation')));
ucsb_idx_static_lighting=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_static_lighting')));
ucsb_idx_perspective=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_perspective')));
ucsb_idx_panning=ucsb_idx_all(~cellfun('isempty',strfind(sequences_ucsb, '_panning')));

ucsb_idxs={
    ucsb_idx_all,...
    ucsb_idx_bricks,...
    ucsb_idx_building,...
    ucsb_idx_mission,...
    ucsb_idx_sunset,...
    ucsb_idx_paris,...
    ucsb_idx_wood,...
    ucsb_idx_dynamic_lighting,...
    ucsb_idx_motion1,...
    ucsb_idx_motion2,...
    ucsb_idx_motion3,...
    ucsb_idx_motion4,...
    ucsb_idx_motion5,...
    ucsb_idx_motion6,...
    ucsb_idx_motion7,...
    ucsb_idx_motion8,...
    ucsb_idx_motion9,...
    ucsb_idx_unconstrained,...
    ucsb_idx_zoom,...
    ucsb_idx_rotation,...
    ucsb_idx_static_lighting,...
    ucsb_idx_perspective,...
    ucsb_idx_panning
    };

ucsb_idx_types={
    'all',...%0
    'bricks',...%1
    'building',...%2
    'mission',...%3
    'sunset',...%4
    'paris',...%5
    'wood',...%6
    'dynamic_lighting',...%7
    'motion1',...%8
    'motion2',...%9
    'motion3',...%10
    'motion4',...%11
    'motion5',...%12
    'motion6',...%13
    'motion7',...%14
    'motion8',...%15
    'motion9',...%16
    'unconstrained',...%17
    'zoom',...%18
    'rotation',...%19
    'static_lighting',...%20
    'perspective',...%21
    'panning'%22
    };

lintrack_idx_all=1:3;
lintrack_short_idx_all=1:14;

lintrack_idxs={
    lintrack_idx_all,...
    [1],...
    [2],...
    [3]
    };
lintrack_idx_types={
    'all',...%0
    'mouse_pad',...%1
    'phone',...%2
    'towel'%3
    };

sequences_lintrack_short = {
    'mouse_pad_1',...%0
    'mouse_pad_2',...%1
    'mouse_pad_3',...%2
    'mouse_pad_4',...%3
    'mouse_pad_5',...%4
    'mouse_pad_6',...%5
    'mouse_pad_7',...%6
    'phone_1',...%7
    'phone_2',...%8
    'phone_3',...%9
    'towel_1',...%10
    'towel_2',...%11
    'towel_3',...%12
    'towel_4'%13
    };
lintrack_short_idxs={
    lintrack_short_idx_all,...
    1:7,...
    8:10,...
    11:14
    };
lintrack_short_idx_types={
    'all',...%0
    'mouse_pad',...%1
    'phone',...%2
    'towel'%3
    };

tmt_fine_idx_all=1:24;
tmt_fine_idx_cam1=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, '_cam1')));
tmt_fine_idx_cam2=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, '_cam2')));
tmt_fine_idx_left=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, '_left')));
tmt_fine_idx_right=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, '_right')));
tmt_fine_idx_fast=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, '_fast')));
tmt_fine_idx_fish_lure=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'fish_lure')));
tmt_fine_idx_hexagon_task=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'hexagon_task')));
tmt_fine_idx_key_task=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'key_task')));
tmt_fine_idx_eth=[tmt_fine_idx_cam1 tmt_fine_idx_cam2];
tmt_fine_idx_eih=[tmt_fine_idx_left tmt_fine_idx_right];
tmt_fine_idx_fish_lure_fast_left=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'fish_lure_fast_left')));
tmt_fine_idx_fish_lure_left=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'fish_lure_left')));
tmt_fine_idx_hexagon_task_left=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'hexagon_task_left')));
tmt_fine_idx_key_task_left=tmt_fine_idx_all(~cellfun('isempty',strfind(sequences_tmt_fine, 'key_task_left')));

tmt_fine_idxs={
    tmt_fine_idx_all,...%0
    tmt_fine_idx_cam1,...%1
    tmt_fine_idx_cam2,...%2
    tmt_fine_idx_left,...%3
    tmt_fine_idx_right,...%4
    tmt_fine_idx_fast,...%5
    tmt_fine_idx_fish_lure,...%6
    tmt_fine_idx_hexagon_task,...%7
    tmt_fine_idx_key_task,...%8
    tmt_fine_idx_eth,...%9
    tmt_fine_idx_eih,...%10
    tmt_fine_idx_fish_lure_fast_left,...%11
    tmt_fine_idx_fish_lure_left,...%12
    tmt_fine_idx_hexagon_task_left,...%13
    tmt_fine_idx_key_task_left...%14
    
    };
tmt_fine_idx_types={
    'all',...%0
    'cam1',...%1
    'cam2',...%2
    'left',...%3
    'right',...%4
    'fast',...%5
    'fish_lure',...%6
    'hexagon_task',...%7
    'key_task',...%8
    'eye_to_hand',...%9
    'eye_in_hand',...%10
    'fish_lure_fast_left',...%11
    'fish_lure_left',...%12
    'hexagon_task_left',...%13
    'key_task_left',...%14    
    };

pami_idx_all=1:25;
cmt_idx_all=1:20;
metaio_idx_all=1:40;
vivid_idx_all=1:9;
vot_idx_all=1:25;
vot16_idx_all=1:length(sequences_vot16);
vtb_idx_all=1:100;
trakmark_idx_all=1:21;

pami_idxs={
    pami_idx_all
    };
pami_idx_types={
    'all'
    };
cmt_idxs={
    cmt_idx_all
    };
cmt_idx_types={
    'all'
    };
metaio_idxs={
    metaio_idx_all
    };
metaio_idx_types={
    'all'
    };
vivid_idxs={
    vivid_idx_all
    };
vivid_idx_types={
    'all'
    };
vot_idxs={
    vot_idx_all
    };
vot_idx_types={
    'all'
    };
vot16_idxs={
    vot16_idx_all
    };
vot16_idx_types={
    'all'
    };
vtb_idxs={
    vtb_idx_all
    };
vtb_idx_types={
    'all'
    };
trakmark_idxs={
    trakmark_idx_all
    };
trakmark_idx_types={
    'all'
    };

mosic_idx_all=1:length(sequences_mosaic);
misc_idx_all=1:length(sequences_misc);
synthetic_idx_all=1:length(sequences_synthetic);

mosaic_idxs={
    trakmark_idx_all
    };
mosaic_idx_types={
    'all'
    };
misc_idxs={
    misc_idx_all
    };
misc_idx_types={
    'all'
    };
synthetic_idxs={
    synthetic_idx_all
    };
synthetic_idx_types={
    'all'
    };
actor_idxs={
    tmt_idxs,...%0
    ucsb_idxs,...%1
    lintrack_idxs,...%2
    pami_idxs,...%3
    lintrack_short_idxs,...%4
    metaio_idxs,...%5
    cmt_idxs,...%6
    vot_idxs,...%7
    vot16_idxs,...%8
    vtb_idxs,...%9
    vivid_idxs,...%10
    trakmark_idxs,...%11
    tmt_fine_idxs,...%12
    mosaic_idxs,...%13
    misc_idxs,...%14
    synthetic_idxs%15    
    };
actor_idx_types={
    tmt_idx_types,...%0
    ucsb_idx_types,...%1
    lintrack_idx_types,...%2
    pami_idx_types,...%3
    lintrack_short_idx_types,...%4
    metaio_idx_types,...%5
    cmt_idx_types,...%6
    vot_idx_types,...%7
    vot16_idx_types,...%8
    vtb_idx_types,...%9
    vivid_idx_types,...%10
    trakmark_idx_types,...%11
    tmt_fine_idx_types,...%12
    mosaic_idx_types,...%13
    misc_idx_types,...%14
    synthetic_idx_types%15  
    };

sequences={
    sequences_tmt,...%0
    sequences_ucsb,...%1
    sequences_lintrack,...%2
    sequences_pami,...%3
    sequences_lintrack_short,...%4
    sequences_metaio,...%5
    sequences_cmt,...%6
    sequences_vot,...%7
    sequences_vot16,...%8
    sequences_vtb,...%9    
    sequences_vivid,...%10
    sequences_trakmark,...%11
    sequences_tmt_fine,...%12
    sequences_mosaic,...%13
    sequences_misc,...%14
    sequences_synthetic,...%16
    sequences_live%16
    };

actors = {
    'TMT',...%0
    'UCSB',...%1
    'LinTrack',...%2
    'PAMI',...%3
    'LinTrackShort',...%4
    'METAIO',...%5
    'CMT',...%6
    'VOT',...%7
    'VOT16',...%8
    'VTB',...%9
    'VIVID',...%10
    'TrakMark',...%11
    'TMT_FINE',...%12
    'Mosaic',...%13
    'Misc',...%14    
    'Synthetic',...%15
    'Live'%16
    };
