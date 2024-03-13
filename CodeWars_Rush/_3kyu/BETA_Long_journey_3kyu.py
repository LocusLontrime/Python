# accepted on codewars.com
import math

memo_table: dict[tuple[int, int], int]
dirs = ((-1, 1), (0, 1), (1, 1))


def cheapest_route(road: list[list[int]]):                                            # 36 366 98 989 98989 LL
    global memo_table

    max_j, max_i = len(road), len(road[0])
    memo_table = {(j, max_i): 0 for j in range(max_j)}

    min_route = math.inf
    for j in range(max_j):
        min_route = min(min_route, dp_ := dp(j, 0, max_j, max_i, road))
        print(f'{j = } | {dp_}')

    print(f'{memo_table = }')

    return min_route


def dp(j: int, i: int, max_j: int, max_i: int, road: list[list[int]]) -> int:
    if (j, i) not in memo_table.keys():

        min_dp = math.inf

        for dj, di in dirs:
            if 0 <= (j_ := j + dj) < max_j and 0 <= (i_ := i + di):
                min_dp = min(min_dp, dp(j_, i_, max_j, max_i, road))

        memo_table[(j, i)] = min_dp + road[j][i]

    # print(f'{j, i} -> {memo_table[(j, i)]}')

    return memo_table[(j, i)]


road_1 = [
    [1, 32, 19, 9, 5],
    [4, 8, 30, 6, 5],
    [5, 17, 18, 10, 6],
    [9, 13, 4, 11, 7]
]

road_2 = [[2, 1, 12, 6, 13, 2],
          [2, 18, 19, 17, 3, 13],
          [7, 18, 8, 18, 5, 5],
          [14, 6, 15, 11, 2, 5],
          [18, 19, 1, 8, 9, 8],
          [9, 2, 3, 2, 14, 4],
          [7, 16, 14, 15, 11, 1]]  # ans = 24

print(f'res: {cheapest_route(road_2)}')
