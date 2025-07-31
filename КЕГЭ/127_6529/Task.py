# accepted on kompege.ru

# -*- coding: utf-8 -*-
# Ежедневно почтальон разносит корреспонденцию по домам.
# Его сумка вмещает не более M килограмм корреспонденции.
# Определите максимальное количество домов, расположенных друг за другом (непрерывная подпоследовательность),
# которое ему удастся обойти. В ответ укажите количество домов.

# Входные данные:

# Дано два входных файла (файл А и файл В),
# каждый из которых в первой строке содержит два числа:
# N (1 ⩽ N ⩽ 10 000 000) - общее количество домов и M (1 ⩽ M ⩽ 100 000 000) – максимальный вес корреспонденции,
# который может унести с собой почтальон. В каждой из следующих N строк находится число – масса корреспонденции,
# которую нужно доставить в дом (все числа натуральные, значение показания не превышает 3000).

# Пример входного файла:
# 10, [1, 3, 5, 3, 6, 5, 8]

# Будем искать такую максимальную длину подпоследовательности, при которой возможно получить максимальную сумму,
# меньшую или равную 10. 1+3+5=9 – максимальная масса (килограммы), которую удастся получить,
# чтобы почтальон смог унести её. Следовательно, ответ: 3.


def longest_subseq(m: int, array: list[int]):
    # let us use "sliding window" approach:
    sliding_window_sum = 0
    curr_subseq_length = 0
    max_subseq_length = 0
    left_border = 0
    for i, el in enumerate(array):
        sliding_window_sum += el
        curr_subseq_length += 1
        if sliding_window_sum <= m:
            max_subseq_length = max(max_subseq_length, curr_subseq_length)
        else:
            while sliding_window_sum > m:
                sliding_window_sum -= array[left_border]
                left_border += 1
                curr_subseq_length -= 1
    return max_subseq_length


def longest_subseq_circular_case(m: int, array: list[int]):
    # array's length:
    n = len(array)
    # let us use "sliding window" approach:
    sliding_window_sum = 0
    curr_subseq_length = 0  # should always be not greater than n
    max_subseq_length = 0
    left_border = 0  # now can exceed n - 1 -> we should use left_border % n to stay within the array's borders
    for i in range(2 * n - 1):
        sliding_window_sum += array[i % n]
        curr_subseq_length += 1
        if sliding_window_sum <= m:
            max_subseq_length = max(max_subseq_length, curr_subseq_length)
        else:
            while sliding_window_sum > m:
                sliding_window_sum -= array[left_border]
                left_border = (left_border + 1) % n
                curr_subseq_length -= 1
    return max_subseq_length


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(int, f.readlines()[1:])
        f.close()
    arr_ = list(arr_)
    return arr_


test_ex = 10, [1, 3, 5, 3, 6, 5, 8, 2, 1, 1]
arr_A = get_arr(f'27A_6529.txt')
arr_B = get_arr(f'27B_6529.txt')

print(f'test ex -> {longest_subseq(*test_ex)}')                                       # 36 366 98 989 98989 LL
print(f'file A -> {longest_subseq(400_000, arr_A)}')
print(f'file B -> {longest_subseq(36_000_000, arr_B)}')

# print(f'{-1 % 98}')

print(f'test ex circular -> {longest_subseq_circular_case(*test_ex)}')
print(f'file A circular -> {longest_subseq_circular_case(400_000, arr_A)}')
print(f'file B circular -> {longest_subseq_circular_case(36_000_000, arr_B)}')


