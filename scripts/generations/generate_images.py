import argparse
import time
import os
import re
import pandas as pd
import numpy as np
import yaml
from os import path
import json
import config
from PIL import Image
from libs import utils

# Make sure every generation yields the same traits by fixing the random seed
np.random.seed(0)


def verify_trait_images_exists(traits_configs: dict):
    not_founds = []
    for trait_class, trait_values in traits_configs.items():
        for trait_value in trait_values:
            value_path = utils.trait_value_path(trait_class, trait_value)
            if not path.isfile(value_path):
                not_founds.append(value_path)

    if not_founds:
        raise FileNotFoundError(f"{not_founds}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images', action='store_true',
                        help='If flagged, images are generated, if not, only metadata files')
    args = parser.parse_args()

    faction = 'q00tants'

    allowed_levels = [0, 10]

    metadata_config = utils.load_metadata_configs(faction)
    traits_configs = metadata_config['traits']
    total_supply = metadata_config['total-supply']
    trait_order = metadata_config['overlapping-order']
    upgrade_order = metadata_config['upgrade-order']
    img_size = metadata_config['img']['size']

    verify_trait_images_exists(traits_configs)

    collection_traits = json.load(open(
        path.join(config.project_path, 'metadata', 'output', 'traits_info',
                  'collection_traits.json'), 'r'))
    print(f"Generating images for {len(collection_traits)} tokenids, {len(allowed_levels)} levels")

    ntokens = len(collection_traits)

    for level, trait_class in enumerate(upgrade_order):

        level_time = time.time()

        if (level not in allowed_levels):
            print(f"Skipping level {level}")
            continue

        print(f"{level}upgrades, new_trait: {trait_class}")
        unlocked_traits = upgrade_order[:level + 1]

        output_path = path.join(config.project_path, 'metadata', 'output', 'img', f"{level}_upgrades")
        os.makedirs(output_path, exist_ok=True)

        for tokenid, token_traits in collection_traits.items():
            # Remove items for the image or use the basic image
            upgraded_traits = utils.hide_traits(token_traits, unlocked_traits)

            image = utils.generate_image(upgraded_traits, trait_order, img_size)

            image_path = path.join(output_path, str(tokenid))
            image.save(image_path, format='png')
            print(f"saved: {image_path}")

            avg_time = (time.time() - level_time) / (int(tokenid) + 1)
            print(f"Estimated time left: {round((avg_time * ntokens - int(tokenid) - 1) / 3600, 2)} hours")
