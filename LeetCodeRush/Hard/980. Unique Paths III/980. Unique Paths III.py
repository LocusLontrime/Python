# accepted on leetcode.com


walk = ((1, 0), (0, -1), (-1, 0), (0, 1))


def unique_paths_3(grid: list[list[int]]) -> int:
    # linear sizes:
    max_j, max_i = len(grid), len(grid[0])
    # important pars for dfs method:
    start_j, start_i, end_j, end_i, obstacles_count = parse(grid, max_j, max_i)
    print(f'{start_j, start_i = } | {end_j, end_i = }')
    # starting dfs:
    return dfs(start_j, start_i, max_j, max_i, grid, end_j, end_i, max_j * max_i - obstacles_count - 1)


def parse(grid: list[list[int]], max_j: int, max_i: int):
    obstacles_count = 0
    for j in range(max_j):
        for i in range(max_i):
            if grid[j][i] == 1:
                start_j, start_i = j, i
            elif grid[j][i] == 2:
                end_j, end_i = j, i
            elif grid[j][i] == -1:
                obstacles_count += 1
    return start_j, start_i, end_j, end_i, obstacles_count


def dfs(j: int, i: int, max_j: int, max_i: int, grid: list[list[int]], end_j: int, end_i: int, length: int) -> int:
    print(f'...reaching [{j, i}]')
    # border case:
    if (j, i) == (end_j, end_i) and length == 0:
        # the path reaches the end point:
        return 1
    # if not:
    res = 0
    for dj, di in walk:
        j_, i_ = j + dj, i + di
        # we are within the grid's borders:
        if 0 <= j_ < max_j and 0 <= i_ < max_i:
            # searching for visitable neighs:
            if grid[j_][i_] in {0, 2}:
                # visiting:
                grid[j_][i_] = -1
                # next step:
                res += dfs(j_, i_, max_j, max_i, grid, end_j, end_i, length - 1)
                # unvisiting (backtracking):
                grid[j_][i_] = 0
    return res


test_ex = [
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 2]
]

test_ex_1 = [
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 2, -1]
]

print(f'test ex res -> {unique_paths_3(test_ex)}')                                    # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {unique_paths_3(test_ex_1)}')
