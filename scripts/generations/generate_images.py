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


if __name__ == '__main__':

    faction = 'q00nicorns'

    allowed_levels = [1, 2, 3]

    metadata_config = utils.load_metadata_configs(faction)
    traits_configs = metadata_config['traits']
    total_supply = metadata_config['total-supply']
    trait_order = metadata_config['overlapping-order']
    upgrade_order = metadata_config['upgrade-order']
    img_size = metadata_config['img']['size']

    utils.verify_trait_images_exists(faction, traits_configs)

    collection_traits = json.load(open(
        path.join(utils.metadata_path(faction), 'output', 'traits_info',
                  'collection_traits.json'), 'r'))
    print(f"Generating images for {len(collection_traits)} tokenids, {len(allowed_levels)} levels")

    ntokens = len(collection_traits)

    traitsdf = pd.DataFrame.from_dict(collection_traits, orient='index')

    for level in range(1, len(upgrade_order) + 1):

        level_time = time.time()

        if (level not in allowed_levels):
            print(f"Skipping level {level}")
            continue

        print(f"{level}upgrades")

        unlocked_traits = upgrade_order[:level]

        output_path = path.join(utils.metadata_path(faction), 'output', 'img', f"{level}_upgrades")
        os.makedirs(output_path, exist_ok=True)

        for tokenid, token_traits in collection_traits.items():
            # Remove items for the image or use the basic image
            upgraded_traits = utils.hide_traits(token_traits, unlocked_traits, faction)

            image = utils.generate_image(faction, upgraded_traits, trait_order, img_size)

            image_path = path.join(output_path, str(tokenid))
            image.save(image_path, format='png')
            print(f"saved: {image_path}")

            avg_time = (time.time() - level_time) / (int(tokenid) + 1)
            print(f"Estimated time left: {round((avg_time * (ntokens - int(tokenid) - 1)) / 3600, 2)} hours")
