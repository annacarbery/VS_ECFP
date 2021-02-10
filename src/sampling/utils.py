import numpy as np
from pymol import cmd

def dist(point1, point2):
    return np.sqrt(
        sum([
            (float(point1[i])-float(point2[i])) ** 2 for i in range(len(point1))
        ])
    )

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
        xyz.write(f'Mg {x[i]} {y[i]} {z[i]}\n')
    xyz.close()


def reduce_cloud(filename, newfilename, prot, near=2, far=4):
    cmd.reinitialize()
    cmd.load(prot, 'prot')
    cmd.extract('hets', 'prot and HETATM')
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

def sample_pdb(points, datatype):
    X, Y, Z = [i[0] for i in points], [i[1] for i in points], [i[2] for i in points]
    write_xyz_file(X, Y, Z, f'/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_{datatype}.xyz')
    cmd.reinitialize()
    cmd.load(f'/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_{datatype}.xyz', 'sample')
    cmd.save(f'/dls/science/users/tyt15771/DPhil/VS_ECFP/data/tmp/sample_{datatype}.pdb', 'sample')

def stack_ECFP(ref, sample):
    stacked = [ref[i]+sample[i] for i in range(len(ref))]
    return stacked