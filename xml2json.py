import xml.etree.ElementTree as ET
import json
from os import listdir
from os.path import isfile, join
import sys

json_filename = '%s.json'%sys.argv[1]
xml_folder = sys.argv[2]
image_path = sys.argv[3]
file_ext = 'jpg'

def xyxy_to_xywh(coords):
    x, y = coords[0], coords[1]
    w, h = coords[2] - x, coords[3] - y
    return [x, y, w, h]

counter = 1
xmlCat_to_cocoCat = {'human' : 1, 'cyclist' : 2, 'car' : 3,}


def xml2json(xml_root, json_dict):
    global counter
    images = []
    annotations = []
    for child in xml_root:
        if child.tag == 'image':
            image_dict = {}
            image_dict['id'] = child.attrib['name'].split('/')[2]
            image_dict['file_name'] = child.attrib['name'].split('/')[2]
            images.append(image_dict)
            for box in child:
                bbox_dict = {}
                ### Change this
                bbox_dict['image_id'] = child.attrib['name'].split('/')[2]
                ###
                xyxy = [int(round(float(box.attrib[x]))) for x in ['xtl', 'ytl', 'xbr', 'ybr']]
                bbox_dict['bbox'] = xyxy_to_xywh(xyxy)
                bbox_dict['area'] = bbox_dict['bbox'][2] * bbox_dict['bbox'][3] 
                bbox_dict['occluded'] = box.attrib['occluded']
                bbox_dict['category_id'] = xmlCat_to_cocoCat[box.attrib['label']]
                bbox_dict['id'] = counter
                bbox_dict['iscrowd'] = 0
                counter += 1
                annotations.append(bbox_dict)
    categories = []
    categories.append({'supercategory' : 'Person', 'id' : 1, 'name' : 'Person'})
    categories.append({'supercategory' : 'Car', 'id' : 3, 'name' : 'Car'})
    if json_dict == {}:
        json_dict['annotations'] = annotations
        json_dict['categories'] = categories
    else:
        json_dict['annotations'] += annotations


xmlfiles = sorted([join(xml_folder, f) for f in listdir(xml_folder) if isfile(join(xml_folder, f)) and f.split('.')[-1] == 'xml'])

json_dict = {}
for xmlfile in xmlfiles:
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    xml2json(root, json_dict)

json_dict['images'] = [{'id' : f, 'file_name' : f} for f in listdir(image_path) if isfile(join(image_path, f)) and f.split('.')[-1] == 'jpg']

with open(json_filename, 'w+') as out:
    json.dump(json_dict, out)

