import cv2
import numpy as np
import time
import sys
# This is needed since the notebook is stored in the object_detection folder.

# ## Object detection imports
# Here are the imports from the object detection module.

from Misc import processArguments, sortKey
import os

params = {
    'labels_path': 'data/wildlife_label_map.pbtxt',
    # 'src_path': 'images/train',
    # 'det_path': 'data/train.csv',
    # 'save_path': 'images/train_vis',
    'src_path': 'images/test',
    'det_path': 'data/test.csv',
    'save_path': 'images/test_vis',
    'load_path': '',
    'n_classes': 7,
    'img_ext': 'jpg',
    'batch_size': 1,
    'show_img': 1,
    'save_fmt': 1,
    'n_frames': 0,
}

processArguments(sys.argv[1:], params)
src_path = params['src_path']
labels_path = params['labels_path']
det_path = params['det_path']
n_classes = params['n_classes']
save_path = params['save_path']
load_path = params['load_path']
img_ext = params['img_ext']
batch_size = params['batch_size']
show_img = params['show_img']
save_fmt = params['save_fmt']
n_frames = params['n_frames']

print('Reading source images from: {}'.format(src_path))

src_file_list = [k for k in os.listdir(src_path) if k.endswith('.{:s}'.format(img_ext))]
total_frames = len(src_file_list)
# print('file_list: {}'.format(file_list))
if total_frames <= 0:
    raise SystemError('No input frames found')
print('total_frames: {}'.format(total_frames))
src_file_list.sort(key=sortKey)

label_map = label_map_util.load_labelmap(labels_path)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=n_classes, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
class_dict = dict((v['name'], v['id']) for k, v in category_index.items())

print('categories: ', categories)
print('category_index: ', category_index)

df = pd.read_csv(det_path)

# Mapping name to id

# class_dict = {
#     'bear': 1,
#     'moose': 2,
#     'coyote': 3,
#     'deer': 4,
#     'horse': 5,
#     'cow': 6,
#     'elk': 7,
# }

video_out = None
if save_fmt == 1:
    print('Saving output images to {}'.format(save_path))
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
elif save_fmt == 2:
    save_dir = os.path.dirname(save_path)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    print('Saving output video to {}'.format(save_path))
    temp_img = cv2.imread(os.path.join(src_path, src_file_list[0]))
    height, width, _ = temp_img.shape
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    video_out = cv2.VideoWriter(save_path, fourcc, 20, (width, height))

frame_id = 0
pause_after_frame = 1
# Collect instances of objects and remove from df
while not df.empty:
    # Look for objects with similar filenames, group them, send them to csv_to_record function and remove from df
    multiple_instance = df.loc[df['filename'] == df.iloc[0].loc['filename']]
    # Total # of object instances in a file
    no_instances = len(multiple_instance.index)
    # Remove from df (avoids duplication)
    df = df.drop(multiple_instance.index[:no_instances])

    filename = multiple_instance.iloc[0].loc['filename']
    file_path = os.path.join(src_path, filename)
    if not os.path.exists(file_path):
        raise SystemError('Image file {} does not exist'.format(file_path))

    image = cv2.imread(file_path)

    width = float(multiple_instance.iloc[0].loc['width'])
    height = float(multiple_instance.iloc[0].loc['height'])

    classes_text = []
    classes = []
    boxes = []
    scores = []

    for instance in range(0, len(multiple_instance.index)):
        xmin = multiple_instance.iloc[instance].loc['xmin']
        ymin = multiple_instance.iloc[instance].loc['ymin']
        xmax = multiple_instance.iloc[instance].loc['xmax']
        ymax = multiple_instance.iloc[instance].loc['ymax']
        class_name = multiple_instance.iloc[instance].loc['class']
        class_id = class_dict[class_name]

        boxes.append([ymin, xmin, ymax, xmax])
        classes.append(class_id)
        scores.append(1)

    boxes = np.asarray(boxes, dtype=np.float32)
    classes = np.asarray(classes)
    scores = np.asarray(scores)

    # print('boxes', boxes)
    # print('scores', scores)
    # print('classes', classes)

    # print('boxes.shape', boxes.shape)
    # print('scores.shape', scores.shape)
    # print('classes.shape', classes.shape)

    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        boxes,
        classes.astype(np.int32),
        scores,
        # None,
        category_index,
        use_normalized_coordinates=False,
        line_thickness=4)

    if show_img:
        cv2.imshow('frame', image)
        k = cv2.waitKey(1 - pause_after_frame) & 0xFF
        if k == ord('q') or k == 27:
            break
        elif k == 32:
            pause_after_frame = 1 - pause_after_frame

    if save_fmt == 1:
        out_file_path = os.path.join(save_path, filename)
        cv2.imwrite(out_file_path, image)
    elif save_fmt == 2:
        video_out.write(image)

    frame_id += 1
    sys.stdout.write('\rDone {:d} frames '.format(frame_id))
    sys.stdout.flush()

    if n_frames > 0 and frame_id >= n_frames:
        break

sys.stdout.write('\n')
sys.stdout.flush()

if save_fmt == 2:
    video_out.release()

if show_img:
    cv2.destroyAllWindows()
