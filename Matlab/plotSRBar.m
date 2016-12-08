labels=cell(n_lines, 1);
bars_per_group=length(plot_data_desc{1}('value'));
colors=plot_data_desc{1}('color');
values=zeros(n_lines, bars_per_group);
for line_id=1:n_lines
    desc=plot_data_desc{line_id};
    labels{line_id}=desc('label');
    values(line_id, :)=desc('value');
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