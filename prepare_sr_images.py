from __future__ import print_function
import argparse
import glob
import os
import sys
import json
from natsort import natsorted
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", help='Training files containing annotations in Yolo format')
    parser.add_argument(
        "dataset", help='Json file containing annotations')
    parser.add_argument(
        "--sr_num", help='Number of SR images to be produced', default=2)
    parser.add_argument(
        "--seed", help='Random number seed', default=30)
    args = parser.parse_args()

    styles = ["antimonocromatismo",
              "asheville",
              "brushstrokes",
              "contrast_of_forms",
              "en_campo_gris",
              "flower_of_life",
              "goeritz",
              "impronte_d_artista",
              "la_muse",
              "mondrian",
              "mondrian_cropped",
              "picasso_seated_nude_hr",
              "picasso_self_portrait",
              "scene_de_rue",
              "sketch",
              "the_resevoir_at_poitiers",
              "trial",
              "woman_in_peasant_dress",
              "woman_in_peasant_dress_cropped",
              "woman_with_hat_matisse"]

    with open(args.path) as f:
        data = f.readlines()
        random.seed(30)
        image_ids = set()
        for line in data:
            fname = line.split('.')[0]
            sr_list = random.sample(styles, args.sr_num)
            for sr in sr_list:
                file = '%s_stylized_%s' % (fname, sr)
                image_ids.add(file)
        with open(args.dataset + '_SR_out.txt', 'w+') as f:
            f.write('\n'.join(natsorted(list(image_ids), key=lambda y: y.lower())))
