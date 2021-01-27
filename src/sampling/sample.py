from pymol import cmd
from utils import write_xyz_file
import time
import os

def main(targ):
    target = f'../../data/bubbles/{targ}/bubble.xyz'
    cmd.load(target, 'target')
    print(time.ctime())
    target_lines = open(target, 'r').readlines()
    print(len(target_lines))
    point_num = 0
    for line in target_lines:

        os.mkdir(f'../../data/samples/{targ}/{point_num}')

        coords = [float(i) for i in line[2:].strip().split(' ')]
        [x, y, z] = [[i] for i in coords]
        write_xyz_file(x, y, z, '../../test_point.xyz')
        cmd.load('../../test_point.xyz', str(point_num))
        cmd.select('ligand', f'target within 7 of {str(point_num)}')
        cmd.save(f'../../data/samples/{targ}/{point_num}/points.pdb', 'ligand')
        cmd.delete('ligand')
        point_num += 1
        if point_num % 1000 == 0:
            print(time.ctime())
            cmd.reinitialize()
            cmd.load(target, 'target')
        # print(len(target_lines)-point_num)

    print(time.ctime())
