import math

tree_size: int
tree: list[int | float]
postponed_update: list[int]


# Segment Tree
def initialize_tree(n: int):  # 36 36.6 98 989 LL
    global tree_size, tree, postponed_update
    p = 1
    while p < n:
        p *= 2
    tree_size = 2 * p
    tree = [0 for _ in range(tree_size)]
    postponed_update = [0 for _ in range(tree_size)]


def push(vert_ind: int) -> None:
    # vert_ind < p ???
    left_vert_ind = vert_ind << 1
    right_vert_ind = left_vert_ind + 1
    delta_ = postponed_update[vert_ind]
    # lazy propagation step:
    tree[left_vert_ind] = delta_
    tree[right_vert_ind] = delta_
    postponed_update[left_vert_ind] = delta_
    postponed_update[right_vert_ind] = delta_
    # nullifying used update info:
    postponed_update[vert_ind] = 0


def build(array: list[int], v: int, tl: int, tr: int):
    if tl == tr:
        # assignment:
        tree[v] = array[tl]
    else:
        tm = (tl + tr) // 2
        new_l, new_r = v << 1, (v << 1) + 1
        build(array, new_l, tl, tm)
        build(array, new_r, tm + 1, tr)
        tree[v] = min(tree[new_l], tree[new_r])


def get_min(v: int, tl: int, tr: int, left: int, right: int) -> int or float:
    if left > right:
        return math.inf
    if left == tl and right == tr:
        return tree[v]
    # apply the pending updates if any:
    if postponed_update[v]:
        push(v)
    # middle point:
    tm = (tl + tr) // 2
    # the minimum of the queries on the children:
    return min(
        get_min(v << 1, tl, tm, left, min(right, tm)),
        get_min((v << 1) + 1, tm + 1, tr, max(left, tm + 1), right)
    )


def update(v: int, tl: int, tr: int, left: int, right: int, delta: int) -> None:
    # set, not increase
    if left > right:
        return
    if left == tl and right == tr:
        # update by adding a value to the segment:
        tree[v] = delta
        # lazy propagation:
        postponed_update[v] = delta
    else:
        # here we apply pending updates if any:
        if postponed_update[v]:
            push(v)
        tm = (tl + tr) // 2
        new_l, new_r = v << 1, (v << 1) + 1
        update(new_l, tl, tm, left, min(right, tm), delta)
        update(new_r, tm + 1, tr, max(left, tm + 1), right, delta)
        tree[v] = min(tree[new_l], tree[new_r])


m = 10
array = [0 for _ in range(m)]

initialize_tree(m)
build(array, 1, 0, m - 1)                                                             # 36 366 98 989 98989 LL
update(1, 0, m - 1, 4, 8, -9)

print(f'{tree = }')
print(f'{tree_size = }')
print(f'{postponed_update = }')

min_ = get_min(1, 0, m - 1, 4, 4)
print(f'{min_ = }')

