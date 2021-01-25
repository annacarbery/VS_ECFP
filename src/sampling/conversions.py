
def pcd_to_xyz(infile, outfile):
    pcd = open(infile, 'r').read()
    pcd = pcd.split('DATA ascii\n')[1].split('\n')
    xyz = open(outfile, 'w')
    for line in pcd:
        coords = line.split(' ')[:3]
        xyz.write(f'H {(" ").join(coords)}\n')
    xyz.close()