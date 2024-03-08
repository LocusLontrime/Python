import math
import random
import sys
import time

from collections import defaultdict as d, Counter

length: int  # = 98
arr: list[int]  # = [1, 1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 7]  # 36 366 98 989 LL
s_tree_l: int  # <= 4 * length (can be defined more carefully -> in algo)
min_tree: list[tuple[int, int]]  # = [(0, 0) for _ in range(s_tree_l)]
postponed_update: list[int]
p: int


# idea:
# 1. odd 1s -> killed (in all scenarios)
# 2. even 1s -> revived (only if evens == 1)
# 3. need to calculate evens at the every step...


def get_naive_subs_q(array: list[int]):
    global length, arr, s_tree_l, min_tree, postponed_update, p

    length = len(array)
    p = 1
    while p < length:
        p *= 2
    s_tree_l = 2 * p

    print(f'{length = }')
    print(f'{s_tree_l = }')
    print(f'{p = }')

    min_tree = [(math.inf, 0) for _ in range(s_tree_l)]
    postponed_update = [0 for _ in range(s_tree_l)]
    arr = [0 for _ in range(len(array))]
    build()

    # print(f'{arr = }')
    # print(f'{array = }')
    # print(f'{min_tree = }')

    valid_ones_q = 0

    # tracks occurrences of the every element in the array:
    occurrences = d(list[int])

    for i, el in enumerate(array):

        print(f'{i} ---> {el}, occs = {len(occurrences[el])}:')

        # updates evens:
        lb, rb = -1, -1
        for ind, i_ in enumerate(occurrences[el]):
            i_occs_to_right = len(occurrences[el]) - ind + 1  # <--- new element 'el' included
            # indices walking:
            lb, rb = rb + 1, i_
            # print(f'...{lb, rb, i_occs_to_right = }')
            if i_occs_to_right % 2 == 0:
                # evens incrementing:
                range_update(lb, rb, addition=1)
            else:
                # evens decrementing:
                range_update(lb, rb, addition=-1)

        # updates invalid ones counter:
        min_, min_q = get_min(0, i)

        if min_ == 0:
            valid_ones_q += min_q

        # updates tracker:
        occurrences[el] += [i]

        # print(f'...{min_tree = }')
        # get_array()
        print(f'-->{valid_ones_q = } ~ zeroes={min_q} | non_zeroes={i + 1 - min_q}')

    # all_subs_q = length * (length + 1) // 2

    # print(f'{all_subs_q, valid_ones_q = }')

    return valid_ones_q


