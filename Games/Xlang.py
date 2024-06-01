# йазыгг падонкафф (прастити (нет) )
# -*- coding: utf-8 -*-
import csv
import os
import json
import pickle


doubleable = []

# vowels:
prime_vowels = ['а', 'и', 'о', 'у', 'ы', 'э']
vowels_pairs = {'а': 'о', 'о': 'а', 'и': 'е', 'е': 'и'}
composite_vowels = {'е': 'йэ', 'ё': 'йо', 'ю': 'йу', 'я': 'йа'}

# consonants:
voiced_consonants = {'б', 'в', 'г', 'д', 'ж', 'з', 'л', 'м', 'н', 'р'}  # [б], [в], [г], [д], [ж], [з], [л], [м], [н], [р]
voiceless_consonants = {'к', 'п', 'c', 'т', 'ф', 'x', 'ц', 'ч', 'ш', 'щ'}  # [к], [п], [с], [т], [ф], [х], [ц], [ч], [ш], [щ]
consonants_pairs = {
    'г': 'к', 'б': 'п', 'в': 'ф', 'д': 'т', 'з': 'c', 'ж': 'ш',
    'к': 'г', 'п': 'б', 'ф': 'в', 'т': 'д', 'c': 'з', 'ш': 'ж'
}

# doubling:
doubleables = {'ф', 'г', 'ц'}

# replacements:
replaceables = {'тс': 'ц', 'ц': 'тс'}

# omits:
omittables = {'й'}


# TODO: words dictionary is badly needed...

# some rules (briefing):
# 1. unstressed vowels can be replaced by pairs from vowels_pairs dictionary if they exist... (stress dictionary needed)
# 2. composite vowels can be replaced by their transcription pairs from composite_vowels dict...
# 3. voiceless consonants can be replaced by their voiced equivalents and vice versa  (???) if they are followed by another voiceless consonant /
# they are situated in the end of the word...
# 4. some consonants in the end of the word can be doubled if they lies in doubleables set...
# 5. some parts can be replaced by another ones -> replaceables dict is created for this purpose...
# 6. some letters can be omitted in some cases: omittables set...
# 7. some several words can be connected in the bigger one (when ???)
#
#
#


class Word:
    def __init__(self):
        ...


class Mutation:
    def __init__(self):
        ...


def translate(word: str) -> str:
    # dictionaries loading:
    stress_dict = {}
    path_ = 'D:\\python\\zalizniak-2010-master\\zalizniak-2010-master\\dictionary'
    gen_size = rec_info_getter(path_)


def rec_info_getter(path: str):
    """"""
    files_n_dirs = os.listdir(path)
    print(f'files_n_dirs: {files_n_dirs}')
    type_: str
    general_size_ = 0

    for file_or_dir in files_n_dirs:
        file_or_dir_ = os.path.join(path, file_or_dir)
        if os.path.isdir(file_or_dir_):
            # recursion
            size_ = rec_info_getter(file_or_dir_)
            ...
        elif os.path.isfile(file_or_dir_):
            size_ = os.path.getsize(file_or_dir_)
            ...
        else:
            try:
                size_ = os.path.getsize(file_or_dir_)
            except Exception:
                size_ = 0
                print(f'Congratulations, you found an unbeknown object in your OS!!!')

        print(f'size: {size_}')

        general_size_ += size_

    return general_size_


def to_giga_bytes(bytes_q: int) -> int:
    return bytes_q // 1024 ** 3


path1 = 'D:\\Хранилище'

# s = get_info(path98)
# print(f'Gen size = {to_giga_bytes(s)} GIGA bytes')











































