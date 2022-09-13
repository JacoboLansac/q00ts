import numpy as np
import pandas as pd
import os
import numpy as np
import pandas as pd
import os
import glob
from os import path
import json

traits = json.load(open(
    "/metadata/FINAL_OUTPUTS/output_first_stage/traits_info/collection_traits.json", 'r'))

df = pd.DataFrame.from_records(traits).T
df.index = (df.index.astype(int) + 1).astype(str)

probs = df.copy()
stats = {}
for trait in df.columns:
    probabilities = (df[trait].value_counts() / len(df)).to_dict()
    probs[trait] = df[trait].replace(probabilities)

prob = probs.cumprod(axis=1)['sky']
prob.name = 'probability'

df['probability'] = prob

2927
1744

3218

2440
4911

df['sky'].unique()

df[df['skin'] == 'multicolor'].sort_values(by='probability')
df[df['skin'] == 'leopard'].sort_values(by='probability')
df[df['skin'] == 'bengal-tiger'].sort_values(by='probability')
df[df['sky'] == 'sauron-eye'].sort_values(by='probability')


