import json
from oddt.fingerprints_new import PLEC, fold, sparse_to_dense
import oddt
import os
import numpy as np

def depths(ECFP):
    total = []
    for i in ECFP:
        total += ECFP[i]
    return set(total)

def main(target):

    ref = f'/Users/tyt15771/Documents/VS_ECFP/data/targets/{target}.pdb'
    
    protein = next(oddt.toolkit.readfile('pdb', ref))
    protein.protein = True

    for sample in os.listdir(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}'):

        if not os.path.isfile(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}/{sample}/ECFP_FP.npy'):
            

            lig = f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}/{sample}/points.pdb'
            ligand = next(oddt.toolkit.readfile('pdb', lig))

            x, ECFP = PLEC(ligand, protein)
            ECFP = list(depths(ECFP))
            folded_ECFP = fold(ECFP, size=16384)
            vector_ECFP = sparse_to_dense(folded_ECFP, size=16384)
        
            # json_file = f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}/{sample}/ECFP.json'

            # json.dump(ECFP, open(json_file, 'w'))
            # print(sample)

            npy_file = f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}/{sample}/ECFP_FP.npy'

            np.save(npy_file, vector_ECFP)
            print(sample)