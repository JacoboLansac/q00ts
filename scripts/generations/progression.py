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

    tokenids = [2927, 1744, 3218, 2440, 4911]
    tokenids = [str(t) for t in tokenids]

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

    for tokenid in tokenids:
        token_traits = collection_traits[tokenid]

        for l in range(len(trait_order)):
            level = l + 1
            unlocked_traits = upgrade_order[:level]
            upgraded_traits = utils.hide_traits(token_traits, unlocked_traits, faction)

            image = utils.generate_image(faction, upgraded_traits, trait_order, img_size)

            output_path = path.join(utils.metadata_path(faction), 'trait_evolution', str(tokenid))
            os.makedirs(output_path, exist_ok=True)

            image_path = path.join(output_path, f"{level}_upgrades")
            image.save(image_path, format='png')
            print(f"saved: {image_path}")
