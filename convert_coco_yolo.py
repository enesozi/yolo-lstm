from __future__ import print_function
# best model until now
import argparse
import glob
import os
import sys
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", help='Json file containing annotations')
    parser.add_argument(
        "output_path", help='Output directory for image.txt files')
    args = parser.parse_args()

    with open(json_file) as f:
        data = json.load(f)
        annotations = data['annotations']
        width = 1920
        height = 1208
        converted_results = []
        for ann in annotations:
            cat_id = int(ann['category_id'])
            left, top, bbox_width, bbox_height = map(
                float, ann['bbox'])

            # Yolo classes are starting from zero index
            cat_id -= 1
            x_center, y_center = (
                left + bbox_width / 2, top + bbox_height / 2)
            # darknet expects relative values wrt image width&height
            x_rel, y_rel = (x_center / width, y_center / height)
            w_rel, h_rel = (bbox_width / width, bbox_height / height)
            converted_results.append(
                (cat_id, x_rel, y_rel, w_rel, h_rel))
        with open(os.path.join(args.output_path, ann['image_id'].split('.')[0] + '.txt'), 'w+') as fp:
            fp.write('\n'.join('%d %.6f %.6f %.6f %.6f' %
                               res for res in converted_results))
