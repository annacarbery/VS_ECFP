import numpy as np
from pymol import cmd
import argparse
import os
from utils import box_edges, generate_points, write_xyz_file, reduce_cloud, bubble_xyz


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
    mins, maxes = box_edges(f'{TARGET_DIR}/{target}.pdb', clean=True)
    X, Y, Z = generate_points(mins, maxes)
    write_xyz_file(X.flatten(), Y.flatten(), Z.flatten(), filename=f'{BUBBLE_DIR}/{target}/box.xyz')

    # trim grid to layer over surface of protein
    reduce_cloud(f'{BUBBLE_DIR}/{target}/box.xyz', f'{BUBBLE_DIR}/{target}/bubble.pdb')
    bubble_xyz(f'{BUBBLE_DIR}/{target}/bubble.pdb')
