from target_pcd import main as gen_pcd
from sample import main as sample_surface
import os

for target in os.listdir('/Users/tyt15771/Documents/VS_ECFP/data/targets'):
    if 'Mpro' in target:
        print(target.split('.')[0])
        gen_pcd(target.split('.')[0])
        sample_surface(target.split('.')[0])


