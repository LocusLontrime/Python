import math
import random
import sys
import time

from collections import defaultdict as d, Counter


sys.set_int_max_str_digits(1_000_000)


# idea:
# 1. keep forbidden intervals incrementing the index through the array...


def get_naive_subs_q(array: list[int]):
    length = len(array)

    # keeps forbidden intervals for the last odd and even occurrences of the every element:
    saved_intervals: dict[int, list[...]] = {}

    # keeps forbidden intervals' aggregated length at the every index i:
    forbiddances = {}

    # tracks occurrences of the every element in the array:
    occurrences = d(list[int])

    # current intervals structure (sorted in ascending order):
    curr_intervals = []

    for i, el in enumerate(array):

        # if the element occurs at the first time:
        if el not in occurrences.keys():
            saved_intervals[...] = ...
        # already occurred element:
        else:
            ...

        # updates tracker:
        occurrences[el] += [i]


def append_interval(intervals: list[tuple[int, int]], interval: tuple[int, int]):
    li, l_flag = bin_search_intervals(intervals, interval[0])
    ri, r_flag = bin_search_intervals(intervals, interval[1])

    print(f'{li, l_flag = }')
    print(f'{ri, r_flag = }')

    return intervals[: li] + [
        (
            intervals[li][0] if l_flag else interval[0],
            intervals[ri][1] if r_flag else interval[1]
        )
    ] + intervals[ri + 1 if r_flag else ri:]


def bin_search_intervals(intervals: list[tuple[int, int]], value: int) -> tuple[int, bool]:
    lb, rb = 0, len(intervals) - 1
    while lb <= rb:

        pivot_ind = (lb + rb) // 2

        print(f'{lb, rb = } | {pivot_ind = }')

        if intervals[pivot_ind][0] <= value <= intervals[pivot_ind][1]:
            return pivot_ind, True
        elif value < intervals[pivot_ind][0]:
            rb = pivot_ind - 1
        else:  # value > intervals[pivot_ind][1]:
            lb = pivot_ind + 1

    return lb, False


array_ = [2, 2, 2, 3]  # 7
array_1 = [2, 5, 2, 3, 6, 7, 8, 23, 23, 13, 65, 31, 3, 4, 3]  # 53
array_2 = [6, 1, 7, 4, 6, 7, 1, 4, 7, 1, 4, 6, 6, 7, 4, 1, 6, 4, 7, 1, 4, 5, 3, 2, 1, 6, 9]  # 114
array_3 = [1, 3, 1]
array_4 = [2, 1, 1, 1]

intervals_ = [(0, 1), (5, 7), (17, 28), (78, 81), (89, 98)]
interval_ = (11, 97)
value_ = 97  # 11

# res = bin_search_intervals(intervals_, value_)

# print(f'{res = }')

print(f'new intervals: {append_interval(intervals_, interval_)}')

k1 = pow(111_111, 111_111, 100000007)
k2 = pow(101_101, 101_101, 100000007)
print(f'processing the sum...')
k = 0
for i in range(10_000):
    k += k1 + k2
print(f'printing now...')                                                                       # 36 366 98 989 LL
print(f'{k = }')
