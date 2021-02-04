from target_pcd import main as gen_pcd
from sample import main as sample_surface
import os
import shutil
from ECFP import main as gen_ECFP
from ligand_distances import main as get_lig_dists

def make_dir(pathname):
    if not os.path.isdir(pathname):
        os.mkdir(pathname)

DATA_DIR = f'{os.getcwd()}/data'
print(DATA_DIR)

make_dir(f'{DATA_DIR}/samples/')
make_dir(f'{DATA_DIR}/bubbles/')

for target in os.listdir(f'{DATA_DIR}/targets'):
    if 'Mpro' in target:
        try:

            print(target.split('.')[0])
            if os.path.isdir(f'{DATA_DIR}/samples/{target.split(".")[0]}'):
                shutil.rmtree(f'{DATA_DIR}/samples/{target.split(".")[0]}')
            os.mkdir(f'{DATA_DIR}/samples/{target.split(".")[0]}')

            gen_pcd(target.split('.')[0])
            print('made target bubble')

            sample_surface(target.split('.')[0])
            print('sampled target surface')

            # gen_ECFP(target.split('.')[0])
            # print('generated patch ECFPs')

            # get_lig_dists(target.split('.')[0])

            print(target, 'done')
        except:
            print(target, 'failed')
            raise
    