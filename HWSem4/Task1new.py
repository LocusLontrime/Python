# Создать и заполнить файл случайными целыми значениями.
# Выполнить сортировку содержимого файла по возрастанию.

import random
import time
from functools import reduce

from Agrorithms.Sorts.Merge_sort import Merge
from Agrorithms.Sorts.QuickSort import Quick


def fill_in_random(quantity: int, abs_val: int):
    with open("number_4_task.txt", "w") as file:
        for i in range(random.randint(1, quantity)):
            file.write(str(random.randint(-abs_val, abs_val)) + '\n')


def sort():
    with open("number_4_task.txt", "r") as file:
        numbers_list_int = [int(x) for x in file.readlines()]
        print(f'initial numbers to be sorted: {numbers_list_int}')
        sorted_ints = Merge.merge_sort(numbers_list_int)
        print(f'sorted ones: {sorted_ints}')
    with open("number_4_task.txt", "w") as file:
        for num in sorted_ints:
            file.write(str(num) + '\n')


fill_in_random(25, 100)

sort()

array_to_be_merged = [99, 87, 5, 7, 17, 87, 4, 3, 2, 1, 11, 111, 1, 98, 989, 2, 3, 36, 366, 989, 1, 5, 55, 7, 989, 67, 78, 3, 54, 45, 35, 36, 73, 1, 11, 111, 1001, 971, 97, 99, 198, 999]


def get_array(length: int, abs_val: int) -> list:
    result_list = []
    for i in range(length):
        result_list.append(random.randint(-abs_val, abs_val))
    return result_list


# random array for speed-test
array_to_be_merged_new = get_array(1000000, 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)

# comparison of two sorts
tic = time.perf_counter()

sorted_sort = Merge.merge_sort(array_to_be_merged_new)
# print(sorted_sort)

toc1 = time.perf_counter()
print(f"Time elapsed for merged sort: {toc1 - tic:0.4f} seconds")

Quick.quick_sort(array_to_be_merged_new)
# print(array_to_be_merged)

toc2 = time.perf_counter()
print(f"Time elapsed for quick sort: {toc2 - toc1:0.4f} seconds")




