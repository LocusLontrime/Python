# find the quantity of distinct islands (if one island can be processed from another one via reflection or rotation these two are the same)...
import random
import sys
import time
from collections import defaultdict as d


sys.setrecursionlimit(100_000)


walk = ((0, 1), (1, 0), (0, -1), (-1, 0))


def find_islands(islands_map: list[str]):
    islands_map_ = [[_ for _ in row] for row in islands_map]
    # print(f'initial islands map: ')
    # print_map(islands_map_)
    counter = 0
    hashed_islands = set()
    distinct_islands_q = 0
    for j in range(j_max := len(islands_map_)):
        for i in range(i_max := len(islands_map_[0])):
            if islands_map_[j][i] == 'x':
                counter += 1
                print(f'{counter}th island found...')
                points = []
                dfs(j, i, j_max, i_max, islands_map_, points)
                print(f'...points found: ')
                print(f'...{points = }')
                print(f'...island: ')
                print_island(points)
                inv_dict: d[int, int] = build_dict(points)
                print(f'...{inv_dict = }')
                packed_inv_dict = pack(inv_dict)
                print(f'...{packed_inv_dict = }')
                if packed_inv_dict not in hashed_islands:
                    hashed_islands |= {packed_inv_dict}
                    distinct_islands_q += 1
                    print(f'...A NEW ISLAND FOUND!!!')
                else:
                    ...
                    print(f'...JUST AN OLD ONE...')
                # print_map(islands_map_)
    return distinct_islands_q


def euclidian_dist_sq(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def build_dict(points: list[tuple[int, int]]) -> d[int, int]:
    inv_dict = d(int)
    for n in range(len(points)):
        for m in range(n + 1, len(points)):
            inv_dict[euclidian_dist_sq(points[n], points[m])] += 1
    return inv_dict


def pack(inv_dict: d[int, int]) -> str:
    res = '0'  # starting hash for an island with the one only point...
    for distance in sorted(inv_dict.keys()):
        res += f'{distance}{inv_dict[distance]}'
    return res


def dfs(j: int, i: int, j_max: int, i_max: int, map_: list[list[str]], points: list[tuple[int, int]]):
    if 0 <= j < j_max and 0 <= i < i_max:
        if map_[j][i] == 'x':
            points += [(j, i)]
            map_[j][i] = ' '
            for dj, di in walk:
                dfs(j + dj, i + di, j_max, i_max, map_, points)


def print_map(map_: list):
    for row in map_:
        print(f'{row}')


def print_island(points: list[tuple[int, int]]):
    max_j = max(points, key=lambda x: x[0])[0]
    min_j = min(points, key=lambda x: x[0])[0]
    max_i = max(points, key=lambda x: x[1])[1]
    min_i = min(points, key=lambda x: x[1])[1]
    points_ = set(points)
    print(f' ' + f'_' * (max_i - min_i + 1))
    for j in range(min_j, max_j + 1):
        print(f'|', end='')
        for i in range(min_i, max_i + 1):
            print(f'x' if (j, i) in points_ else ' ', end='')
        print(f'|')
    print(f' ' + f'-' * (max_i - min_i + 1))


map1 = [
    'xx   xxx',
    'xx   xx ',
    'x       ',
    ' xx     ',
    '   x    ',
    'x  x  xx',
    'xx      ',
    'xx      '
]                                                                                     # 36 366 98 989 98989 LL

mj, mi = 200, 200
map_great = [''.join(['x' if random.randint(1, 100) <= 55 else ' ' for _ in range(mi)]) for _ in range(mj)]

start = time.time_ns()
print(f'RESULT -> {find_islands(map_great)} distinct island found...')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
