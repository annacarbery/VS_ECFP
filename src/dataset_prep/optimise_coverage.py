from pymol import cmd
from oddt.fingerprints_new import PLEC
import numpy as np
import oddt
import json


def depths(ECFP, min_depth):
    total = []
    for i in ECFP:
        if int(i) >= min_depth:
            total += ECFP[i]
    return list(set(total))

def generate_points(mins, maxes, res=1.5): 
    X, Y, Z = np.mgrid[mins[0]:maxes[0]:res,
                    mins[1]:maxes[1]:res, 
                    mins[2]:maxes[2]:res
                    ]
    return X, Y, Z


def write_xyz_file(x, y, z, filename):
    xyz = open(filename, 'w')
    for i in range(len(x)):
        xyz.write(f'Mg {x[i]} {y[i]} {z[i]}\n')
    xyz.close()
    
def tversky(a, b):
    match = 0
    for i in set(a):
        if i in b:
            match += 1
    return match / len(set(a))


def get_sim(radius, target, i):

    cmd.reinitialize()
    cmd.load(f'/Users/tyt15771/Documents/VS_ECFP/data/ligands/{target}/{i}', 'lig')
    cmd.load(f'/Users/tyt15771/Documents/VS_ECFP/data/proteins/{target}/{i[:-4]}.pdb', 'prot')
    cmd.extract('hets', 'prot and HETATM')

    centre = cmd.centerofmass('lig')
    mins, maxes = [i-radius for i in centre], [i+radius for i in centre]
    x, y, z = generate_points(mins, maxes, res=1.0)
    write_xyz_file(x.flatten(), y.flatten(), z.flatten(), 'lig_box.xyz')

    cmd.load('lig_box.xyz', 'lig_bubble')
    # cmd.select('lig_bubble', 'box within 4 of lig')
    cmd.extract('close', 'lig_bubble within 2.5 of prot')
    cmd.save('lig_bubble.pdb', 'lig_bubble')


    sample = next(oddt.toolkit.readfile('pdb', 'lig_bubble.pdb'))
    ligand = next(oddt.toolkit.readfile('sdf', f'/Users/tyt15771/Documents/VS_ECFP/data/ligands/{target}/{i}'))

    ref = next(oddt.toolkit.readfile('pdb', f'/Users/tyt15771/Documents/VS_ECFP/data/targets/{target}.pdb'))
    ref.protein = True

    protein = next(oddt.toolkit.readfile('pdb', f'/Users/tyt15771/Documents/VS_ECFP/data/proteins/{target}/{i[:-4]}.pdb'))
    protein.protein = True

    dist = 6.5
    x, LT = PLEC(ligand, protein, distance_cutoff=dist)
    x, SR = PLEC(sample, ref, distance_cutoff=dist)
    LT = depths(LT, 0)
    SR = depths(SR, 0)
    print(len(LT), len(SR))
    LT_SR = tversky(LT, SR)
    print(i, LT_SR)
    return LT_SR

pairs = open('/Users/tyt15771/Documents/VS_ECFP/paired_structures.txt', 'r').readlines()
structures = set([i.split(' ')[0] for i in pairs])
LTSR_2 = []
LTSR_3 = []
LTSR_4 = []
LTSR_5 = []
LTSR_7 = []
LTSR_9 = []

print(len(structures))
for i in structures:
    try:
        target = i.split('-')[0] if 'NUDT7A' not in i else 'NUDT7A'
        
        LTSR_2.append(get_sim(2, target, i))
        LTSR_3.append(get_sim(3, target, i))
        LTSR_4.append(get_sim(4, target, i))
        LTSR_5.append(get_sim(5, target, i))
        LTSR_7.append(get_sim(7, target, i))
        LTSR_9.append(get_sim(9, target, i))

        json.dump(LTSR_2, open('LTSR_2.json', 'w'))
        json.dump(LTSR_3, open('LTSR_3.json', 'w'))
        json.dump(LTSR_4, open('LTSR_4.json', 'w'))
        json.dump(LTSR_5, open('LTSR_5.json', 'w'))
        json.dump(LTSR_7, open('LTSR_7.json', 'w'))
        json.dump(LTSR_9, open('LTSR_9.json', 'w'))
        
    except:
        print(i, 'error')


