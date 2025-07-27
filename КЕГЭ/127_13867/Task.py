# accepted on kompege.ru
# -*- coding: utf-8 -*-
# На вход программе подается последовательность из N целых чисел.
# Рассматриваются все её непрерывные подпоследовательности с нулевой суммой элементов,
# содержащие в совокупной записи своих чисел все десятичные цифры. Найдите количество подходящих подпоследовательностей.

# Входные данные. Даны два входных файла (файл A и файл B),
# каждый из которых содержит в первой строке число N (1 ≤ N ≤ 10 000 000) – количество чисел в последовательности.
# Каждая из следующих N строк содержит одно целое число, по модулю не превышающее 100.

# В ответе укажите два числа: сначала искомое значение для файла А, затем для файла B.

# Пример входного файла:

# 10, 36, -36, -9, 15, 25, -7, 30, 14, -68, -9

# При таких исходных данных подходят три подпоследовательности:
# [-9, 15, 25, -7, 30, 14, -68], [15, 25, -7, 30, 14, -68, -9] и [36, -36, -9, 15, 25, -7, 30, 14, -68].
# Подпоследовательность [36, -36] не подходит, поскольку совокупная запись всех её чисел содержит только цифры 3 и 6.
from collections import defaultdict as def_dict


def count_subseqs(array: list[int]):
    # array's length:
    n = len(array)
    # the core algo:
    dig_dict = def_dict(int)
    shifts = def_dict(list)
    element_to_shift_ind = n - 1
    for i in range(n - 1, -1, -1):
        el = array[i]
        new_digs = get_digs(el)
        for dig, quantity in new_digs.items():
            dig_dict[dig] += quantity
        # all digits are done:
        while len(dig_dict) == 10:
            shifts[i] += [element_to_shift_ind]
            # dig_dict's change:
            digs_to_be_removed = get_digs(array[element_to_shift_ind])
            for dig, quantity in digs_to_be_removed.items():
                dig_dict[dig] -= quantity
                if dig_dict[dig] == 0:
                    del dig_dict[dig]
            # let us move to the next left element:
            element_to_shift_ind -= 1
    # prefix sums building:
    prefix_sums = [0 for i in range(n + 1)]
    for i, el in enumerate(array):
        prefix_sums[i + 1] = prefix_sums[i] + el
    # memoized sums building:
    res = 0
    memoized_sums = def_dict(int)
    for i, el in enumerate(prefix_sums):
        if i - 1 in shifts.keys():
            for ind in shifts[i - 1]:
                delta = memoized_sums[prefix_sums[ind + 1]]
                res += delta
        memoized_sums[el] += 1
    return res


def get_digs(num: int) -> dict:
    num_ = abs(num)
    dig_dict = {}
    num_str = f'{num_}'
    for char in num_str:
        el = int(char)
        if el in dig_dict.keys():
            dig_dict[el] += 1
        else:
            dig_dict[el] = 1
    return dig_dict


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(int, f.readlines()[1:])
        f.close()
    arr_ = list(arr_)
    return arr_


test_ex = [36, -36, -9, 15, 25, -7, 30, 14, -68, -9]  # [1234567890, -1234567890, 789, 89, 9, 1, 98]
arr_A = get_arr(f'27A_13867.txt')
arr_B = get_arr(f'27B_13867.txt')
print(f'test ex -> {count_subseqs(test_ex)}')                                         # 36 366 98 989 98989 LL
print(f'file A -> {count_subseqs(arr_A)}')
print(f'file B -> {count_subseqs(arr_B)}')


