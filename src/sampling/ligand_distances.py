import oddt
import os
import numpy as np
import json

def get_dist(a, b):
    return np.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])** 2 +
        (a[2]-b[2])**2
    )

def get_com(coords):
    com = []
    for i in range(3):
        com.append(np.mean([l[i] for l in coords]))
    return com

def main(target):
    for sample in os.listdir(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}'):

        pdb = f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}/{sample}/points.pdb'
        sample_patch = next(oddt.toolkit.readfile('pdb', pdb))

        sample_com = get_com(np.asarray(sample_patch.coords))


        dists = {}

        for lig in os.listdir(f'/Users/tyt15771/Documents/VS_ECFP/data/ligands/{target}'):
            lig_mol = next(oddt.toolkit.readfile('sdf', f'/Users/tyt15771/Documents/VS_ECFP/data/ligands/{target}/{lig}'))

            distance = get_dist(sample_com, get_com(np.asarray(lig_mol.coords)))

            dists[lig] = distance

        json.dump(dists, open(f'/Users/tyt15771/Documents/VS_ECFP/data/samples/{target}/{sample}/distances.json', 'w'))

        