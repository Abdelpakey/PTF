import xml.etree.cElementTree as ET
from Misc import getParamDict

root_dir = 'C:/Datasets'
actor_id = 4
seq_id = 0

params=getParamDict()
actors = params['mot_actors']
sequences = params['mot_sequences']
actor = actors[actor_id]
seq_name = sequences[actor][seq_id]
out_fname = '{:s}/{:s}/Annotations/{:s}.txt'.format(root_dir, actor, seq_name)
out_fid = open(out_fname, 'w')
fname = '{:s}/{:s}/Annotations/{:s}.xml'.format(root_dir, actor, seq_name)
tree = ET.parse(fname)
root = tree.getroot()
for frame_obj in tree.iter('frame'):
    tsrget_list = frame_obj.find('target_list')
    frame_id = int(frame_obj.attrib['num'])
    for obj in tsrget_list.iter('target'):
        bndbox = obj.find('box')
        obj_id = int(obj.attrib['id'])
        xmin = float(bndbox.attrib['left'])
        ymin = float(bndbox.attrib['top'])
        width = float(bndbox.attrib['width'])
        height = float(bndbox.attrib['height'])
        out_fid.write('{:d},{:d},{:f},{:f},{:f},{:f},1,-1,-1,-1\n'.format(
            frame_id + 1, obj_id, xmin, ymin, width, height))
    if (frame_id + 1) % 100 == 0:
        print 'Done {:d} frames'.format(frame_id + 1)
out_fid.close()
