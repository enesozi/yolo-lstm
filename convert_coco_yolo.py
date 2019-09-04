from __future__ import print_function
import argparse
import glob
import os
import sys
import json
from natsort import natsorted

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", help='Json file containing annotations')
    parser.add_argument(
        "dataset", help='Json file containing annotations')
    parser.add_argument(
        "output_path", help='Output directory for image.txt files')
    args = parser.parse_args()

    with open(args.path) as f:
        data = json.load(f)
        annotations = data['annotations']
        width = 1920
        height = 1208
	if 'rescue' in args.dataset:
		height = 1088
        image_ids = set()
        anns_converted = {}
	cats = {0:0,1:0,2:0,3:0}
        for ann in annotations:
            if not os.path.exists('/home/Downloads/%s/%s'%(args.dataset,ann['image_id'])):
                continue
            cat_id = int(ann['category_id'])
	    if cat_id == 19:
	    	cat_id = 4
	    #if cat_id > 1:
	    #	continue
            left, top, bbox_width, bbox_height = map(
                float, ann['bbox'])
	    cats[cat_id-1] += 1
            # Yolo classes are starting from zero index
            cat_id -= 1
	    #if cat_id == 2:
            #	cat_id -= 1
            x_center, y_center = (
                left + bbox_width / 2, top + bbox_height / 2)
            # darknet expects relative values wrt image width&height
            x_rel, y_rel = (x_center / width, y_center / height)
            w_rel, h_rel = (bbox_width / width, bbox_height / height)

            file_name = "%s_%s.txt" % (
                args.dataset, ann['image_id'].split('.')[0])
            image_id = ann['image_id']
            image_ids.add(image_id)
            if image_id not in anns_converted:
                anns_converted[image_id] = {}
                anns_converted[image_id]['file'] = file_name
                anns_converted[image_id]['anns'] = []

            anns_converted[image_id]['anns'].append(
                (cat_id, x_rel, y_rel, w_rel, h_rel))
	print(len(image_ids))
        for image_id in anns_converted:
            file_name = anns_converted[image_id]['file']
            converted_results = anns_converted[image_id]['anns']
            with open(os.path.join(args.output_path, file_name), 'w+') as fp:
                fp.write('\n'.join('%d %.6f %.6f %.6f %.6f' %
                                   res for res in converted_results))
        with open(args.dataset + '.txt', 'w+') as f:
            f.write('\n'.join(natsorted(list(image_ids), key=lambda y: y.lower())))

	print(cats)
