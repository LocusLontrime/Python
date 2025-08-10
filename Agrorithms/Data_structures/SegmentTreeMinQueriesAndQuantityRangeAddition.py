import math

tree_size: int
tree: list[tuple[int or float, int]]
postponed_update: list[int]


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
        tree[v] = a[tl], 1
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
    # applies the pending updates if any:
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
        # applies the pending updates if any:
        push(v)  # lp next
        tm = (tl + tr) // 2
        new_l, new_r = v << 1, (v << 1) + 1
        update(new_l, tl, tm, left, min(right, tm), delta)
        update(new_r, tm + 1, tr, max(left, tm + 1), right, delta)
        tree[v] = combine(tree[new_l], tree[new_r])                                   # 36 366 98 989 98989 LL LL
