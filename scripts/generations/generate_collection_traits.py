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


def generate_random_token_traits(traits_configs: dict) -> dict:
    """Picks up randomly the traits for a new token taking into account the probabilities
    specified for each trait value"""
    token_traits = {}
    for trait_class, trait_values in traits_configs.items():
        probabilities = [prob / 100 for (value, prob) in trait_values.items()]
        norm_probs = [p / sum(probabilities) for p in probabilities]
        values = [value for (value, prob) in trait_values.items()]
        value = np.random.choice(values, p=norm_probs)
        token_traits.update({trait_class: value})
    return token_traits


def calculate_hash(token_traits: dict) -> int:
    """Hash is used to make sure an item is not repeated twice in the collection"""
    return hash(str(token_traits))


def random_generation_of_metadata(traits_configs: dict, total_supply: int) -> dict:
    """
    Randomly generates traits for all items in the collection,
    making sure that no item is repeated
    """
    print(f"\nGenerating traits for [{total_supply}] tokens")
    current_tokenid = 1
    existing_hashes = []
    collection_traits = {}

    while current_tokenid <= total_supply:
        token_traits = generate_random_token_traits(traits_configs)
        token_hash = calculate_hash(token_traits)

        if token_hash in existing_hashes:
            continue

        existing_hashes.append(token_hash)
        collection_traits.update({current_tokenid: token_traits})
        current_tokenid += 1

    print(f"Traits generation done")
    return collection_traits


def validate_generated_traits(collection_traits: dict, total_supply: int):
    """
    Performs two validation checks:
        there is no repeated tokens with same traits (groupby counting)
        requested total supply is met
    """
    df = pd.DataFrame.from_records(collection_traits).T
    assert df.value_counts().max() == 1, f"Repeated traits:\n{df.value_counts()}"
    assert total_supply == len(df), "Wrong total supply"
    print(f"Validation: done")


def save_stats(faction: str, collection_traits: dict):
    """ Dumps the statistics of how often each trait value of each trait class appears """
    df = pd.DataFrame.from_records(collection_traits).T
    total_supply = len(df)
    stats = {}
    for trait_class, trait_values in df.items():
        trait_probabilities = 100 * trait_values.value_counts() / total_supply
        stats.update({trait_class: trait_probabilities.to_dict()})

    traits_stats_path = path.join(utils.metadata_path(faction), 'output', 'traits_info',
                                  'stats.json')
    os.makedirs(path.dirname(traits_stats_path), exist_ok=True)
    json.dump(stats, open(traits_stats_path, 'w'), indent=2)
    print(f"Stats saved at: {traits_stats_path}")


def save_collection_traits(faction: str, collection_traits: dict, traits_configs: dict,
                           upgrade_order: list):
    """ Saves the traits in a json file for later generation of the images """
    generated_traits_path = path.join(utils.metadata_path(faction), 'output', 'traits_info',
                                      'collection_traits.json')
    os.makedirs(path.dirname(generated_traits_path), exist_ok=True)
    json.dump(collection_traits, open(generated_traits_path, 'w'), indent=2)
    print(f"Traits saved at: {generated_traits_path}")


def artificial_modifications(faction, collection_traits: dict) -> dict:
    if faction == 'q00nicorns':
        return collection_traits

    tokenid = 2758
    collection_traits[tokenid]['sky'] = 'flamed-eye'
    collection_traits[tokenid]['shoes'] = 'red-oStar'
    collection_traits[tokenid]['background'] = 'multicolor'
    collection_traits[tokenid]['ears'] = 'saiyan'
    collection_traits[tokenid]['head'] = 'dinosaur'
    collection_traits[tokenid]['skin'] = 'bengal-tiger'

    tokenid = 3904
    collection_traits[tokenid]['sky'] = 'rain'
    collection_traits[tokenid]['background'] = 'multicolor'
    collection_traits[tokenid]['skin'] = 'leopard'
    collection_traits[tokenid]['eyes'] = 'q00t-snake'
    collection_traits[tokenid]['mouth'] = 'vampire'
    collection_traits[tokenid]['companion'] = 'spider'

    tokenid = 1829
    collection_traits[tokenid]['sky'] = 'rain'
    collection_traits[tokenid]['skin'] = 'multicolor'
    collection_traits[tokenid]['background'] = 'bloody-dark'
    collection_traits[tokenid]['mouth'] = 'why-so-serious'
    collection_traits[tokenid]['eyes'] = 'q00t-eyelashes'
    collection_traits[tokenid]['companion'] = 'transparent-dog'

    tokenid = 4399
    collection_traits[tokenid]['sky'] = 'rocket'
    collection_traits[tokenid]['background'] = 'volcano'
    collection_traits[tokenid]['skin'] = 'bengal-tiger'
    collection_traits[tokenid]['flag'] = 'osnipe'
    collection_traits[tokenid]['head'] = 'dinosaur'
    collection_traits[tokenid]['mouth'] = 'pacifier-blue'
    collection_traits[tokenid]['companion'] = 'box'

    tokenid = 4755
    collection_traits[tokenid]['sky'] = 'shooting-star'
    collection_traits[tokenid]['background'] = 'volcano'
    collection_traits[tokenid]['skin'] = 'multicolor'
    collection_traits[tokenid]['eyes'] = 'q00t-cyclops'
    collection_traits[tokenid]['head'] = 'antelope-horns'

    return collection_traits


if __name__ == '__main__':
    faction = 'q00nicorns'
    # faction = 'q00tants'

    metadata_config = utils.load_metadata_configs(faction)
    traits_configs = metadata_config['traits']
    total_supply = metadata_config['total-supply']
    trait_overlapping_order = metadata_config['overlapping-order']
    upgrade_order = metadata_config['upgrade-order']
    img_size = metadata_config['img']['size']

    # Validate that there is enough traits to generate enough unique NFTs
    utils.check_max_number_unique_nfts(traits_configs, total_supply)

    # ===================================================================================
    collection_traits = random_generation_of_metadata(traits_configs, total_supply)
    # ===================================================================================
    collection_traits = artificial_modifications(faction, collection_traits)
    # ===================================================================================

    validate_generated_traits(collection_traits, total_supply)
    save_stats(faction, collection_traits)
    save_collection_traits(faction, collection_traits, traits_configs, upgrade_order)
