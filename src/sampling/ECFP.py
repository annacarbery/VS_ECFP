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

def main(lig, prot):

    protein = next(oddt.toolkit.readfile('pdb', prot))
    protein.protein = True

    ligand = next(oddt.toolkit.readfile(lig.split('.')[1], lig))
    
    x, ECFP = PLEC(ligand, protein, depth_ligand=0, depth_protein=5)
    ECFP = list(depths(ECFP))
    folded_ECFP = fold(ECFP, size=4096)
    vector_ECFP = sparse_to_dense(folded_ECFP, size=4096, count_bits=False)
    return [int(i) for i in vector_ECFP]

    