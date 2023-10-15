# accepted on codewars.com (what with runtime on codewars? 5-10x times higher...)
import math
import random
import time
from collections import defaultdict as d


tree_size: int
tree: list[tuple[int or float, int]]
postponed_update: list[int]
decompress_x: dict[int, int]
decompress_y: dict[int, int]


# Segment Tree
def initialize_tree(n: int):  # 36 36.6 98 989 LL
    global tree_size, tree, postponed_update
    p = 1
    while p < n:
        p *= 2
    tree_size = 2 * p
    tree = [(0, 0) for _ in range(tree_size)]
    postponed_update = [0 for _ in range(tree_size)]


def push(vert_ind: int) -> None:
    global tree, postponed_update
    if postponed_update[vert_ind] != 0:  # and vert_ind < p ???
        left_vert_ind = vert_ind << 1
        right_vert_ind = left_vert_ind + 1
        delta_ = postponed_update[vert_ind]
        # lazy propagation step:
        tree[left_vert_ind] = tree[left_vert_ind][0] + delta_, tree[left_vert_ind][1]
        postponed_update[left_vert_ind] += delta_
        tree[right_vert_ind] = tree[right_vert_ind][0] + delta_, tree[right_vert_ind][1]
        postponed_update[right_vert_ind] += delta_
        # nullifying used update info:
        postponed_update[vert_ind] = 0


def combine(a: tuple[int or float, int], b: tuple[int or float, int]) -> tuple[int or float, int]:
    if a[0] < b[0]:
        return a
    if b[0] < a[0]:
        return b
    # a[0] == b[0]:
    return a[0], a[1] + b[1]


def build(a: list[int], v: int, tl: int, tr: int):
    if tl == tr:
        # decompressing coords:
        tree[v] = a[tl], decompress_y[tl + 1] - decompress_y[tl]
    else:
        tm = (tl + tr) // 2
        new_l, new_r = v << 1, (v << 1) + 1
        build(a, new_l, tl, tm)
        build(a, new_r, tm + 1, tr)
        tree[v] = combine(tree[new_l], tree[new_r])


def get_min(v: int, tl: int, tr: int, left: int, right: int) -> tuple[int or float, int]:
    if left > right:
        return math.inf, 0
    if left == tl and right == tr:
        return tree[v]
    push(v)
    tm = (tl + tr) // 2
    return combine(
        get_min(v << 1, tl, tm, left, min(right, tm)),
        get_min(v << 1 + 1, tm + 1, tr, max(left, tm + 1), right)
    )


def update(v: int, tl: int, tr: int, left: int, right: int, delta: int) -> None:
    # not set, but increase
    if left > right:
        return
    if left == tl and right == tr:
        # update by adding a value to the segment:
        tree[v] = tree[v][0] + delta, tree[v][1]
        # lazy propagation:
        postponed_update[v] += delta
    else:
        push(v)  # lp next
        tm = (tl + tr) // 2
        new_l, new_r = v << 1, (v << 1) + 1
        update(new_l, tl, tm, left, min(right, tm), delta)
        update(new_r, tm + 1, tr, max(left, tm + 1), right, delta)
        tree[v] = combine(tree[new_l], tree[new_r])


def calculate(rectangles: list[tuple[int, int, int, int]]) -> int:
    area = 0
    if not rectangles:
        return area
    x_rect_pos_events, x_rect_neg_events, max_ys, max_xs, y_interval = compress_coords(rectangles)
    initialize_tree(max_ys)
    build([0] * max_ys, 1, 0, max_ys - 1)
    prev_x = 0
    for x in range(max_xs + 1):
        min_, freq = get_min(1, 0, max_ys - 1, 0, max_ys - 1)
        area += (y_interval - (0 if min_ else freq)) * (decompress_x[x] - decompress_x[prev_x])
        for yl, yr in x_rect_pos_events[x]:
            update(1, 0, max_ys - 1, yl, yr - 1, 1)
        for yl, yr in x_rect_neg_events[x]:
            update(1, 0, max_ys - 1, yl, yr - 1, -1)
        prev_x = x
    return area


