plot_synthetic_sr = 1;
n_syn_ssm_sigma_ids = length(syn_ssm_sigma_ids);
line_data{line_id}=zeros(n_syn_ssm_sigma_ids, 1);
line_data_idx = 1;
for syn_ssm_sigma_id = syn_ssm_sigma_ids
    if ~isempty(file_name)
        syn_data_fname=sprintf('%s_%s_%s', data_fname, syn_out_suffix, file_name);
        if ~isempty(desc('mtf_sm'))
            syn_add_noise = st2double(desc('mtf_sm'));
            if isempty(syn_add_noise)
                error('Invalid value specified for boolean syn_add_noise');
            else
                syn_add_noise = logical(syn_add_noise);
            end
        if ~isempty(desc('mtf_am'))
            syn_ilm = desc('mtf_am');
        end
        if ~isempty(desc('mtf_ssm'))
            syn_am_sigma_id = desc('mtf_ssm');
            if isempty(syn_am_sigma_id)
                error('Invalid value specified for integral syn_am_sigma_id');
            else
                syn_am_sigma_id = uint32(syn_am_sigma_id);
            end
        end
    else
        syn_data_fname=sprintf('%s_%s_%s_%s_%s_%d', data_fname, syn_out_suffix,...
            desc('mtf_sm'), desc('mtf_am'), desc('mtf_ssm'), desc('iiw'));
    end
    syn_out_suffix = sprintf('warped_%s_s%d',syn_ssm, syn_ssm_sigma_id);
    if ~strcmp(syn_ilm, '0')
        syn_out_suffix = sprintf('%s_%s_s%d',syn_out_suffix, syn_ilm, syn_am_sigma_id);
    end
    if syn_add_noise
        syn_out_suffix = sprintf('%s_gauss_%4.2f_%4.2f',...
            syn_out_suffix, syn_noise_mean, syn_noise_sigma);
    end
    if read_from_bin
        syn_data_fname=sprintf('%s.bin', syn_data_fname);
    else
        syn_data_fname=sprintf('%s.txt', syn_data_fname);
    end
    fprintf('Reading synthetic SR data for plot line %d SSM sigma ID %d from: %s\n',...
        line_id, syn_ssm_sigma_id, syn_data_fname);
    if read_from_bin
        data_fid=fopen(syn_data_fname);
        data_rows=fread(data_fid, 1, 'uint32', 'a');
        data_cols=fread(data_fid, 1, 'uint32', 'a');
        actor_data_sr=fread(data_fid, [data_cols, data_rows], 'float64', 'a');
        actor_data_sr = actor_data_sr';
        fclose(data_fid);
    else
        actor_data_sr=importdata(syn_data_fname);
    end
    avg_err=actor_data_sr(end, :);
    actor_data_sr(end, :) = [];   
    err_thr=actor_data_sr(:, 1);
    combined_sr=actor_data_sr(:, end);
    if syn_plot_type==0
        idx = find(err_thr>=syn_err_thresh,1);
        line_data{line_id}(line_data_idx)=combined_sr(idx);
    else
        line_data{line_id}(line_data_idx)=avg_err(end);
    end
    line_data_idx = line_data_idx + 1;
end
