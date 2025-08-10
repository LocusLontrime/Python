# accepted on leetcode.com
import math


# There are several squares being dropped onto the X - axis of a 2D plane.

# You are given a 2D integer array positions where positions[i] = [left_i, sideLength_i] represents the i_th square
# with a side length of sideLength_i that is dropped with its left edge aligned with X-coordinate left_i.

# Each square is dropped one at a time from a height above any landed squares.
# It then falls downward(negative Y direction) until it either lands on the top side of another square or on the X - axis.
# A square brushing the left / right side of another square does not count as landing on it.
# Once it lands, it freezes in place and cannot be moved.

# After each square is dropped, you must record the height of the current tallest stackof squares.

# Return an integer array ans where ans[i] represents the height described above after dropping the ith square.

# Example 1:
# Input: positions = [[1, 2], [2, 3], [6, 1]]
# Output: [2, 5, 5]
# Explanation: After the first drop, the tallest stack is square 1 with a height of 2.
# After the second drop, the tallest stack is squares 1 and 2 with a height of 5.
# After the third drop, the tallest stack is still squares 1 and 2 with a height of 5.
# Thus, we return an answer of [2, 5, 5].

# Example 2:
# Input: positions = [[100, 100], [200, 100]]
# Output: [100, 100]
# Explanation: After the first drop, the tallest stack is square 1 with a height of 100.
# After the second drop, the tallest stack is either square 1 or square 2, both with heights of 100.
# Thus, we return an answer of [100, 100].
# Note that square 2 only brushes the right side of square 1, which does not count as landing on it.

# Constraints:
# 1 <= positions.length <= 1000
# 1 <= lefti <= 10 ** 8
# 1 <= sideLengthi <= 10 ** 6


tree_size: int
tree: list[int | float]
postponed_update: list[int]


# O(n^2) with coords compressing (should be optimized by using a max segment tree with lazy propagation)
def falling_squares(positions: list[list[int]]) -> list[int]:
    # 1. coordinates compressing:
    coords = set()
    for li, side in positions:
        coords |= {li, li + side - 1}
    compress = {el: i for i, el in enumerate(sorted(coords))}
    n = len(compress)
    # 2. the main part of finding the max heights at the every square's falling:
    heights = [0 for _ in range(n)]
    max_height = 0
    ans = []
    for li, side in positions:
        max_h_under = max(heights[compress[li]: compress[li + side - 1] + 1])
        for i in range(compress[li], compress[li + side - 1] + 1):
            heights[i] = max_h_under + side
        max_height = max(max_height, max_h_under + side)
        ans += [max_height]
    return ans


# O(n * log(n)) with MaxSegmentTree and coords compressing:
def falling_squares_fast(positions: list[list[int]]) -> list[int]:
    # 1. coordinates compressing:
    coords = set()
    for li, side in positions:
        coords |= {li, li + side - 1}
    compress = {el: i for i, el in enumerate(sorted(coords))}
    n = len(compress)
    # 2. the main part of finding the max heights at the every square's falling:
    heights = [0 for _ in range(n)]
    initialize_tree(n)
    build(heights, 1, 0, n - 1)
    max_height = 0
    ans = []
    for li, side in positions:
        max_h_under = get_max(1, 0, n - 1, compress[li], compress[li + side - 1])  # max(heights[compress[li]: compress[li + side - 1] + 1])
        update(1, 0, n - 1, compress[li], compress[li + side - 1], max_h_under + side)
        # for i in range(compress[li], compress[li + side - 1] + 1):
        #     heights[i] = max_h_under + side
        max_height = max(max_height, max_h_under + side)
        ans += [max_height]
    return ans


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
        tree[v] = max(tree[new_l], tree[new_r])


def get_max(v: int, tl: int, tr: int, left: int, right: int) -> int or float:
    if left > right:
        return -math.inf
    if left == tl and right == tr:
        return tree[v]
    # apply the pending updates if any:
    if postponed_update[v]:
        push(v)
    # middle point:
    tm = (tl + tr) // 2
    # the minimum of the queries on the children:
    return max(
        get_max(v << 1, tl, tm, left, min(right, tm)),
        get_max((v << 1) + 1, tm + 1, tr, max(left, tm + 1), right)
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
        tree[v] = max(tree[new_l], tree[new_r])


test_ex = [
    [1, 2],
    [2, 3],
    [6, 1]
]

test_ex_1 = [
    [100, 100],
    [200, 100]
]

print(f'test ex res -> {falling_squares_fast(test_ex)}')                                   # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {falling_squares_fast(test_ex_1)}')
