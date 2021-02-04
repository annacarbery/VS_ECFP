from rdkit import Chem
import os
from rdkit import DataStructs
import shutil

cases = open('/dls/science/users/tyt15771/DPhil/VS_ECFP/cases.txt', 'r').readlines()

xtal_dir = '/dls/science/users/tyt15771/DPhil/VS_ECFP/data/ligands'
target_dir = '/dls/science/users/tyt15771/DPhil/VS_ECFP/data/proteins'

num = 1
for i in cases:
    print(i)
    xtals = i.strip().split(', ')
    print(xtals)
    os.mkdir(f'case_studies/{num}')
    for x in xtals:
        target = x.split('-')[0]
        print(target, x)
        shutil.copyfile(f'{xtal_dir}/{target}/{x}', f'case_studies/{num}/{x}')
        shutil.copyfile(f'{target_dir}/{target}/{x[:-4]}.pdb', f'case_studies/{num}/{x[:-4]}.pdb')
    
    num += 1