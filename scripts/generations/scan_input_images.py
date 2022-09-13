import numpy as np
import pandas as pd
import os
from os import path
import config


def scan_images():
    """
    Scans and prints it so that it is easy to copy paste into the metadata-config.yaml
    :return:
    """
    input_img_path = path.join(config.project_path, 'metadata', 'input', 'img')

    print(f"traits:")

    for root, dir, files in os.walk(input_img_path):

        if files:
            trait_class = path.basename(root)
            trait_values = [value.split('.')[0] for value in files]
            values_without_basic = [value for value in trait_values if 'basic' not in value]

            print(f"\t{trait_class}:")
            for value in trait_values:
                if ('basic' in value) and (len(trait_values) == 1):
                    print(f"\t\t{value}: 100")
                if 'basic' not in value:
                    print(f"\t\t{value}: {round(100 * 1/(len(values_without_basic)), 2)}")


if __name__ == '__main__':
    scan_images()
