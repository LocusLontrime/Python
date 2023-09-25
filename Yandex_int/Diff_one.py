# The Task: Count all the good subarrays of the array given.
# Subarray is good if
# 1. length is greater than 1;
# 2. leftmost element equals min el
# 3. rightmost element equals max el

# Notes:
# all estimations based on the worst case...
# 1. Bruteforce -->> runtime: O(n^3), additional memory: O(1)
# 2. Accurate BruteForce -->> runtime: O(n^2), additional memory: O(1)
# 3. Divide and Conquer -->> runtime: O(n * log^2(n)), additional memory: O(n)

import random
import time
from bisect import bisect_left


# O(n^3)
def i_am_brute(arr: list[int]) -> int:
    counter = 0
    for j in range(length := len(arr)):
        for i in range(j + 1, length):
            subarray = arr[j: i + 1]
            if arr[j] <= min(subarray) and max(subarray) <= arr[i]:
                counter += 1
                # print(f'{counter}th good subarray: {subarray}')
    return counter


# O(n^2)
def i_am_accurate_brute(arr: list[int]) -> int:
    counter = 0
    for j in range(length := len(arr)):
        min_ = max_ = aj = arr[j]
        i = j + 1
        while i < length and min_ >= aj:
            min_ = min(min_, ai := arr[i])
            max_ = max(max_, ai)
            if max_ <= ai:
                # print(f'{counter}th good subarray: {arr[j: i + 1]}')
                counter += 1
            i += 1
    return counter


# O(n*log^2(n))
def divide_and_conquer(arr: list[int], left: int, right: int) -> int:
    # border case:
    if left == right:
        return 0
    # pivot index of array:
    pivot_index = (left + right) // 2
    lp, rp = pivot_index, pivot_index + 1
    # recurrent relation:
    counter = divide_and_conquer(arr, left, pivot_index) + divide_and_conquer(arr, pivot_index + 1, right)
    # building three auxiliary arrays (1 left and 2 right) of current (min/max)s:
    left_arr_mins, left_arr_maxes, right_arr_mins, right_arr_maxes = [], [], [], []
    get_mins_maxes(arr, left_arr_mins, left_arr_maxes, lp, left, -1)
    get_mins_maxes(arr, right_arr_mins, right_arr_maxes, rp, right, 1)
    # reversing the right_arr_mins arr for the correct bin_search:
    right_arr_mins = right_arr_mins[::-1]  # has almost no impact on algo's performance!
    # processing arrays with bisect:
    for min_left_, max_left_ in zip(left_arr_mins, left_arr_maxes):
        bisect_l = bisect_left(right_arr_maxes, max_left_)
        bisect_r = len(right_arr_mins) - bisect_left(right_arr_mins, min_left_)
        delta = bisect_r - bisect_l
        # incrementing the counter if possible:
        if delta > 0:
            counter += delta
    return counter


def get_mins_maxes(arr: list[int], mins: list[int], maxes: list[int], start: int, end: int, delta: int) -> None:
    min_ = max_ = arr[start]
    for i in range(start, end + delta, delta):
        min_ = min(min_, arr[i])
        max_ = max(max_, arr[i])
        if arr[i] == (min_ if delta == -1 else max_):
            mins.append(min_)
            maxes.append(max_)


arr_ex = [2, 3, 15, 3, 4, 3, 6, 7, 11, 13, 12, 7, 1, 2, 6, 3, 5, 15, 5, 7, 6, 5, 4, 3, 2, 4, 3, 6, 9, 1, 7, 2, 4, 3, 2, 6, 3, 7, 17, 1, 15, 2, 1, 4, 3, 6, 16, 2]  # [1, 2, 6, 3, 5, 5, 7, 6, 5, 4, 3, 2, 4, 3, 6, 9, 1, 7, 2, 4, 3, 2, 6, 3] -->> 23  # 1, 2, 3, 6
arr_big = [random.randint(1, 100 + 1) for _ in range(1_000_000)]

start1 = time.time_ns()
# print(f'i_am_brute: {i_am_brute(arr_big)}')
start2 = time.time_ns()
# print(f'i_am_accurate_brute: {i_am_accurate_brute(arr_big)}')
start3 = time.time_ns()
print(f'divide_and_conquer: {divide_and_conquer(arr_big, 0, len(arr_big) - 1)}')
finish = time.time_ns()

print(f'time elapsed brut: {(start2 - start1) // 10 ** 6} milliseconds')
print(f'time elapsed accurate brut: {(start3 - start2) // 10 ** 6} milliseconds')
print(f'time elapsed divide and conquer: {(finish - start3) // 10 ** 6} milliseconds')

# array = [1, 2, 2, 2, 2, 6, 7, 89, 90, 98, 989]
# n = 2
# print(f'bisect_left({n}): {bisect_left(array, n)}')
