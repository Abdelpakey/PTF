if isnumeric(plot_data_desc{1}('value'))
    bars_per_group=length(plot_data_desc{1}('value'));
    labels=cell(n_lines, 1);
else
    bars_per_group = 2;
    labels=cell(n_lines, 1);
end
colors=plot_data_desc{1}('color');
values=zeros(n_lines, bars_per_group);
stats_col = 1;
for line_id=1:n_lines
    desc=plot_data_desc{line_id};
    curr_colors=desc('color');
    line_styles=desc('line_style');    
    if ~isnumeric(desc('value'))
        key_string = desc('value');
        if ~isempty(desc('stats_file_name'))
            stats_file_name=desc('stats_file_name');
        else
            stats_file_name = 'tracking_stats.txt';
        end        
        fprintf('Reading stats data for key %d: %s from %s\n',...
            line_id, key_string, stats_file_name);
        stats = importdata(stats_file_name);
        stats_col = 1;
        show_bar_legend_=show_bar_legend;
        if ~isempty(desc('stats_col'))
            show_bar_legend_=desc('stats_col');
%             stats_col=desc('stats_col');
%             fprintf('Getting data from mean of column %d\n', stats_col);            
        end     
        
        key_data=stats.data(~cellfun('isempty',strfind(stats.textdata(:, end),...
            key_string)), stats_col);
        key_data(isnan(key_data))=[];
        n_key_data=length(key_data);
        
        key_data_mean=mean(key_data);
        key_data_std=std(key_data);
        fprintf('key_data :: count: %d mean: %f std: %f\n',...
            n_key_data, key_data_mean, key_data_std);
        values(line_id, 1) = key_data_mean;
        values(line_id, 2) = key_data_std;
%         labels{2*line_id-1}=sprintf('%s/Mean', desc('label'));
%         labels{2*line_id}=sprintf('%s/Std', desc('label'));
        labels{line_id}=desc('label');
        if bar_with_legend
%             bar_x=[2*line_id-1, 2*line_id];
            line_id_avg=(line_id-1)*1.75 + 0.40;
            bar_ids(line_id) = bar(line_id_avg, values(line_id, 1),...
                'Parent', gca,...
                'BarWidth', bar_width,...
                'LineWidth', bar_line_width,...
                'LineStyle', line_styles{1},...
                'FaceColor', col_rgb{strcmp(col_names,curr_colors(1))},...
                'EdgeColor', col_rgb{strcmp(col_names,'black')});  
            bar(line_id_avg + 0.65, values(line_id, 2),...
                'Parent', gca,...
                'BarWidth', bar_width,...
                'LineWidth', bar_line_width,...
                'LineStyle', line_styles{2},...
                'FaceColor', col_rgb{strcmp(col_names,curr_colors(1))},...
                'EdgeColor', col_rgb{strcmp(col_names,'black')});
%             for bar_id=1:bars_per_group
%                 set(b(bar_id), 'LineStyle', line_styles{bar_id});
%                 set(b(bar_id), 'FaceColor', col_rgb{strcmp(col_names,curr_colors{bar_id})});
%                 set(b(bar_id), 'EdgeColor', col_rgb{strcmp(col_names,'black')});
%             end
        end
    else
        labels{line_id}=desc('label');
        values(line_id, :)=desc('value');
    end
    if annotate_bars
        for bar_id=1:bars_per_group
            if isempty(annotation_col)
                bar_annotation_col=col_rgb{strcmp(col_names,colors{bar_id})};
            else
                bar_annotation_col = annotation_col;
            end                                
            annotation('textbox',...
                [0 0 0.3 0.15],...
                'String',num2str(values(line_id, bar_id)),...
                'FontSize',20,...
                'FontWeight','bold',...
                'FontName','Times New Roman',...
                'LineStyle','-',...
                'EdgeColor','none',...
                'LineWidth',2,...
                'BackgroundColor','none',...
                'Color',bar_annotation_col,...
                'FitBoxToText','on');
        end
    end
end
if bar_with_legend
    if show_bar_legend_
        if col_legend
            h_legend=columnlegend(2,labels,'NorthWest', 'boxon');
        else
            h_legend=legend(bar_ids, labels);
        end
        set(h_legend,'FontSize',legend_font_size);
        set(h_legend,'FontWeight','bold');
    end
    set(gca, 'XAxisLocation', 'bottom');
    set(gca, 'YAxisLocation', 'left');
    set(gca, 'Color', 'None');
    x_lim=(n_lines-1)*1.75 + 1.40;
    set(gca, 'XLim', [0, x_lim]);
%     set(gca, 'XTick', 1:n_lines);
    set(gca, 'XTickLabel', []);
    set(gca,'box','off');
    ylabel('Speed in FPS');
else
    if horz_bar_plot
        b = barh(values);
        set(gca, 'YTick', 1:n_lines);
        set(gca, 'YTickLabel', labels, 'DefaultTextInterpreter', 'none');
        xlabel('MCD Error');
    else
        b=bar(values);
        set(gca, 'XTick', 1:n_lines);
        ylabel('MCD Error');
        set(gca, 'XTickLabel', labels, 'DefaultTextInterpreter', 'none');
    end                
    line_styles=plot_data_desc{1}('line_style');
    for bar_id=1:bars_per_group
        set(b(bar_id), 'LineStyle', line_styles{bar_id});
        set(b(bar_id), 'FaceColor', col_rgb{strcmp(col_names,colors{bar_id})});
        set(b(bar_id), 'EdgeColor', col_rgb{strcmp(col_names,'black')});
    end
end