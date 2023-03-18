import time
from random import random, randint


# Task 1 (SORTING, HOARE):

rec_counter: int


# covering:
def quick_sort(array: list[int]) -> int:
    global rec_counter
    rec_counter = 0
    length = len(array)
    recursive_quick_sort(array, 0, length - 1)
    return rec_counter


# the core of sorting method:
def recursive_quick_sort(array: list[int], left_border: int, right_border: int) -> None:
    global rec_counter
    rec_counter += 1

    # border case:
    if left_border == right_border:
        return

    # median defining:
    pivot_element = (array[left_border] + array[right_border]) // 2

    # pivot index:
    pivot_index = hoare_partition(array, left_border, right_border, pivot_element)

    # recurrent relation:
    recursive_quick_sort(array, left_border, pivot_index)
    recursive_quick_sort(array, pivot_index + 1, right_border)


# Hoare's partition part:
def hoare_partition(array: list[int], left_border: int, right_border: int, pivot_element: int) -> int:
    while True:
        while array[left_border] < pivot_element:
            left_border += 1
        while array[right_border] > pivot_element:
            right_border -= 1
        # elements' with wrong placement swap:
        if left_border < right_border:
            array[left_border], array[right_border] = array[right_border], array[left_border]
            left_border += 1
            right_border -= 1
        else:
            return right_border


input_list = [randint(1, 1000000) for _ in range(1000000)]

start = time.time_ns()
its = quick_sort(input_list)
finish = time.time_ns()

print(f'{input_list} \n its: {its}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


# Task 2 (Three lists and a dict):

def func(names: list[str], salaries: list[int], cash_prizes: list[str]) -> dict[str, float]:
    if len({(l := len(names)), len(salaries), len(cash_prizes)}) != 1:
        raise ValueError(f'Lengths of all three lists must be the same!!!')
    return {names[i]: (salaries[i] * float(cash_prizes[i].split('%')[0]) / 100) for i in range(l)}


names_ = ['Vadik', 'Svetlana', 'Dmitry', 'Ivan', 'Roman']
salaries_ = [100000, 50000, 900000, 250000, 500000]
cash_prizes_ = ['10.25', '19.88', '125.98', '55.52', '101.88']

print(f'new dict: {func(names_, salaries_, cash_prizes_)}')



