import json

import numpy as np
import pandas as pd
import os
from os import path
import config
import glob

# TODO This logic should be included in the generate.py script

unlocked_traits = ['mouth']
level = 0

# outputpath = f'/home/jl/projects/q00ts/metadata/output/json/{level}upgrades'
outputpath = f'/home/jl/projects/q00ts/metadata/output/run_20220910-113917336538/json/{level}_upgrades'
os.makedirs(outputpath, exist_ok=True)

traits_files = sorted(glob.glob("/home/jl/projects/q00ts/metadata/output/run_20220910-113917336538/json/fullyUpgraded/*"))

nfiles = 0
for trait_file in traits_files:
    if 'json' in path.basename(trait_file):
        continue

    nfiles += 1
    tokenid = path.basename(trait_file)
    token_traits = json.load(open(trait_file, 'r'))

    level_traits = {}
    for tclass, tvalue in token_traits.items():
        if tclass in unlocked_traits:
            level_traits.update({tclass: tvalue})
        else:
            level_traits.update({tclass: 'locked'})

    save_token_traits = path.join(outputpath, tokenid)
    json.dump(level_traits, open(save_token_traits, 'w'), indent=2)

    print(f"saved:{save_token_traits}")

print(f"Updated: {nfiles} files")