# -*- coding: utf-8 -*-
import csv
import os
import json
import pickle

info: dict[str: tuple[str, str, int]] = dict()


def get_info(path: str):
    gen_size = rec_info_getter(path)

    with (open('info.json', 'w', encoding='utf-8') as f1,
          open('info.csv', 'w', encoding='utf-8') as f2,
          open('info.txt', 'wb') as f3):
        # json saving:
        json.dump(info, f1, separators=(' ', '\n'))
        # csv saving:
        writer = csv.writer(f2, dialect='excel', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in info.items():
            writer.writerow(row)
        # pickle
        pickle.dump(info, f3)

    return gen_size


def rec_info_getter(path: str):
    """"""
    NAMES = ['file', 'dir', 'mount', 'link', 'unbeknown_obj']

    files_n_dirs = os.listdir(path)
    print(f'files_n_dirs: {files_n_dirs}')
    type_: str
    general_size_ = 0

    for file_or_dir in files_n_dirs:
        file_or_dir_ = os.path.join(path, file_or_dir)
        if os.path.islink(file_or_dir_):
            size_ = os.path.getsize(file_or_dir_)
            info[file_or_dir_] = (path, NAMES[3], size_)
        elif os.path.isdir(file_or_dir_):
            # recursion
            size_ = rec_info_getter(file_or_dir_)
            info[file_or_dir_] = (path, NAMES[1], size_)
        elif os.path.isfile(file_or_dir_):
            size_ = os.path.getsize(file_or_dir_)
            info[file_or_dir_] = (path, NAMES[0], size_)
        elif os.path.ismount(file_or_dir_):
            size_ = os.path.getsize(file_or_dir_)
            info[file_or_dir_] = (path, NAMES[2], size_)
        else:
            try:
                size_ = os.path.getsize(file_or_dir_)
            except Exception:
                size_ = 0
                print(f'Congratulations, you found an unbeknown object in your OS!!!')
            info[file_or_dir_] = (path, NAMES[4], size_)

        print(f'size: {size_}')

        general_size_ += size_

    return general_size_


def to_giga_bytes(bytes_q: int) -> int:
    return bytes_q // 1024 ** 3


path1 = 'D:\\Хранилище'
path11 = 'D:\\python\\zalizniak-2010-master\\zalizniak-2010-master\\dictionary'

s = get_info(path11)
print(f'Gen size = {to_giga_bytes(s)} GIGA bytes')




