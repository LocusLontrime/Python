# accepted on coderun
import random
import sys
import time

length: int  # = 98
arr: list[int]  # = [1, 1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 7]
s_tree_l: int  # = 4 * length
max_tree: list[tuple[int, int]]  # = [(0, 0) for _ in range(s_tree_l)]
postponed_update: list[tuple[int, int]]
p: int


def process_queries():
    global length, arr, s_tree_l, max_tree, postponed_update, p
    n, m, q, chunks_on_servers, queries = get_pars()
    # print(f'chunks_on_servers: {chunks_on_servers}')
    length = n
    p = 1
    while p < length:
        p *= 2
    s_tree_l = 2 * p
    arr = chunks_on_servers
    max_tree = [(0, 0) for _ in range(s_tree_l)]
    postponed_update = [(0, 0) for _ in range(s_tree_l)]
    build()
    # print(f'max_tree: {max_tree}')
    # main cycle:
    for s_out, s_in, left, right in queries:
        # max queries:
        max_, max_q = get_max(left - 1, right - 1)                                    # 36.6 98
        # print(f'max_, max_q: {max_, max_q}')
        if max_ == s_out and max_q == right - left + 1:
            # updates:
            range_update(left - 1, right - 1, s_in)
            print(f'1')
        else:
            print(f'0')


def get_pars():
    n, m, q = map(int, input().split(' '))
    chunks_on_servers = list(map(int, input().split(' ')))
    queries = [map(int, input().split(' ')) for _ in range(q)]
    return n, m, q, chunks_on_servers, queries


def combine(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    if t1[0] > t2[0]:
        return t1
    if t2[0] > t1[0]:
        return t2
    return t1[0], t1[1] + t2[1]


def update(vert_ind: int):
    global postponed_update, max_tree
    if postponed_update[vert_ind][0] != 0 and vert_ind < p:
        print(f'postponed update: {vert_ind}')
        left_vert_ind = vert_ind << 1
        right_vert_ind = left_vert_ind + 1
        max_, max_q_ = postponed_update[vert_ind]
        max_tree[left_vert_ind] = max_, (max_q_ + 1) // 2
        max_tree[right_vert_ind] = max_, max_q_ // 2
        postponed_update[left_vert_ind] = max_, (max_q_ + 1) // 2
        postponed_update[right_vert_ind] = max_,  max_q_ // 2
        postponed_update[vert_ind] = (0, 0)


def build():
    def build_(vert_ind: int, left_: int, right_: int) -> None:
        # border case:
        if left_ == right_:
            max_tree[vert_ind] = arr[left_], 1
        # recurrent relation:
        else:
            middle = (left_ + right_) // 2
            i_ = vert_ind << 1
            build_(i_, left_, middle)
            build_(i_ + 1, middle + 1, right_)
            max_tree[vert_ind] = combine(max_tree[i_], max_tree[i_ + 1])

    build_(1, 0, length - 1)


def get_max(ql: int, qr: int) -> tuple[int, int]:

    def get_max_(vert_ind: int, left_: int, right_: int, ql_: int, qr_: int) -> tuple[int, int]:
        # print(f'left_, right_: {left_, right_}, ql_, qr_: {ql_, qr_}')
        # border cases:
        if ql_ > qr_:
            return -1, 0
        if (left_, right_) == (ql_, qr_):
            return max_tree[vert_ind]
        update(vert_ind)
        # recurrent relation:
        middle = (left_ + right_) // 2
        i_ = vert_ind << 1
        return combine(
            get_max_(i_, left_, middle, ql_, min(qr_, middle)),
            get_max_(i_ + 1, middle + 1, right_, max(ql_, middle + 1), qr_)
        )

    return get_max_(1, 0, length - 1, ql, qr)


def range_update(ql: int, qr: int, new_val: int):

    def range_update_(vert_ind: int, left_: int, right_: int, ql_: int, qr_: int) -> None:
        # print(f'{counter}. left_, right_: {left_, right_}, ql_, qr_: {ql_, qr_}')
        # border cases:
        if ql_ > qr_:
            return
        if (left_, right_) == (ql_, qr_):
            max_tree[vert_ind] = postponed_update[vert_ind] = new_val, right_ - left_ + 1                      # 36.6 98
            return
        update(vert_ind)
        # recurrent relation:
        middle = (left_ + right_) // 2
        i_ = vert_ind << 1
        range_update_(i_, left_, middle, ql_, min(qr_, middle))
        range_update_(i_ + 1, middle + 1, right_, max(middle + 1, ql_), qr_)
        max_tree[vert_ind] = combine(max_tree[i_], max_tree[i_ + 1])

    range_update_(1, 0, length - 1, ql, qr)


process_queries()
