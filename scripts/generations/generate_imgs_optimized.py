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


def image_generation_in_groups():
    for group, (_, traits) in enumerate(unique_items.iterrows()):
        _hashstr = traits.astype(str).sum()
        group_tokenids = leveltratisdf.loc[hashstrings == _hashstr].index.to_list()

        token_traits = collection_traits[group_tokenids[0]]

        upgraded_traits = utils.hide_traits(token_traits, unlocked_traits, faction)
        image = utils.generate_image(faction, upgraded_traits, trait_order, img_size)

        reference_path = None
        for tokenid in group_tokenids:
            image_path = path.join(output_path, str(tokenid))

            if reference_path is None:
                image.save(image_path, format='png')
                print(f"saved: {image_path}")
            else:
                os.system(f'cp {reference_path} {image_path}')
                print(f"[{faction}, level {level}, img-group {group}/{ngroups}] "
                      f"Copied: {path.basename(reference_path)} to {path.basename(image_path)}")

            reference_path = image_path


def image_generation_one_by_one():
    for tokenid, token_traits in collection_traits.items():
        # Remove items for the image or use the basic image
        upgraded_traits = utils.hide_traits(token_traits, unlocked_traits, faction)

        image = utils.generate_image(faction, upgraded_traits, trait_order, img_size)

        image_path = path.join(output_path, str(tokenid))
        image.save(image_path, format='png')
        print(f"[{faction}, level {level}: {path.basename(image_path)}")

        avg_time = (time.time() - level_time) / (int(tokenid))
        print(
            f"Estimated time left: {round((avg_time * ntokens - int(tokenid)) / 3600, 2)} hours")


if __name__ == '__main__':

    # faction = 'q00nicorns'
    faction = 'q00tants'

    allowed_levels = [2]

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

        if not ((level in allowed_levels) or ((-1 in allowed_levels) and (level == len(upgrade_order)))):
            print(f"Skipping level {level}")
            continue

        unlocked_traits = upgrade_order[:level]
        print(f"level: {level}. unlocked_traits: {unlocked_traits}")

        leveltratisdf = traitsdf.copy()
        for _class in traitsdf.columns:
            if _class not in unlocked_traits:
                leveltratisdf[_class] = 'locked'
        leveltratisdf.index.name = 'index'
        cols = list(leveltratisdf.columns)

        unique_items = leveltratisdf.reset_index().groupby(
            cols).count().reset_index().set_index('index')
        hashstrings = leveltratisdf.astype(str).sum(axis=1)

        output_path = path.join(utils.metadata_path(faction), 'output', 'img', f"{level}_upgrades")
        os.makedirs(output_path, exist_ok=True)

        ngroups = len(unique_items)

        if ngroups < 500:
            image_generation_in_groups()
        else:
            image_generation_one_by_one()


