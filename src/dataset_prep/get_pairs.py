from rdkit import Chem
import os
from rdkit import DataStructs


target_ligands = {}
for target in os.listdir('/Users/tyt15771/Documents/VS_ECFP/data/ligands'):
    target_ligands[target] = []
    for sdf in os.listdir(f'/Users/tyt15771/Documents/VS_ECFP/data/ligands/{target}'):
        mol = Chem.MolFromMolFile(f'/Users/tyt15771/Documents/VS_ECFP/data/ligands/{target}/{sdf}')
        target_ligands[target].append([sdf, mol])

tot = 0
for target in target_ligands:
    fps = [(i[0], Chem.RDKFingerprint(i[1])) for i in target_ligands[target]]
    for target2 in target_ligands:
        if target != target2:
            if 'Mac1_mArh' != f'{target}_{target2}' and 'Mac1_mArh' != f'{target2}_{target}' and 'MUREECA_MUREECOLI' != f'{target2}_{target}' and 'MUREECA_MUREECOLI' != f'{target}_{target2}':
                fps2 = [(i[0], Chem.RDKFingerprint(i[1])) for i in target_ligands[target2]]

                for fp in fps:
                    for fp2 in fps2:
                        if DataStructs.FingerprintSimilarity(fp[1], fp2[1]) == 1:
                            print(fp[0], fp2[0])
                            tot += 1

print(tot)
            