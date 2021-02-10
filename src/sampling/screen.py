from rdkit import Chem
import os
import random
# import oddt
# from oddt.fingerprints_new import PLEC, fold, sparse_to_dense
import json
import sys
# from pymol import cmd
# import numpy as np
import argparse
import subprocess

def filter_structures(structures):
    targs = [i.split('/')[2] for i in structures]
    targs = list(set(targs))
    if 'mArh' in targs and 'Mac1' in targs:
        targs.remove('Mac1')
    if 'MUREECA' in targs and 'MUREECOLI' in targs:
        targs.remove('MUREECOLI')
    
    filtered_structures = []
    for i in structures:
        t = i.split('/')[2]
        if t in targs:
            filtered_structures.append(i)
            targs.remove(t)
    return filtered_structures


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', required=True)
args = vars(parser.parse_args())
target = args["target"]


all_mols = []
strucs = []

for targ in os.listdir('data/ligands'):
    all_mols += [Chem.MolFromMolFile(f'data/ligands/{targ}/{i}') for i in os.listdir(f'data/ligands/{targ}')]
    strucs += [f'data/ligands/{targ}/{i}' for i in os.listdir(f'data/ligands/{targ}')]


all_smiles = [Chem.MolToSmiles(i) for i in all_mols]
unique_smiles = list(set(all_smiles))

shuffle_strucs = [i for i in strucs]
random.shuffle(shuffle_strucs)

train_structures = []
test_structures = [] 
control_structures = []

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
                        if target in ''.join(final):
                            control_structures.append([[i for i in final if target in i][0], shuffle_strucs[m]])
                            shuffle_strucs.remove(shuffle_strucs[m])
                            test_structures.append([final[0], final[1].strip()])
                            break
                        else:
                            train_structures.append(final)
                            shuffle_strucs.remove(shuffle_strucs[m])
                            break

train = open('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/pairs.txt', 'w')
for i in train_structures:
    train.write(f'{i[0]} {i[1]}\n')
train.close()

test = open('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/test_pairs.txt', 'w')
for i in test_structures:
    if target in i[0]:
        test.write(f'{i[0]} {i[1]}\n')
    else:
        test.write(f'{i[1]} {i[0]}\n')
test.close()

control = open('/dls/science/users/tyt15771/DPhil/VS_ECFP/data/miss_pairs.txt', 'w')
for i in control_structures:
    if target in i[0]:
        control.write(f'{i[0]} {i[1]}\n')
    else:
        control.write(f'{i[1]} {i[0]}\n')
control.close()
print('written')

subprocess.Popen(['python', '/dls/science/users/tyt15771/DPhil/VS_ECFP/src/sampling/prepare.py'])
subprocess.Popen(['python', '/dls/science/users/tyt15771/DPhil/VS_ECFP/src/sampling/prepare_test.py'])
subprocess.Popen(['python', '/dls/science/users/tyt15771/DPhil/VS_ECFP/src/sampling/prepare_control.py'])