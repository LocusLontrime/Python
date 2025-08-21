# accepted on leetcode.com


def cherry_pickup(grid: list[list[int]]) -> int:
    # linear sizes:
    max_j, max_i = len(grid), len(grid[0])
    # let us use dp technique:
    # to gatherers start simultaneously -> i2 = (i1 + i1) - j2
    memo_table = {}
    return max(0, dp(0, 0, 0, max_j, max_i, grid, memo_table))


def dp(j1: int, i1: int, j2: int, max_j: int, max_i: int, grid: list[list[int]], memo_table: dict) -> int:
    # border case:
    if (j1, i1) == (max_j - 1, max_i - 1):
        return grid[j1][i1]
    if grid[j1][i1] == -1 or grid[j2][(j1 + i1) - j2] == -1:
        return -1
    # core algo:
    if (j1, i1, j2) not in memo_table.keys():
        i2 = (j1 + i1) - j2  # simultaneous start!
        cherries = grid[j1][i1] + (0 if j1 == j2 else grid[j2][i2])
        values = []
        if j1 + 1 < max_j and j2 + 1 < max_j:
            values += [dp(j1 + 1, i1, j2 + 1, max_j, max_i, grid, memo_table)]
        if j1 + 1 < max_j and (j1 + i1 + 1) - j2 < max_i:
            values += [dp(j1 + 1, i1, j2, max_j, max_i, grid, memo_table)]
        if i1 + 1 < max_i and j2 + 1 < max_j:
            values += [dp(j1, i1 + 1, j2 + 1, max_j, max_i, grid, memo_table)]
        if i1 + 1 < max_i and (j1 + i1 + 1) - j2 < max_i:
            values += [dp(j1, i1 + 1, j2, max_j, max_i, grid, memo_table)]
        res = max(values)
        memo_table[(j1, i1, j2)] = (res + cherries) if res != -1 else -1          # 36 366 98 989 98989 LL LL
    return memo_table[(j1, i1, j2)]


test_ex = [
    [0, 1, -1],
    [1, 0, -1],
    [1, 1, 1]
]

print(f'test ex res -> {cherry_pickup(test_ex)}')                                     # 36 366 98 989 98989 LL LL













