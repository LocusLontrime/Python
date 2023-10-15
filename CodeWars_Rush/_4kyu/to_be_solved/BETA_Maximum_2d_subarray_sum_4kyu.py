import math

max_res: tuple[int, int, int]


def max_sum(arr: list[list[int]]):
    best_res = 0, 0, 0, 0, -math.inf
    mj, mi = len(arr), len(arr[0])
    # prefix arrays building:
    columns_prefixes = []
    for i in range(0, mi):
        columns_prefix = [0 for _ in range(mj + 1)]
        for j in range(0, mj):
            columns_prefix[j + 1] = columns_prefix[j] + arr[j][i]
        columns_prefixes.append(columns_prefix)
    # kadane-borodane:
    for js in range(0, mj):
        for je in range(js, mj):
            row_sums = [columns_prefixes[i][je + 1] - columns_prefixes[i][js] for i in range(0, mi)]
            ist, ie, res_ = max_sequence(row_sums)
            if res_ > best_res[4]:
                best_res = js, ist, je, ie, res_
    # returning res:
    return best_res


# auxiliary methods:
def max_sequence(arr: list[int]):
    global max_res
    max_res = 0, 0, -math.inf
    dp_1d(len(arr) - 1, arr)
    return max_res


def dp_1d(i: int, arr: list[int]) -> tuple[int, int]:
    global max_res
    # border case:
    if i == 0:
        return 0, arr[i]
    _i, _res = dp_1d(i - 1, arr)
    best_i, res = (i, arr[i]) if (r := _res + arr[i]) < arr[i] else (_i, r)
    if res > max_res[2]:
        max_res = best_i, i, res
    return best_i, res


arr_ = [
    [5, 6, 0, 0],
    [-6, -7, 0, 3],
    [3, 8, -10, -5],
    [-3, -7, 0, -1],
    [4, 4, -2, -5]
]  # -->> 0, 0, 1, 0, 11

arr_x = [
    [ 1,  2, -1, -4, -20],
    [-8, -3,  4,  2,   1],
    [ 3,  8, 10,  1,   3],
    [-4, -1,  1,  7, - 6]
]

arr_z = [
    [-15, 27, 57, -75, 86, -66, -48],
    [-20, 50, 45, -42, -58, -35, -84],
    [23, 47, 23, -61, 10, 85, -69],
    [-33, -34, 52, 85, 17, 52, 82],
    [-72, 67, -90, -91, 9, 84, 60],
    [66, 25, -44, 85, 43, -43, -18],
    [-16, 95, -53, 81, 85, -57, -45],
    [-67, 30, -61, -77, -16, 86, -50],
    [-25, -51, -98, -13, -62, 68, 63],
    [-65, 83, 98, -30, 22, 34, 82],
    [-75, -40, -47, 83, 74, 89, -38],
    [36, -85, -33, -12, 97, -94, -21],
    [-77, -47, -44, -7, -47, 74, 65],
    [-67, -64, 12, -4, 27, 7, 5],
    [-36, -54, 92, 55, 86, 85, 66],
    [38, -29, 25, -12, 68, -61, 86],
    [35, 19, 47, -86, -77, 35, 73],
    [1, 12, 98, -30, 40, 88, -25],
    [-47, -58, 29, -33, -22, -32, 82],
    [4, 10, 40, 96, 75, -79, -69],
    [-73, -8, -6, 51, 48, 39, 1],
    [70, -50, 40, -4, 33, -40, -68],
    [20, -30, 1, -97, -62, -52, -89],
    [89, 71, 82, -55, -15, -20, -53],
    [43, -66, -17, 11, -28, 47, -94]
]

flat_arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

print(f'res: {max_sum(arr_z)}')

# print(f'res: {max_sequence(flat_arr)}')

# t = (1, 2, 3, 4, 5)
# r = *t, 6
# print(f'{r}, {type(r)}')
