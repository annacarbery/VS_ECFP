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
pairs = open(f'{DATA_DIR}/test_pairs.txt').readlines()

X_test = {}
Y_test = {}
pos = {}
for pair in pairs:
    print('test pair:', pair.strip())
    try:

        lig1, lig2 = pair.strip().split(' ')[1], pair.strip().split(' ')[0]
        prot1, prot2 = lig1.replace('sdf', 'pdb').replace('ligands', 'proteins'), lig2.replace('sdf', 'pdb').replace('ligands', 'proteins')
        
        lig = next(oddt.toolkit.readfile('sdf', lig2))
        lig = [np.mean([i[0] for i in lig.coords]), np.mean([i[1] for i in lig.coords]), np.mean([i[2] for i in lig.coords])]

        ECFP_ref = get_ECFP(lig1, prot1)
        gen_pcd(prot2, 'test')
        bubble_points = [[i[30:38], i[38:46], i[46:54]] for i in open('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/bubble_test.pdb', 'r').readlines() if i.startswith('HETATM')]
        point_dists = [dist(point, lig) for point in bubble_points]

        pos_points = [bubble_points[i] for i in range(len(bubble_points)) if point_dists[i] < 5]
        neg_points = [bubble_points[i] for i in range(len(bubble_points)) if point_dists[i] > 5]

        pos_ECFP = []
        neg_ECFP = []
        pos[pair.strip()] = []

        for point in pos_points[::5]:
            sample_points = [i for i in bubble_points if dist(i, point) < 5]
            sample_pdb(sample_points, 'test')
            pos_ECFP.append(get_ECFP('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_test.pdb', prot2))
            pos[pair.strip()].append(point)

        for point in neg_points[::5]:
            sample_points = [i for i in bubble_points if dist(i, point) < 5]
            sample_pdb(sample_points, 'test')
            neg_ECFP.append(get_ECFP('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_test.pdb', prot2))
            pos[pair.strip()].append(point)



        X_test[pair.strip()] = [stack_ECFP(ECFP_ref, i) for i in pos_ECFP] + [stack_ECFP(ECFP_ref, i) for i in neg_ECFP]
        Y_test[pair.strip()] = [1]*len(pos_ECFP) + [0]*len(neg_ECFP)

        print('test pair finished:', pair.strip(), len(X_test[pair.strip()]), len(Y_test[pair.strip()]))

        json.dump(X_test, open('X_test.json', 'w'))
        json.dump(Y_test, open('Y_test.json', 'w'))
        json.dump(pos, open('pos_test.json', 'w'))
    except:
        print(pair.strip(), sys.exc_info()[1])


print('test data completed')

