# accepted on kompege.ru

# -*- coding: utf-8 -*-
# Задание 127 (№1869).
#
# На вход программы поступает последовательность из целых положительных чисел.
# Необходимо выбрать такую подпоследовательность подряд идущих чисел, чтобы их сумма
# была максимальной и делилась на 89, а также её длину. Если таких подпоследовательностей
# несколько, выбрать такую, у которой длина меньше.
#
# Входные данные. Даны два входных файла (файл А и файл В), каждый из которых содержит в
#
# первой строке количество чисел М (2 < №< 108). В каждой из последующих М строк записано
# одно целое положительное число, не превышающее 10000. Программа должна вывести
# длину найденной последовательности.
#
# Пример организации исходных данных во входном файле:
#
# 2, 3, 4, 93, 42, 34, 5, 95
#
# Для делителя 50 при указанных входных данных значением искомой суммы должно быть
# число 100 (3+4+93 или 5+95). Следовательно, ответ на задачу - 2. В ответе укажите два числа:
# ‘сначала длину искомой подпоследовательности для файла А, затем для файла В.

def max_sum_shortest_subseq(array: list[int]):
    MODULO = 89
    data = [[0, 0, 0, 0] for i in range(MODULO)]  # i_start, i_end, sum_start, subseq_sum
    sum_ = 0
    for i, el in enumerate(array):
        sum_ += el
        if data[sum_ % MODULO][2]:
            data[sum_ % MODULO][1] = i
            data[sum_ % MODULO][3] = sum_ - data[sum_ % MODULO][2]
        else:
            data[sum_ % MODULO][0] = i
            data[sum_ % MODULO][2] = sum_
    return -sort_key(sorted(data, key=sort_key, reverse=True)[0])[1]


def sort_key(element: list[int]):
    return element[3], element[0] - element[1]


def func(x: str) -> int:
    return int(x.strip())


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(func, f.readlines()[1:])
        f.close()
    arr_ = list(arr_)
    return arr_


test_ex = [2, 3, 4, 93, 42, 34, 5, 95]  # MODULO = 50

arr_A = get_arr(f'27_A_1869.txt')
arr_B = get_arr(f'27_B_1869.txt')

# print(f'res test -> {max_sum_shortest_subseq(test_ex)}')
print(f'res file A -> {max_sum_shortest_subseq(arr_A)}')
print(f'res file B -> {max_sum_shortest_subseq(arr_B)}')                              # 36 366 98 989 98989 LL



