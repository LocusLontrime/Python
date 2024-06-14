# accepted on codewars.com
walk = ((0, 1), (1, 0), (0, -1), (-1, 0))


def pac_man(n: int, pm: list[int], enemies: list[list[int]]) -> int:
    grid = [['O' for _ in range(n)] for _ in range(n)]
    grid[pm[0]][pm[1]] = 'P'
    for ey, ex in enemies:
        for k in range(n):
            grid[ey][k] = 'E'
            grid[k][ex] = 'E'
    return dfs_count(*pm, n, grid)


def dfs_count(y: int, x: int, n: int, grid: list[list[str]]) -> int:
    res = 0
    # base case:
    if 0 <= y < n and 0 <= x < n:
        if grid[y][x] != 'E':
            if grid[y][x] == 'O':
                res += 1
            # visiting:
            grid[y][x] = 'E'
            # next turns:
            for dy, dx in walk:
                res += dfs_count(y + dy, x + dx, n, grid)
    return res


print(f'res: {pac_man(10,[4, 6],[[0,2], [5,2], [5,5]])}')  # -> 15



