from target_pcd import main as gen_pcd
# from sample import main as sample_surface
import os
from utils import dist, sample_pdb, stack_ECFP
import oddt
import numpy as np
import random
# import shutil
from ECFP import main as get_ECFP
# from ligand_distances import main as get_lig_dists
import sys
import json

DATA_DIR = f'{os.getcwd()}/data'
print(DATA_DIR)

X_train = {}
Y_train = {}

for pair in open(f'{DATA_DIR}/pairs.txt', 'r').readlines():
    print('training pair', pair.strip())
    try:
        lig1, lig2 = pair.strip().split(' ')[0], pair.strip().split(' ')[1]
        prot1, prot2 = lig1.replace('sdf', 'pdb').replace('ligands', 'proteins'), lig2.replace('sdf', 'pdb').replace('ligands', 'proteins')
        
        lig = next(oddt.toolkit.readfile('sdf', lig2))
        lig = [np.mean([i[0] for i in lig.coords]), np.mean([i[1] for i in lig.coords]), np.mean([i[2] for i in lig.coords])]

        ECFP_ref = get_ECFP(lig1, prot1)
        gen_pcd(prot2, 'train')
        bubble_points = [[i[30:38], i[38:46], i[46:54]] for i in open('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/bubble_train.pdb', 'r').readlines() if i.startswith('HETATM')]
        point_dists = [dist(point, lig) for point in bubble_points]

        pos_points = [bubble_points[i] for i in range(len(bubble_points)) if point_dists[i] < 5]
        neg_points = [bubble_points[i] for i in range(len(bubble_points)) if point_dists[i] > 12]
        random.shuffle(neg_points)
        neg_points = neg_points[:len(pos_points)]

        pos_ECFP = []
        neg_ECFP = []

        for point in pos_points:
            sample_points = [i for i in bubble_points if dist(i, point) < 5]
            sample_pdb(sample_points, 'train')
            pos_ECFP.append(get_ECFP('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_train.pdb', prot2))


        for point in neg_points:
            sample_points = [i for i in bubble_points if dist(i, point) < 5]
            sample_pdb(sample_points, 'train')
            neg_ECFP.append(get_ECFP('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_train.pdb', prot2))



        X_train[pair.strip()] = [stack_ECFP(ECFP_ref, i) for i in pos_ECFP] + [stack_ECFP(ECFP_ref, i) for i in neg_ECFP]
        Y_train[pair.strip()] = [1]*len(pos_ECFP) + [0]*len(neg_ECFP)


        print('train pair finished:', pair.strip(), len(X_train[pair.strip()]), len(Y_train[pair.strip()]))

        json.dump(X_train, open('X_train.json', 'w'))
        json.dump(Y_train, open('Y_train.json', 'w'))
    except:
        print(pair.strip(), sys.exc_info()[1])

print('training data completed')