import numpy as np
from pymol import cmd

def box_edges(target_pdb, padding=10, clean=False):
    cmd.reinitialize()
    cmd.load(target_pdb, 'prot')
    if clean == True:
        cmd.extract('hets', 'prot and HETATM')
    ([minX, minY, minZ],[maxX, maxY, maxZ]) = cmd.get_extent('all')
    mins, maxes = cmd.get_extent('all')
    mins, maxes = [m-padding for m in mins], [m+padding for m in maxes]
    
    return mins, maxes


def generate_points(mins, maxes, res=1.5): 
    X, Y, Z = np.mgrid[mins[0]:maxes[0]:res,
                    mins[1]:maxes[1]:res, 
                    mins[2]:maxes[2]:res
                    ]
    return X, Y, Z


def write_xyz_file(x, y, z, filename):
    xyz = open(filename, 'w')
    for i in range(len(x)):
        xyz.write(f'H {x[i]} {y[i]} {z[i]}\n')
    xyz.close()


def reduce_cloud(filename, newfilename, near=2.5, far=8):
    cmd.load(filename, 'cloud')
    cmd.extract('near', f'cloud within {near} of prot')
    cmd.extract('bubble', f'cloud within {far} of prot')
    cmd.save(newfilename, 'bubble')


def reduce_ligand_cloud(filename, newfilename, target_filename, prot_distance=2.5, ligand_distance=4):
    cmd.load(target_filename, 'target')
    cmd.extract('hets', 'target and HETATM')
    cmd.load(filename, 'ligand_box')
    cmd.extract('protein_close', f'ligand_box within {prot_distance} of target')
    cmd.save('../../smallbox.pdb', 'ligand_box')
    cmd.select('lig_bubble', f'ligand_box within {ligand_distance} of prot')
    cmd.save(newfilename, 'lig_bubble')


def bubble_xyz(bubble_filename):
    bubble_lines = [i for i in open(bubble_filename, 'r').readlines() if i.startswith('HETATM')]
    x = [float(l[30:38]) for l in bubble_lines]
    y = [float(l[38:46]) for l in bubble_lines]
    z = [float(l[46:54]) for l in bubble_lines]
    write_xyz_file(x, y, z, filename=bubble_filename[:-4]+'.xyz')
