import time
from random import random


def quick_sort(array: list[int]) -> None:
    rec_counter = 0
    length = len(array)
    recursive_quick_sort(array, 0, length - 1, rec_counter)
    print(f'Quick sort is finished, {rec_counter} steps done')


# the core of sorting method
def recursive_quick_sort(array: list[int], left_border: int, right_border: int, rec_counter) -> None:
    rec_counter += 1

    # border case of list of 1 element
    if left_border == right_border:
        return

    # at first, we define the pivotElement(median)
    pivot_element = (array[left_border] + array[right_border]) // 2

    # Hoare's Partition, here we're finding the pivotIndex
    pivot_index = hoare_partition(array, left_border, right_border, pivot_element)

    # recursive tree building, divide and conquer tactics
    recursive_quick_sort(array, left_border, pivot_index, rec_counter)
    recursive_quick_sort(array, pivot_index + 1, right_border, rec_counter)


# Hoare's partition part, auxiliary to main method
def hoare_partition(array: list[int], left_border: int, right_border: int, pivot_element: int) -> int:
    while True:
        # skipping the elements that stayed at their place on the left side
        while array[left_border] < pivot_element:
            left_border += 1
        # skipping the elements that stayed at their place on the right side
        while array[right_border] > pivot_element:
            right_border -= 1
        # we are swapping two elements if they are both stay at wrong places
        if left_border < right_border:
            array[left_border], array[right_border] = array[right_border], array[left_border]
            left_border += 1
            right_border -= 1
        else:
            return right_border


# simple variation of quick sort
def quick(data):
    less = []
    pivotList = []
    more = []
    if len(data) <= 1:
        return data
    else:
        pivot = data[0]
        for i in data:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
        less = quick(less)
        more = quick(more)
        return less + pivotList + more


arr = [1, 1, 0, 1, 0, 98, 989, 1, 1, 3, 36, 78, 11, 101, 98989]
quick_sort(arr)
print(arr)
arr = [1, 1, 0, 1, 0, 98, 989, 1, 1, 3, 36, 78, 11, 101, 98989]
print(quick(arr))

arr_x = [int(10000000 * random()) for _ in range(10000000 * 2)]

start = time.time_ns()
quick_sort(arr_x.copy())
finish = time.time_ns()
print(f'time elapsed Quick_sort: {(finish - start) // 10 ** 6} milliseconds')

start1 = time.time_ns()
quick(arr_x.copy())
finish1 = time.time_ns()
print(f'time elapsed Quick: {(finish1 - start1) // 10 ** 6} milliseconds')

# 10 ** 7 elements: quick -> 29892 ms, quick_sort: 27553 ms

