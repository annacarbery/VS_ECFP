from target_pcd import main as gen_pcd
import os
from utils import dist, sample_pdb, stack_ECFP
import oddt
import numpy as np
import random
from ECFP import main as get_ECFP
import sys
import json

DATA_DIR = '/dls/science/users/tyt15771/DPhil/VS_ECFP/data'
pairs = open(f'{DATA_DIR}/miss_pairs.txt').readlines()

X_test = {}
Y_test = {}
pos = {}
for pair in pairs:
    try:
        print('control pair', pair.strip())
        lig1, lig2 = pair.strip().split(' ')[1], pair.strip().split(' ')[0]
        prot1, prot2 = lig1.replace('sdf', 'pdb').replace('ligands', 'proteins'), lig2.replace('sdf', 'pdb').replace('ligands', 'proteins')
        
        ECFP_ref = get_ECFP(lig1, prot1)
        gen_pcd(prot2, 'control')
        bubble_points = [[i[30:38], i[38:46], i[46:54]] for i in open('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/bubble_test.pdb', 'r').readlines() if i.startswith('HETATM')]
        

        ECFP = []
        pos[pair.strip()] = []
        
        for point in bubble_points[:10:5]:
            sample_points = [i for i in bubble_points if dist(i, point) < 5]
            sample_pdb(sample_points, 'control')
            ECFP.append(get_ECFP('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_test.pdb', prot2))
            pos[pair.strip()].append(point)

        X_test[pair.strip()] = [stack_ECFP(ECFP_ref, i) for i in ECFP]
        Y_test[pair.strip()] = [0]*len(ECFP)

        print('control pair finished', pair.strip(), len(X_test[pair.strip()]), len(Y_test[pair.strip()]))

        json.dump(X_test, open('X_control.json', 'w'))
        json.dump(Y_test, open('Y_control.json', 'w'))
        json.dump(pos, open('pos_control.json', 'w'))
    except:
        print(pair.strip(), sys.exc_info()[1])


print('control data completed')