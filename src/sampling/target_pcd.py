import numpy as np
from pymol import cmd
import argparse
import os

def box_edges(target_pdb, padding=10):
    cmd.reinitialize()
    cmd.load(target_pdb, 'prot')
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
        xyz.write(f'P {x[i]} {y[i]} {z[i]}\n')
    xyz.close()


def reduce_cloud(filename, newfilename, near=3, far=8):
    cmd.load(filename, 'cloud')
    cmd.extract('near', f'cloud within {near} of prot')
    cmd.extract('bubble', f'cloud within {far} of prot')
    cmd.save(newfilename, 'bubble')


def bubble_xyz(bubble_filename):
    bubble_lines = [i for i in open(bubble_filename, 'r').readlines() if i.startswith('HETATM')]
    x = [float(l[30:38]) for l in bubble_lines]
    y = [float(l[38:46]) for l in bubble_lines]
    z = [float(l[46:54]) for l in bubble_lines]
    write_xyz_file(x, y, z, filename=bubble_filename[:-4]+'.xyz')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--target", required=True,
                        )
    args = vars(parser.parse_args())
    target = args["target"]

    TARGET_DIR = '/Users/tyt15771/Documents/VS_ECFP/data/targets'
    BUBBLE_DIR = '/Users/tyt15771/Documents/VS_ECFP/data/bubbles'

    if not os.path.isdir(f'{BUBBLE_DIR}/{target}'):
        os.mkdir(f'{BUBBLE_DIR}/{target}')

    # making 3D grid over protin
    mins, maxes = box_edges(f'{TARGET_DIR}/{target}.pdb')
    X, Y, Z = generate_points(mins, maxes)
    write_xyz_file(X.flatten(), Y.flatten(), Z.flatten(), filename=f'{BUBBLE_DIR}/{target}/box.xyz')

    # trim grid to layer over surface of protein
    reduce_cloud(f'{BUBBLE_DIR}/{target}/box.xyz', f'{BUBBLE_DIR}/{target}/bubble.pdb')
    bubble_xyz(f'{BUBBLE_DIR}/{target}/bubble.pdb')
