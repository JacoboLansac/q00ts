import numpy as np
import pandas as pd
import os
from os import path

destination = '/home/jl/projects/q00ts/metadata_q00unicorns/input/img'
origin = '/home/jl/projects/q00ts/metadata_q00unicorns/input/raw_traits/'

for root, dirs, files in os.walk(origin):

    if files:
        trait_class = root.split('/')[root.split('/').index('raw_traits') + 1]
        values = files

        dest_trait_folder = path.join(destination, trait_class)

        print(trait_class, root)

        os.makedirs(dest_trait_folder, exist_ok=True)

        command = f"cp {path.join(root, '*')} {dest_trait_folder}"
        print(command)
        # os.system(command)

