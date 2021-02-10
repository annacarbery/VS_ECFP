import numpy as np
import argparse
import os
from utils import generate_points, write_xyz_file, reduce_cloud

def main(target, datatype):

    coords = [[i[30:38], i[38:46], i[46:54]] for i in open(target, 'r').readlines() if i.startswith('ATOM')]
    x, y, z = [float(i[0]) for i in coords], [float(i[1]) for i in coords], [float(i[2]) for i in coords]

    # making 3D grid over protin
    mins, maxes = [min(x), min(y), min(z)], [max(x), max(y), max(z)]
    X, Y, Z = generate_points(mins, maxes)
    write_xyz_file(X.flatten(), Y.flatten(), Z.flatten(), filename=f'/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/box_{datatype}.xyz')

    # trim grid to layer over surface of protein
    reduce_cloud(filename=f'/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/box_{datatype}.xyz', newfilename=f'/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/bubble_{datatype}.pdb', prot=target, near=2.5, far=4)