# Segment max tree: (need to be min for correct algo work!)
def combine(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    if t1[0] < t2[0]:
        return t1
    if t2[0] < t1[0]:
        return t2
    return t1[0], t1[1] + t2[1]


def update(vert_ind: int):
    global postponed_update, min_tree
    if postponed_update[vert_ind] != 0 and vert_ind < p:  # postponed_update[vert_ind][0] != 0 and
        # print(f'!!!!!!!!!!!!postponed update: {vert_ind}')
        left_vert_ind = vert_ind << 1
        right_vert_ind = left_vert_ind + 1

        addition = postponed_update[vert_ind]

        min_tree[left_vert_ind] = min_tree[left_vert_ind][0] + addition, min_tree[left_vert_ind][1]
        min_tree[right_vert_ind] = min_tree[right_vert_ind][0] + addition, min_tree[right_vert_ind][1]

        postponed_update[left_vert_ind] += addition
        postponed_update[right_vert_ind] += addition

        postponed_update[vert_ind] = 0


def build():
    def build_(vert_ind: int, left_: int, right_: int) -> None:
        # border case:
        if left_ == right_:
            min_tree[vert_ind] = arr[left_], 1
        # recurrent relation:
        else:
            middle = (left_ + right_) // 2
            i_ = vert_ind << 1
            build_(i_, left_, middle)
            build_(i_ + 1, middle + 1, right_)
            min_tree[vert_ind] = combine(min_tree[i_], min_tree[i_ + 1])

    build_(1, 0, length - 1)


def get_min(ql: int, qr: int) -> tuple[int, int]:
    def get_min_(vert_ind: int, left_: int, right_: int, ql_: int, qr_: int) -> tuple[int, int]:
        # print(f'left_, right_: {left_, right_}, ql_, qr_: {ql_, qr_}')
        # border cases:
        if ql_ > qr_:
            return math.inf, 0
        if (left_, right_) == (ql_, qr_):
            return min_tree[vert_ind]
        update(vert_ind)
        # recurrent relation:
        middle = (left_ + right_) // 2
        i_ = vert_ind << 1
        return combine(
            get_min_(i_, left_, middle, ql_, min(qr_, middle)),
            get_min_(i_ + 1, middle + 1, right_, max(ql_, middle + 1), qr_)
        )

    return get_min_(1, 0, length - 1, ql, qr)


def range_update(ql: int, qr: int, addition: int):
    def range_update_(vert_ind: int, left_: int, right_: int, ql_: int, qr_: int) -> None:
        # print(f'{counter}. left_, right_: {left_, right_}, ql_, qr_: {ql_, qr_}')
        # border cases:
        if ql_ > qr_:
            return
        if (left_, right_) == (ql_, qr_):
            min_tree[vert_ind] = min_tree[vert_ind][0] + addition, min_tree[vert_ind][1]  # 36.6 98
            postponed_update[vert_ind] += addition
            return
        update(vert_ind)
        # recurrent relation:
        middle = (left_ + right_) // 2
        i_ = vert_ind << 1
        range_update_(i_, left_, middle, ql_, min(qr_, middle))
        range_update_(i_ + 1, middle + 1, right_, max(middle + 1, ql_), qr_)
        min_tree[vert_ind] = combine(min_tree[i_], min_tree[i_ + 1])

    range_update_(1, 0, length - 1, ql, qr)


def get_array():
    print(f'-->evens: ', end='')
    print(f'{[get_min(i, i)[0] for i in range(length)]}')


array_ = [2, 2, 2, 3]  # 7
array_1 = [2, 5, 2, 3, 6, 7, 8, 23, 23, 13, 65, 31, 3, 4, 3]  # 53
array_2 = [6, 1, 7, 4, 6, 7, 1, 4, 7, 1, 4, 6, 6, 7, 4, 1, 6, 4, 7, 1, 4, 5, 3, 2, 1, 6, 9]  # 114
array_3 = [1, 3, 1]
array_4 = [2, 1, 1, 1]

array_n_1000 = []  # ans: 128261

with open("C:\\Users\\langr\\PycharmProjects\\AmberCode\\CodeWars_Rush\\_2kyu\\to_be_solved\\NaiveNums.txt") as f:
    for line in f:
        array_n_1000 += [int(x) for x in line.split(', ')]

array_n_19999 = []  # ans: 7868590

with open("C:\\Users\\langr\\PycharmProjects\\AmberCode\\CodeWars_Rush\\_2kyu\\to_be_solved\\MiniNums.txt") as f:
    for line in f:
        array_n_19999 += [int(x) for x in line.split(', ')]

array_n_100000 = []  # ans: 8492097 (tests performance, many //####''frequently-repeating numbers)

with open("C:\\Users\\langr\\PycharmProjects\\AmberCode\\CodeWars_Rush\\_2kyu\\to_be_solved\\Numbers.txt") as f:
    for line in f:
        array_n_100000 += [int(x) for x in line.split(', ')]

q = 0

array_x = [5, 7, 5, 1, 2, 1, 3, 3, 1, 7, 1]

array_z = [2 if i % 2 else 1 for i in range(100_000)]

start = time.time_ns()
print(f'SIZE: {len(set(array_n_100000))}')
# print(f'{Counter(array_x)}')
res = get_naive_subs_q(array_n_100000)
finish = time.time_ns()

print(f'{res = }')

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
