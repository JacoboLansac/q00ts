import os
import json
from os import path
import config
from PIL import Image
import yaml


def load_metadata_configs(faction: str) -> dict:
    config_file_path = path.join(config.project_path, f'metadata-config-{faction}.yaml')
    return yaml.safe_load(open(config_file_path, 'r'))


def metadata_path(faction: str):
    return path.join(config.project_path, 'metadata', faction)


def trait_value_path(trait_class: str, trait_value_fname: str, faction:str) -> str:
    input_img_path = path.join(metadata_path(faction), 'input', 'img')
    if not trait_value_fname.endswith('.png'):
        trait_value_fname = trait_value_fname + '.png'
    return path.join(input_img_path, trait_class, trait_value_fname)


def check_max_number_unique_nfts(traits: dict, total_supply: int):
    """From a traits dict calculates the max number of unique NFTs that can be generated"""
    n = 1
    for trait_class, trait_values in traits.items():
        n *= len(trait_values)

    assert total_supply <= n, f"max unique NFTS: {n}. Requested total_supply: {total_supply}"
    print(f"Max unique NFTS: {n}")


def check_trait_probabilities(traits: dict):
    """Makes sure probabilities add up to 100 for each trait class"""
    for trait_class, trait_values in traits.items():
        sum_of_probabilities = sum([value for trait, value in trait_values.items()])
        assert abs(
            sum_of_probabilities - 100 < .1), f"trait probabilities should sum should be 100: sum({trait_class}) = {sum_of_probabilities}"


def verify_trait_images_exists(faction: str, traits_configs: dict):

    # This will be None if no translation file is found
    filenames_dict = load_filename_translations(faction)

    not_founds = []
    total = 0
    for trait_class, trait_values in traits_configs.items():
        for trait_value in trait_values:
            total += 1
            if filenames_dict is not None:
                value_filename = filenames_dict[trait_class][trait_value]
            else:
                value_filename = trait_value
            value_path = trait_value_path(trait_class, value_filename, faction)

            if not path.isfile(value_path):
                not_founds.append(value_path)

    if not_founds:
        raise FileNotFoundError(f"{len(not_founds)}/{total} not found:" + '\n'.join(not_founds))


def get_single_traits(traits_configs: dict) -> list:
    return [trait for trait, values in traits_configs.items() if len(values) == 1]


def generate_image(faction:str, token_traits: dict, trait_order: list, img_size: tuple) -> Image:
    """Generates an image overlapping the traits"""

    remaining = list(token_traits.keys())

    translations = load_filename_translations(faction)

    canvas = Image.new("RGBA", img_size)
    for trait_class in trait_order:
        remaining.pop(remaining.index(trait_class))
        trait_value = token_traits[trait_class]
        if trait_value is None:
            continue

        if translations is not None:
            if 'basic' in trait_value:
                value_filename = 'basic.png'
            else:
                value_filename = translations[trait_class][trait_value]
        else:
            value_filename = trait_value

        trait_img_path = trait_value_path(trait_class, value_filename, faction)
        new_layer = Image.open(trait_img_path).resize(img_size).convert('RGBA')
        canvas.alpha_composite(new_layer)

    if remaining:
        raise ValueError(f"unused trait class: {remaining}")

    return canvas


def hide_traits(token_traits: dict, unlocked_classes: list, faction:str):
    current_token_traits = {}
    for class_, value_ in token_traits.items():
        if class_ in unlocked_classes:
            tvalue = value_
        else:
            # Search for basic png
            if not path.exists(trait_value_path(class_, 'basic', faction)):
                tvalue = None
            else:
                tvalue = 'basic'

        current_token_traits.update({class_: tvalue})
    return current_token_traits.copy()

def load_filename_translations(faction:str):
    if faction == 'q00nicorns':
        return json.load(open(path.join(metadata_path(faction), 'input','filenames.json'), 'r'))
    else:
        return None