from rdkit import Chem
import os
import random
import oddt
from oddt.fingerprints_new import PLEC, fold, sparse_to_dense
import json
import sys
from pymol import cmd
import numpy as np

def filter_structures(structures):
    targs = [i.split('/')[2] for i in structures]
    targs = list(set(targs))
    if 'mArh' in targs and 'Mac1' in targs:
        targs.remove('Mac1')
    if 'MUREECA' in targs and 'MURECCOLI' in targs:
        targs.remove('MUREECOLI')
    
    filtered_structures = []
    for i in structures:
        t = i.split('/')[2]
        if t in targs:
            filtered_structures.append(i)
            targs.remove(t)
    return filtered_structures



all_mols = []
strucs = []

for target in os.listdir('data/ligands'):
    all_mols += [Chem.MolFromMolFile(f'data/ligands/{target}/{i}') for i in os.listdir(f'data/ligands/{target}')]
    strucs += [f'data/ligands/{target}/{i}' for i in os.listdir(f'data/ligands/{target}')]

all_smiles = [Chem.MolToSmiles(i) for i in all_mols]
unique_smiles = list(set(all_smiles))

shuffle_strucs = [i for i in strucs]
random.shuffle(shuffle_strucs)

train_smiles_structures = {}
test_smiles_structures = {} 

for s in range(len(unique_smiles)):
    smiles = unique_smiles[s]
    indices = [i for i in range(len(all_smiles)) if all_smiles[i] == smiles]
    if len(indices) > 1:
        struc_list = [strucs[i] for i in indices]
        filtered = filter_structures(struc_list)
        if len(filtered) > 1:
            final = filtered[:2]
            for m in range(len(shuffle_strucs)):
                if shuffle_strucs[m] not in struc_list and Chem.MolFromMolFile(shuffle_strucs[m]).GetNumAtoms() == Chem.MolFromSmiles(smiles).GetNumAtoms():
                    t = shuffle_strucs[m].split('/')[2]
                    if t not in ''.join(final):
                        if 'TNCA' in ''.join(final):
                            test_smiles_structures[smiles] = (final, shuffle_strucs[m])
                            shuffle_strucs.remove(shuffle_strucs[m])
                            break
                        elif 'TNCA' not in shuffle_strucs[m]:
                            train_smiles_structures[smiles] = (final, shuffle_strucs[m])
                            shuffle_strucs.remove(shuffle_strucs[m])
                            break

def depths(ECFP, min_depth):
    alls = []
    for i in ECFP:
        if int(i) >= min_depth:
            alls += ECFP[i]
    return list(set(alls))

def generate_points(mins, maxes, res=1.5): 
    X, Y, Z = np.mgrid[mins[0]:maxes[0]:res,
                    mins[1]:maxes[1]:res, 
                    mins[2]:maxes[2]:res
                    ]
    return X, Y, Z

def distance(one, two):
    return np.sqrt(
        (one[0]-two[0]) ** 2 +
        (one[1]-two[1]) ** 2 +
        (one[2]-two[2]) ** 2
    )

def write_xyz_file(x, y, z, filename):
    xyz = open(filename, 'w')
    for i in range(len(x)):
        xyz.write(f'Mg {x[i]} {y[i]} {z[i]}\n')
    xyz.close()


def struct_pdb(lig, prot):
    cmd.reinitialize()
    cmd.load(lig, 'lig')
    cmd.load(prot, 'prot')
    cmd.extract('clean', 'prot and HETATM')
    centre = cmd.centerofmass('lig')
    mins, maxes = [i-5 for i in centre], [i+5 for i in centre]
    X, Y, Z = generate_points(mins, maxes)
    X_, Y_, Z_ = [], [], []
    for i in range(len(X.flatten())):
        point = [X.flatten()[i], Y.flatten()[i], Z.flatten()[i]]
        dist = distance(point, centre)
        if dist <= 5:
            X_.append(point[0])
            Y_.append(point[1])
            Z_.append(point[2])
    write_xyz_file(X_, Y_, Z_, 'tmp.xyz')
    cmd.load('tmp.xyz', 'bubble')
    cmd.extract('bad', 'bubble within 2.5 of prot')
    cmd.save('tmp.pdb', 'bubble')
        
    


def get_ECFP(prot):
    lig = next(oddt.toolkit.readfile('pdb', 'tmp.pdb'))
    prot = next(oddt.toolkit.readfile('pdb', prot))

    a, ECFP = PLEC(lig, prot, depth_ligand=0, depth_protein=5)
    ECFP = depths(ECFP, 0)
    ECFP = fold(ECFP, size=2048)
    ECFP = sparse_to_dense(ECFP, size=2048, count_bits=False)
    return [int(i) for i in ECFP]


def get_ECFP_stacked(struc1, struc2):
    prot1, prot2 = struc1.replace('ligand', 'protein'), struc2.replace('ligand', 'protein')
    prot1, prot2 = prot1.replace('sdf', 'pdb'), prot2.replace('sdf', 'pdb')

    struct_pdb(struc1, prot1)
    ECFP1 = get_ECFP(prot1)
    struct_pdb(struc2, prot2)
    ECFP2 = get_ECFP(prot2)

    stacked = []
    for i in range(2048):
        stacked.append(ECFP1[i] + ECFP2[i])
    return stacked


train_X = []
train_y = []
test_X = []
test_y = []

for smiles in train_smiles_structures:
    try:
        get_ECFP_stacked(train_smiles_structures[smiles][0][0], train_smiles_structures[smiles][0][1])
        train_X.append(get_ECFP_stacked(train_smiles_structures[smiles][0][0], train_smiles_structures[smiles][0][1]))
        train_y.append(1)
        train_X.append(get_ECFP_stacked(train_smiles_structures[smiles][0][0], train_smiles_structures[smiles][1]))
        train_y.append(0)
        print(smiles)   
    except:
        print(smiles, sys.exc_info()[1])

print(len(train_X))
for smiles in test_smiles_structures:
    try:
        test_X.append(get_ECFP_stacked(test_smiles_structures[smiles][0][0], test_smiles_structures[smiles][0][1]))
        test_y.append(1)
        test_X.append(get_ECFP_stacked(test_smiles_structures[smiles][0][0], test_smiles_structures[smiles][1]))
        test_y.append(0)
        print(smiles)
    except:
        print(smiles, sys.exc_info()[1])
        raise


print(train_X, train_y)
json.dump(train_X, open('pairs_study/data/x_train.json', 'w'))
json.dump(train_y, open('pairs_study/data/y_train.json', 'w'))
json.dump(test_X, open('pairs_study/data/x_test.json', 'w'))
json.dump(test_y, open('pairs_study/data/y_test.json', 'w'))
