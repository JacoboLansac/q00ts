import json

import numpy as np
import pandas as pd
import os
from os import path


for tokenid in range(1, 5001):

    newpath = f"/home/jl/projects/q00ts/metadata/q00nicorns/output/json/1_upgrades/{tokenid}"
    oldpath = f"/home/jl/projects/q00ts/metadata/q00nicorns/output.bkp/json/1_upgrades/{tokenid}"

    newdata = json.load(open(newpath, 'r'))
    olddata = json.load(open(oldpath, 'r'))
    
    print(f"Checked {tokenid}")

    if not hash(str(newdata)) == hash(str(olddata)):
        print(f"Different metadata: {tokenid}")