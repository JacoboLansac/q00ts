import argparse
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


def save_individual_token_traits(faction: str, collection_traits: dict, traits_configs: dict,
                          upgrade_order: list, max_level=None):

    ignore_traits_in_metadata_file = utils.get_single_traits(traits_configs)

    for tokenid, token_traits in collection_traits.items():

        for level in range(1, len(upgrade_order) + 1):
            if (max_level is not None) and (level > max_level):
                continue

            unlocked_classes = upgrade_order[:level]

            token_metadata_to_save = {}
            for class_, value_ in token_traits.items():
                if class_ in ignore_traits_in_metadata_file:
                    continue
                if class_ in unlocked_classes:
                    tvalue = collection_traits[tokenid][class_]
                else:
                    tvalue = 'locked'
                token_metadata_to_save.update({class_: tvalue})

            token_metadata_to_save.update({"faction": faction})

            token_path = path.join(utils.metadata_path(faction), 'output', 'json',
                                   f"{level}_upgrades", str(tokenid))
            os.makedirs(path.dirname(token_path), exist_ok=True)
            json.dump(token_metadata_to_save, open(token_path, 'w'), indent=2)


if __name__ == '__main__':
    # faction = 'q00nicorns'
    faction = 'q00tants'

    metadata_config = utils.load_metadata_configs(faction)
    traits_configs = metadata_config['traits']
    upgrade_order = metadata_config['upgrade-order']

    # ===================================================================================
    collection_traits = json.load(open(path.join(
        utils.metadata_path(faction), 'output', 'traits_info', 'collection_traits.json'), 'r'))
    # ===================================================================================

    save_individual_token_traits(faction,
                                 collection_traits,
                                 traits_configs,
                                 upgrade_order,
                                 max_level=2)
