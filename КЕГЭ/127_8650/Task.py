# accepted on kompege.ru

# -*- coding: utf-8 -*-
# На вход программе подается последовательность из N натуральных чисел.
# Рассматриваются все её непрерывные подпоследовательности длиной не менее K, в которых количество чётных и нечётных чисел совпадает.
# Найдите количество подходящих подпоследовательностей.

# Входные данные.
# Даны два входных файла (файл A и файл B), содержит в первой строке число N (1 ≤ N ≤ 10 000 000) – количество чисел в последовательности,
# а во второй строке число K - наименьшую длину рассматриваемых подпоследовательностей.
# Каждая из следующих N строк содержит одно натуральное число, не превышающее 100 000.

# Выходные данные:
# одно число – количество подпоследовательностей длиной не менее K, в которых количество чётных и нечётных чисел совпадает.

# Пример входного файла:

# 7, 2, [6, 15, 63, 77, 30, 51, 22]
# В этой последовательности подходят подпоследовательности [6, 15]; [77, 30]; [30, 51]; [51, 22] и [77, 30, 51, 22].

# Ответ для примера: 5.
from collections import defaultdict as def_dict


def subseqs_longer_than_k(k: int, array: list[int]):
    # array's length:
    n = len(array)
    # even - odds prefix array:
    prefix_array = [0 for i in range(n + 1)]
    for i, el in enumerate(array):
        # an odd one:
        prefix_array[i + 1] = prefix_array[i] + (- 1 if el % 2 else 1)
    # print(f'{prefix_array = }')
    # the core algo:
    even_odd_diff_visited = def_dict(int)
    res = 0
    for i, el in enumerate(prefix_array):
        if i + k - 1 < n:
            even_odd_diff_visited[el] += 1
            res += (delta := even_odd_diff_visited[prefix_array[i + k]])
            # print(f'{i} -> {el} :: delta -> {delta}')
    return res


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(int, f.readlines()[2:])
        f.close()
    arr_ = list(arr_)
    return arr_


test_ex = 2, [6, 15, 63, 77, 30, 51, 22]
arr_A = get_arr(f'27A_8650.txt')
arr_B = get_arr(f'27B_8650.txt')

print(f'test ex -> {subseqs_longer_than_k(*test_ex)}')                                # 36 366 98 989 98989 LL
print(f'file A -> {subseqs_longer_than_k(100, arr_A)}')
print(f'file B -> {subseqs_longer_than_k(1_000_000, arr_B)}')
