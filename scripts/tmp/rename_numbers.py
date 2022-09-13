import numpy as np
import pandas as pd
import os
import glob
from os import path

rootpath = '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/img/10_upgrades'

for rootpath in [
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/0_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/1_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/2_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/3_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/4_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/5_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/6_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/7_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/8_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/9_upgrades',
    '/home/jl/projects/q00ts/metadata/FINAL_OUTPUTS/output_0upgrades/json/10_upgrades',
]:

    tokenids = sorted([int(tokenid) for tokenid in os.listdir(rootpath)])[::-1]
    assert max(tokenids) == 4999
    assert min(tokenids) == 0

    for tokenid in tokenids:
        print(f"{tokenid} to {tokenid + 1}")

        tokenpath = rootpath + '/' + str(tokenid)
        newtokenpath = rootpath + '/' + str(tokenid + 1)

        os.system(f'mv {tokenpath} {newtokenpath}')
