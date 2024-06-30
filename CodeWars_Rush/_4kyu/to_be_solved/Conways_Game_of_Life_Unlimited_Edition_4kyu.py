# accepted on codewars.com
from collections import defaultdict as d


moore_walk = tuple((j, i) for j in range(-1, 2) for i in range(-1, 2) if j | i)


def get_generation(cells: list[list[int]], generations: int) -> list[list[int]]:
    print(f'{moore_walk = }')                                                         # 36 366 98 989 98989 LL

    n, m = len(cells), len(cells[0])
    print(f'{n, m, generations = }')

    living_cells = {(j, i) for j in range(n) for i in range(m) if cells[j][i]}

    for gen in range(generations):
        # print(f'-> {living_cells}')
        evolve(living_cells)

    # defines borders:
    min_j = min(living_cells, key=lambda x: x[0])[0]
    max_j = min(living_cells, key=lambda x: -x[0])[0]
    min_i = min(living_cells, key=lambda x: x[1])[1]
    max_i = min(living_cells, key=lambda x: -x[1])[1]

    population = [[1 if (j, i) in living_cells else 0 for i in range(min_i, max_i + 1)] for j in range(min_j, max_j + 1)]

    print_population(population)

    return population


def evolve(living_cells: set[tuple[int, int]]) -> None:

    sleeping_cells_living_neighs_q = d(int)
    # new_living_cells = set()

    # cycling over all the living cells:
    set_ = set(living_cells)
    for living_cell in set_:
        print(f'{living_cell = }')
        moores_neighs = get_moores_neighs(*living_cell)
        sleeping_cells = moores_neighs - set_
        print(f'...{moores_neighs = }')
        # print(f'...{sleeping_cells = }')
        for sleeping_cell in sleeping_cells:
            sleeping_cells_living_neighs_q[sleeping_cell] += 1
        living_neighs_q = 8 - len(sleeping_cells)
        if 2 <= living_neighs_q <= 3:
            ...
        else:
            living_cells.remove(living_cell)

    # cycling over all the sleeping cells:
    for sleeping_cell, living_neighs_q in sleeping_cells_living_neighs_q.items():

        if living_neighs_q == 3:
            living_cells |= {sleeping_cell}


def get_moores_neighs(j: int, i: int) -> set[tuple[int, int]]:
    moores_neighs = set()
    for dj, di in moore_walk:
        moores_neighs |= {(j + dj, i + di)}
    return moores_neighs


def print_population(population: list[list[int]]):
    for row in population:
        print(f'{row}')


cells_ = [
    [1, 1, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 1, 1],
]

gens_ = 16

get_generation(cells_, gens_)
