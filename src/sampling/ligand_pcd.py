import numpy as np
from pymol import cmd
import argparse
import os
from utils import box_edges, generate_points, write_xyz_file, reduce_ligand_cloud, bubble_xyz

ligand = '/Users/tyt15771/Documents/ECFP/frag_structures/Mpro/Mpro-x0678A/Mpro-x0678A.sdf'

mins, maxes = box_edges(ligand, padding=4)

print(mins, maxes)
X, Y, Z = generate_points(mins, maxes)
write_xyz_file(X.flatten(), Y.flatten(), Z.flatten(), filename=f'../../lig_box.xyz')
reduce_ligand_cloud(f'../../lig_box.xyz', f'../../lig_bubble.pdb', '/Users/tyt15771/Documents/ECFP/frag_structures/Mpro/Mpro-x0678A/Mpro-x0678A.pdb')
bubble_xyz(f'../../lig_bubble.pdb')