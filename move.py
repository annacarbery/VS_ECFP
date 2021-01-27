import os
import shutil

for target in os.listdir('/Users/tyt15771/Documents/ECFP/frag_structures/'):
    if not os.path.isdir(f'data/ligands/{target}'):
        os.mkdir(f'data/ligands/{target}')
    
    for ligand in os.listdir(f'/Users/tyt15771/Documents/ECFP/frag_structures/{target}'):
        shutil.copyfile(f'/Users/tyt15771/Documents/ECFP/frag_structures/{target}/{ligand}/{ligand}.sdf', f'data/ligands/{target}/{ligand}.sdf')