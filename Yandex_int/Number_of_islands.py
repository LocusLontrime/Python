walk = ((-1, 0), (0, 1), (1, 0), (0, -1))


def island_counter(islands_map: list[list[int]]) -> int:
    counter = 0
    for j in range(max_j := len(islands_map)):
        for i in range(max_i := len(islands_map[0])):
            if islands_map[j][i] == 1:
                bfs(islands_map, j, i, max_j, max_i)
                counter += 1
    return counter


def bfs(islands_map: list[list[int]], j: int, i: int, max_j: int, max_i: int):
    if islands_map[j][i] == 1:
        # visiting:
        islands_map[j][i] = 0
        for dj, di in walk:
            j_, i_ = j + dj, i + di
            if is_valid(j_, i_, max_j, max_i):
                bfs(islands_map, j_, i_, max_j, max_i)


def is_valid(j: int, i: int, max_j: int, max_i: int) -> bool:
    return 0 <= j < max_j and 0 <= i < max_i


islands_map_ = [
    [1, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]

print(f'islands: {island_counter(islands_map_)}')
