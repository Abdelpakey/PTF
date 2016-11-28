import os
import sys
import cv2
import numpy as np


def readTrackingData(filename):
    if not os.path.isfile(filename):
        print "Tracking data file not found:\n ", filename
        sys.exit()

    data_file = open(filename, 'r')
    lines = data_file.readlines()
    no_of_lines = len(lines)
    data_array = np.empty([no_of_lines, 8])
    line_id = 0
    for line in lines:
        # print(line)
        words = line.split()
        if len(words) != 8:
            msg = "Invalid formatting on line %d" % line_id + " in file %s" % filename + ":\n%s" % line
            raise SyntaxError(msg)
        coordinates = []
        for word in words:
            coordinates.append(float(word))
        data_array[line_id, :] = coordinates
        # print words
        line_id += 1
    data_file.close()
    return data_array


def draw_region(img, corners, color, thickness=1):
    for i in xrange(4):
        p1 = (int(corners[0, i]), int(corners[1, i]))
        p2 = (int(corners[0, (i + 1) % 4]), int(corners[1, (i + 1) % 4]))
        cv2.line(img, p1, p2, color, thickness)


if __name__ == '__main__':
    dataset = 'nl_bus'
    ground_truth_file = dataset + '.txt'
    ground_truth = readTrackingData(ground_truth_file)


    for i in xrange(no_of_frames):
        ret, src_img = cap.read()
        if not ret:
            print "Frame ", i, " could not be read"
            break
        actual_corners = [ground_truth[i, 0:2].tolist(),
                          ground_truth[i, 2:4].tolist(),
                          ground_truth[i, 4:6].tolist(),
                          ground_truth[i, 6:8].tolist()]
        actual_corners = np.array(actual_corners).T
        curr_error = math.sqrt(np.sum(np.square(actual_corners - current_corners)) / 4)