def compress_coords(rectangles: list[tuple[int, int, int, int]]) -> tuple[d[int, list[tuple[int, int]]], d[int, list[tuple[int, int]]], int, int, int]:
    global decompress_x, decompress_y
    ys, xs = set(), set()
    for xl, yl, xr, yr in rectangles:
        xs |= {xl, xr}
        ys |= {yl, yr}
    decompress_y, decompress_x = {}, {}
    compress_y, compress_x = {}, {}
    for ind, x in enumerate(sorted(xs)):
        decompress_x[ind] = x
        compress_x[x] = ind
    for ind, y in enumerate(sorted_ys := sorted(ys)):
        decompress_y[ind] = y
        compress_y[y] = ind
    min_y, max_y = sorted_ys[0], sorted_ys[-1]
    x_rect_pos_events = d(list)
    x_rect_neg_events = d(list)
    # building events dicts:
    for xl, yl, xr, yr in rectangles:
        x_rect_pos_events[compress_x[xl]].append((compress_y[yl], compress_y[yr]))
        x_rect_neg_events[compress_x[xr]].append((compress_y[yl], compress_y[yr]))
    return x_rect_pos_events, x_rect_neg_events, len(ys) - 1, len(xs) - 1, max_y - min_y


# rects = [
#     (3, 3, 6, 5),
#     (4, 4, 6, 6),
#     (4, 3, 7, 5),
#     (4, 2, 8, 5),
#     (4, 3, 8, 6),
#     (9, 0, 11, 4),
#     (9, 1, 10, 6),
#     (9, 0, 12, 2),
#     (10, 1, 13, 5),
#     (12, 4, 15, 6),
#     (14, 1, 16, 5),
#     (12, 1, 17, 2)
# ]

# rects = [
#     (2, 4, 6, 6),
#     (4, 2, 10, 7),
#     (7, 3, 9, 6)
# ]

# rects = [
#     (1, 1, 7, 6),
#     (2, 2, 8, 7),
#     (3, 3, 9, 8),
#     (4, 4, 10, 9),
#     (5, 5, 11, 10)
# ]

# rects = [(0, i * 2, 9, i * 2 + 1) for i in range(5)] + [(i * 2, 0, i * 2 + 1, 9) for i in range(5)]

rects = [(random.randint(1, 1_000_000), random.randint(1, 1_000_000), random.randint(1, 1_000_000), random.randint(1, 1_000_000)) for _ in range(100_000)]

start = time.time_ns()
print(f'area: {calculate(rects)}')
finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')

# arr_ = [1, 1, 3, 3, 5, 17, 29, 98]
#
# initialize_tree(length := len(arr_))
# build(arr_, 1, 0, length - 1)
#
# print(f'segment tree: {tree}')
#
# print(f'old arr: ')
# for i_ in range(length):
#     print(f'{get_min(1, 0, length - 1, i_, i_)} ', end='')
# print()
#
# # print(f'min: {get_min(1, 0, length - 1, 0, 3)}')
#
# update(1, 0, length - 1, 0, length - 1, 2)
# update(1, 0, length - 1, 0, length - 1, 2)
# update(1, 0, length - 1, 0, length - 1, -2)
# update(1, 0, length - 1, 0, length - 1, -2)
#
#
# # print(f'min: {get_min(1, 0, length - 1, 0, 3)}')
#
# print(f'new arr: ')
# for i_ in range(length):
#     print(f'{get_min(1, 0, length - 1, i_, i_)} ', end='')
#
# print()
# # print(f'min: {get_min(1, 0, length - 1, 0, length - 1)}')
# # print(f'min: {get_min(1, 0, length - 1, 2, 4)}')
# print(f'segment tree: {tree}')
