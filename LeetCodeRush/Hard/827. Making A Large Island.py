# accepted on leetcode.com


from collections import defaultdict


walk = ((1, 0), (0, -1), (-1, 0), (0, 1))


def largest_island(grid: list[list[int]]) -> int:
    # linear sizes:
    max_j, max_i = len(grid), len(grid[0])
    # now let us find all the isolated islands:
    islands, linking_cells = find_islands(max_j, max_i, grid)
    # max possible area island:
    max_poss_island_area = max([len(island) for island in islands] + [1])
    if linking_cells:
        max_poss_island_area = max(
            max_poss_island_area,
            max(sum(len(islands[i]) for i in indices) for indices in linking_cells.values()) + 1
        )
    return max_poss_island_area


def find_islands(max_j: int, max_i: int, grid: list[list[int]]):
    islands = []
    linking_cells = defaultdict(set)
    # cycling all over the grid's cells:
    island_index = 0
    for j in range(max_j):
        for i in range(max_i):
            if grid[j][i]:
                islands += [set()]
                bfs(j, i, max_j, max_i, grid, islands[-1], linking_cells, island_index)
                # the next island should have incremented index by 1:
                island_index += 1

    print(f'islands -> ')
    for i, island in enumerate(islands):
        print(f'island index: {i} | {island = }')
    print(f'{linking_cells = }')
    return islands, linking_cells


def bfs(j: int, i: int, max_j: int, max_i: int, grid: list[list[int]], island: set, linking_cells: defaultdict, island_index: int):
    # we are in the grid:
    if 0 <= j < max_j and 0 <= i < max_i:
        # it is a land cell:
        if grid[j][i] == 1:
            # visiting:
            grid[j][i] = 0
            # adding the cell to the island:
            island |= {(j, i)}
            # now proceeding farther:
            for dj, di in walk:
                bfs(j + dj, i + di, max_j, max_i, grid, island, linking_cells, island_index)
        else:
            # it has not been visited before:
            if (j, i) not in island:
                # it is a possible linking cell:
                linking_cells[(j, i)] |= {island_index}


test_ex = [
    [1, 1, 0, 1, 1],
    [0, 1, 0, 1, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0]
]

print(f'test ex res -> {largest_island(test_ex)}')                                    # 36 366 98 989 98989 LL LL



