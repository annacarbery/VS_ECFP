import os
import numpy as np
import oddt
from oddt.fingerprints_new import PLEC, fold, sparse_to_dense
import json
import sys

def depths(ECFP, min_depth):
    total = []
    for i in ECFP:
        if int(i) >= min_depth:
            total += ECFP[i]
    return list(set(total))


def reference_ECFP(target, ligand):
    target_pdb = f'/Users/tyt15771/Documents/VS_ECFP/data/targets/{target}.pdb'
    protein = next(oddt.toolkit.readfile('pdb', target_pdb))
    protein.protein = True

    ligand = next(oddt.toolkit.readfile('sdf', f'/Users/tyt15771/Documents/ECFP/frag_structures/{target}/{ligand}/{ligand}.sdf'))

    x, ECFP = PLEC(ligand, protein)
    ECFP = depths(ECFP, 0)
    ECFP = fold(ECFP, size=16384)
    ECFP = sparse_to_dense(ECFP, size=16384)
    print(sum(ECFP))

    return ECFP


def get_arrays(target, ligand, new_target, new_ligand):
    reference = reference_ECFP(target, ligand)
    print(reference)
    for sample in os.listdir(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{new_target}'):
        sample_ECFP = np.load(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{new_target}/{sample}/ECFP_FP.npy')
    
        input_array = np.concatenate((reference, sample_ECFP)).reshape(2, 16384)

        distance = json.load(open(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{new_target}/{sample}/distances.json', 'r'))[new_ligand+'.sdf']
        
        if distance < 4:
            classification = 'hit'
        elif distance < 7:
            classification = 'maybe'
        else:
            classification = 'miss'

        filetag = f'{classification}/{ligand}_{new_ligand}_{sample}'

        if not os.path.isdir(f'/Users/tyt15771/Documents/VS_ECFP/data/input/{filetag}'):
            os.mkdir(f'/Users/tyt15771/Documents/VS_ECFP/data/input/{filetag}')

        np.save(f'/Users/tyt15771/Documents/VS_ECFP/data/input/{filetag}/array.npy', input_array)
        
        with open(f'/Users/tyt15771/Documents/VS_ECFP/data/input/{filetag}/distance.txt', 'w') as w:
            w.write(str(distance))
            w.close()

def main():

    pairs = json.load(open('/Users/tyt15771/Documents/VS_ECFP/data/same_compound_hits.json', 'r'))

    for pair in pairs:

        reference = pair[0]
        ref_prot = pair[0].split('-')[0]

        test_lig = pair[1]
        test_prot = pair[1].split('-')[0]

        get_arrays(ref_prot, reference, test_prot, test_lig)




main()