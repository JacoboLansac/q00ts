import argparse
import os

import numpy as np
from os import path

import config
from libs import utils

# Make sure every generation yields the same traits by fixing the random seed
np.random.seed(0)


def showcase(collection_traits):
    showcase_examples = {}

    counter = 1
    for trait_class, trait_values in collection_traits.items():
        print(f"Showcasing {trait_class}")

        showcase_examples[trait_class] = dict()

        setup_traits = {}
        # chose fixed setup from the other traits
        for _class, values in collection_traits.items():
            normprobs = [v / sum(values.values()) for v in values.values()]
            random_pick = np.random.choice(list(values.keys()), p=normprobs)
            setup_traits.update({_class: random_pick})

        # Showcase traits based on that fixed setup
        for trait_value in trait_values:
            example = setup_traits.copy()
            example.update({trait_class: trait_value})

            showcase_examples[trait_class][trait_value] = example.copy()
            # showcase_examples.update({counter: example})
            counter += 1

    return showcase_examples


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images', action='store_true',
                        help='If flagged, images are generated, if not, only metadata files')
    args = parser.parse_args()

    metadata_config = utils.load_metadata_configs()
    traits_configs = metadata_config['traits']
    trait_order = metadata_config['overlapping-order']
    img_size = metadata_config['img']['size']

    # Validate that all traits probabilities add up to 100%
    # utils.check_trait_probabilities(traits_configs)

    # ===================================================================================
    traits_showcase = showcase(traits_configs)
    # ===================================================================================

    utils.verify_trait_images_exists(traits_configs)

    for trait_class, trait_showcase in traits_showcase.items():
        print(trait_class, trait_showcase)

        for trait_value, token_traits in trait_showcase.items():

            image_path = path.join(config.project_path, 'metadata', 'traits_showcase', trait_class, trait_value)
            os.makedirs(path.dirname(image_path), exist_ok=True)

            image = utils.generate_image(token_traits, trait_order, img_size)
            image.save(image_path, format='png')
            print(f"saved: {image_path}")
