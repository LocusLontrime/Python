# accepted on leetcode.com

from collections import defaultdict as defd
from typing import Any


def grid_illumination(n: int, lamps: list[list[int]], queries: list[list[int]]) -> list[int]:
    # lamps list to set:
    lamps = set(tuple(lamp) for lamp in lamps)
    # for a start, let us create a 4 hashtables with illuminated cells:
    row = defd(int)
    col = defd(int)
    diag_pl = defd(int)
    diag_m = defd(int)
    # now hash all the lamps' illumination:
    for j, i in lamps:
        row[j] += 1
        col[i] += 1
        diag_pl[j + i] += 1
        diag_m[j - i] += 1
    # now we should process all the queries:
    answer = []
    for j, i in queries:
        if (j in row.keys()) or (i in col.keys()) or (j + i in diag_pl.keys()) or (j - i in diag_m.keys()):
            answer += [1]
            # remove the lamps:
            for j_, i_ in get_neighs(j, i):
                if (j_, i_) in lamps:
                    lamps.remove((j_, i_))
                    for d, el in [(row, j_), (col, i_), (diag_pl, j_ + i_), (diag_m, j_ - i_)]:
                        remove(d, el)
        else:
            answer += [0]
    # returns res:
    return answer


def remove(d: defd[Any, int], el: int):
    if el in d.keys():
        d[el] -= 1
        if d[el] == 0:
            del d[el]


def get_neighs(j: int, i: int) -> set[tuple[int, int]]:
    return {(j + dj, i + di) for dj in range(-1, 2) for di in range(-1, 2)}


test_ex = 5, [[0, 0], [4, 4]], [[1, 1], [1, 0]]  # [1, 1]
test_ex_1 = 5, [[0, 0], [4, 4]], [[1, 1], [1, 1]]  # [1, 1]
test_ex_2 = 5, [[0, 0], [0, 4]], [[0, 4], [0, 1], [1, 4]]  # [1,1,0]

print(f'test ex res -> {grid_illumination(*test_ex)}')                          # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {grid_illumination(*test_ex_1)}')
print(f'test ex 2 res -> {grid_illumination(*test_ex_2)}')
