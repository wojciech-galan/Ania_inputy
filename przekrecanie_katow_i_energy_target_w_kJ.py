#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import shutil
import argparse
from typing import Tuple
from typing import List
from typing import Dict


def read_dat_file(path: str) -> Tuple[List]:
    angle1, angle2, e_kcal, e_kj = [], [], [], []
    with open(path) as f:
        # column names
        f.readline()
        # blank line
        f.readline()
        # real data
        while True:
            try:
                angle1_point, angle2_point, e_kcal_point, e_kj_point = f.readline().split()
            except ValueError:  # blank line - end of data
                break
            angle1.append(str(float(angle1_point))) # to change, for example '179' to '179.0'
            angle2.append(str(float(angle2_point)))
            e_kcal.append(e_kcal_point)
            e_kj.append(e_kj_point)
    return angle1, angle2, e_kcal, e_kj


def change_f_paths(old_paths: List[str], new_dir_path:str, replace_dict: Dict[str, str]) -> Dict[str, str]:
    new_paths = {}
    for old_path in old_paths:
        found = False
        for part_to_be_replaced, new_part in replace_dict.items():
            if old_path.endswith(part_to_be_replaced):
                old_name = os.path.basename(old_path)
                new_paths[old_path] = os.path.join(new_dir_path, old_name.replace(part_to_be_replaced, new_part))
                found = True
                break
        assert found
    return new_paths


def process_directory(old_dir_path, new_dir_path):
    dat_f_list = glob.glob(os.path.join(old_dir_path, '*.dat'))
    assert len(dat_f_list) == 1
    dat_f = dat_f_list[0]
    pdb_f_list = glob.glob(os.path.join(old_dir_path, '*.pdb'))
    new_angles, old_angles, _, energies_kj = read_dat_file(dat_f)
    old_names = [''.join(['.', x.replace('-', '_'), '.pdb']) for x in old_angles]
    new_names = [''.join(['.', x, '.pdb']) for x in new_angles]
    path_replace_dict = change_f_paths(pdb_f_list, new_dir_path, dict(zip(old_names, new_names)))
    os.makedirs(os.path.dirname(list(path_replace_dict.values())[0]))
    for old_path, new_path in path_replace_dict.items():
        shutil.copy(old_path, new_path)
    return energies_kj


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory")
    parser.add_argument("output_directory")
    args = parser.parse_args()
    in_dir = args.input_directory #'/home/wojtek/Dokumenty/Ania_do_fitowania/dla_Wojtka_new/'
    out_dir = args.output_directory #'/home/wojtek/Dokumenty/Ania_do_fitowania/dla_Wojtka_new_processed/'
    qm = []
    for directory in sorted(os.listdir(in_dir)):
        print(directory)
        qm.extend(process_directory(os.path.join(in_dir, directory), os.path.join(out_dir, directory)))
    with open(os.path.join(out_dir, 'qm'), 'w') as f:
        f.write('\n'.join(qm))
