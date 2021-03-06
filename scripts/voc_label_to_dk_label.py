import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import pdb

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(workingdir,year, image_id):
    in_file = open('%s/VOCdevkit/VOC%s/Annotations/%s.xml'%(workingdir, year, image_id))
    out_file = open('%s/VOCdevkit/VOC%s/dk_labels/%s.txt'%(workingdir, year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# VOC data abs dir
wd = '/mnt/nas/tanfulun/Data/pascal_voc'

for year, image_set in sets:

    dk_label_abs_dir = os.path.join(wd,'VOCdevkit/VOC%s/dk_labels/'%(year))
    if not os.path.exists(dk_label_abs_dir):
        os.makedirs(dk_label_abs_dir)

    # get image names
    image_ids_abs_path = os.path.join(wd,'VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set))
    image_ids = open(image_ids_abs_path).read().strip().split()

    # store image abs path
    list_file_path = os.path.join(wd,'%s_%s.txt'%(year, image_set))
    list_file = open(list_file_path, 'w')

    for image_id in image_ids:
	print 'VOC%s_%s_%s'%(year, image_set, image_id)

        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
        convert_annotation(wd, year, image_id)
    list_file.close()
    #pdb.set_trace()

#os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > %s/train.txt")
#os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")

