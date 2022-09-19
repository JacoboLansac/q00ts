import numpy as np
import yaml
import pandas as pd
import os
from os import path
import json

translation = {}
target_probs = {'traits': {}}

not_founds = []

print(f"traits:")
for trait_class in os.listdir('/home/jl/projects/q00ts/metadata/q00nicorns/input/img'):
    print(f"\t{trait_class}:")

    target_probs['traits'][trait_class] = {}

    df = pd.read_excel('/home/jl/projects/q00ts/metadata/q00nicorns/input/q00nicorns.xlsx', sheet_name=trait_class, skiprows=1)
    df.dropna(how='all', axis=1, inplace=True)
    df.dropna(how='all', axis=0, inplace=True)
    df.columns = ['value', 'occurance', 'filename']
    df['occurance'] = df['occurance'].astype(int)

    class_translation = df[['value', 'filename']].set_index('value')['filename'].to_dict()

    for name, filename in class_translation.items():
        if not path.isfile(path.join(f'/home/jl/projects/q00ts/metadata/q00nicorns/input/img/', trait_class, filename)):
            print(f"Not found: {name}, {filename}")
            not_founds.append((trait_class, name, filename))
            class_translation[name] = None

    for i, row in df.iterrows():
        if class_translation[row['value']] is not None:
            target_probs['traits'][trait_class][row['value']] = row['occurance']
            print(f"\t\t{row['value']}: {row['occurance']}")

    translation[trait_class] = class_translation

missingdf = pd.DataFrame(not_founds, columns=['category', 'name', 'filename'])
print(missingdf)

json.dump(translation, open('/home/jl/projects/q00ts/metadata/q00nicorns/input/filenames.json', 'w'), indent=4)
yaml.dump(target_probs, open('/home/jl/projects/q00ts/metadata/q00nicorns/input/target_probs.yaml', 'w'), indent=4)