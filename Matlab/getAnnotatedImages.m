function [img_mat] = getAnnotatedImages(img_fname, no_of_frames)
fprintf('Reading and annotating images...');
% shapeInserter = vision.ShapeInserter('Shape', 'Lines');
img_mat=cell(no_of_frames, 1);

img_fid=fopen(img_fname);
img_width=fread(img_fid, 1, 'uint32', 'a');
img_height=fread(img_fid, 1, 'uint32', 'a');
% figure;
for frame_id=1:no_of_frames  
    %fprintf('frame_id: %d\n', frame_id);
    img_bin=fread(img_fid, [img_width img_height], 'uint8', 'a');
%     x=tracker_corners(frame_id+1, [1, 3, 5, 7]);
%     y=tracker_corners(frame_id+1, [2, 4, 6, 8]);
%     lines = int32([[x(1) y(1) x(2) y(2)];
%         [x(2) y(2) x(3) y(3)];
%         [x(3) y(3) x(4) y(4)];
%         [x(4) y(4) x(1) y(1)]]);
%     img_bin_annotated = step(shapeInserter, img_bin, lines); 
    img_mat{frame_id}=uint8(img_bin');
%     imshow(img_bin_annotated);
%     pause(0.01);
end
fclose(img_fid);
fprintf('Done\n');
end

