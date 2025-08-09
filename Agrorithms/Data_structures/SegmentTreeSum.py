import math

tree_size: int
tree: list[int | float]
MAX_N: int


# Segment Tree
def initialize_tree(n: int):  # 36 36.6 98 989 LL
    global tree_size, tree, MAX_N
    # MAX_N = 100
    p = 1
    while p < n:
        p *= 2
    tree_size = 2 * p + 1
    tree = [0 for _ in range(tree_size)]


def build(arr: list[int], v: int, tl: int, tr: int):
    print(f'{tl, tr = }')
    if tl == tr:
        # we reach a leaf:
        tree[v] = arr[tl]
        print(f'{v = } | [{tl, tr}] -> {arr[tl]}')
    else:
        tm = (tl + tr) // 2
        new_l, new_r = v << 1, (v << 1) + 1
        build(arr, new_l, tl, tm)
        build(arr, new_r, tm + 1, tr)
        tree[v] = tree[new_l] + tree[new_r]


def sum_seg(v: int, tl: int, tr: int, left: int, right: int) -> int:
    print(f'{v} | {tl, tr = } | {left, right = }')
    if left > right:
        return 0
    if left == tl and right == tr:
        print(f'+++ {v = } | [{tl, tr}] -> {tree[v]}')
        return tree[v]
    # middle point:
    tm = (tl + tr) // 2
    # the sum of the queries on the children:
    return sum_seg(v << 1, tl, tm, left, min(right, tm)) + sum_seg((v << 1) + 1, tm + 1, tr, max(left, tm + 1), right)


def point_assignment(v: int, tl: int, tr: int, i: int, val: int):
    if tl == tr:
        tree[v] = val
    else:
        # middle point:
        tm = (tl + tr) // 2
        # descending to children:
        if i <= tm:
            point_assignment(v << 1, tl, tm, i, val)
        else:
            point_assignment((v << 1) + 1, tm + 1, tr, i, val)
        # new sum:
        tree[v] = tree[v << 1] + tree[(v << 1) + 1]


array = [1, 7, 2, 5, 4, 3, 6, 9, 0, 8]
initialize_tree(10)
build(array, 1, 0, len(array) - 1)

print(f'{tree = }')
print(f'{tree_size = }')

print(f'{sum(array) = }')                                                             # 36 366 98 989 98989 LL LL

print(f'{sum_seg(1, 0, len(array) - 1, 2, 5) = }')

point_assignment(1, 0, len(array) - 1, 9, 98)

print(f'{sum_seg(1, 0, len(array) - 1, 9, 9) = }')
print(f'{sum_seg(1, 0, len(array) - 1, 5, 9) = }')
