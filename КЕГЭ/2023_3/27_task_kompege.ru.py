# accepted on kompege.ru

# -*- coding: utf-8 -*-
# Пусть S -> последовательность из N целых чисел, пронумерованных подряд, начиная с 1. Обозначим за S(P,K) -> подпоследовательность,
# состоящую из не менее чем 2-х идущих подряд элементов, входящих в S, начиная с элемента с номером P и заканчивая элементом с номером K,
# где 0 < P < K. Определить две такие непересекающиеся подпоследовательности S(L, Q) и S(R, T),
# между которыми находится по крайней мере один элемент (т.е. Q < R - 1), чтобы сумма всех их элементов была максимальна.
# В ответе запишите абсолютное значение найденной максимальной суммы.


import math


# Входные данные:
# Дано два входных файла (A и B), каждый из которых в первой строке содержит число N (5 < N < 10_000_000) - количество целых чисел.
# Каждая из N следующих строчек содержит одно целое число, значение которого по модулю не превышает 1_000.
# В ответе укажите два числа: сначала значение искомой величины для файла A, затем для файла B.

def max_2subs_sum(sequence: list[int]):
    # array's length:
    n = len(sequence)
    # let us use slightly modified kadane's algo 2 times:
    max_sum, max_sum_start, max_sum_end = kadane(sequence)
    print(f'Max sum subsequence1 -> ({max_sum}) ::: {max_sum_start, max_sum_end = }')
    max_sum_1 = kadane(sequence[:max_sum_start - 1])[0] if max_sum_start > 0 else 0
    max_sum_2 = kadane(sequence[max_sum_end + 2:])[0] if max_sum_end + 2 < n else 0
    correction = kadane(sequence[max_sum_start: max_sum_end + 1], True)[0]
    k = min(sequence[max_sum_start: max_sum_end + 1])
    print(f'{k = }')
    print(f'-kadane -> {correction}, {max_sum_1, max_sum_2 = }')
    return max_sum + max(correction, max_sum_1, max_sum_2)


def kadane(sequence: list[int], neg=False) -> tuple[int, int, int]:
    # print(f'kadane seq: {sequence}')
    sum_ = 0
    i_start = 0
    max_sum = -math.inf
    max_sum_start, max_sum_end = -1, -1
    for i, el_ in enumerate(sequence):
        el = -el_ if neg else el_
        sum_ += el
        if sum_ > max_sum:
            if i - i_start > 0:
                max_sum = sum_
                max_sum_start = i_start
                max_sum_end = i
        if sum_ <= 0:
            sum_ = 0
            i_start = i + 1
            neg_sum = 0
            max_neg_curr = 0

    return max_sum, max_sum_start, max_sum_end


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(int, f.readlines()[1:])
        f.close()
    return list(arr_)


test_ex = [-1, 5, 3, -4, 2, -10]
file_A = get_arr('27_A_17644.txt')
file_B = get_arr('27_B_17644.txt')

print(f'A file res -> {max_2subs_sum(file_A)}')
print(f'B file res -> {max_2subs_sum(file_B)}')

print(f'{[98, 98989][0:]}')
