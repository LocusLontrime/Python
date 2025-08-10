# accepted on leetcode.com


walk = ((1, 0), (0, -1), (-1, 0), (0, 1))


def contain_virus(is_infected: list[list[int]]) -> int:
    # linear sizes:
    max_j, max_i = len(is_infected), len(is_infected[0])
    # the core algo:
    infected_cells = 0
    walls_built = 0
    iteration = 0
    quarantined_cells = set()
    while infected_cells < max_j * max_i:
        # at first, we must find all infected regions, their healthy cells borders and numbers of walls needed to quarantine them:
        unions, borders, walls_quantities, infected_cells = finds_inf_unions(max_j, max_i, is_infected, quarantined_cells)
        if not unions:
            # virus cannot widen more:
            break
        # secondly, we must define the most dangerous region (largest healthy cells domain is in danger):
        max_border = -1
        max_ind = None
        for i, border in enumerate(borders):
            if len(border) > max_border:
                max_border = len(border)
                max_ind = i
        # finally, we should quarantine region found, transform borders to infected regions and continue iterating:
        walls_built += walls_quantities[max_ind]
        quarantined_cells |= unions[max_ind]
        for ind, union in enumerate(unions):
            if ind != max_ind:
                for j, i in union:
                    is_infected[j][i] = 1
        for ind, border in enumerate(borders):
            if ind != max_ind:
                for j, i in border:
                    is_infected[j][i] = 1
        # increases the iteration:
        iteration += 1
    return walls_built


def finds_inf_unions(max_j: int, max_i: int, is_infected: list[list[int]], quarantined_cells: set):
    unions = []
    borders = []
    walls_quantities = []
    infected_cells = 0
    # finds unions of infected cells:
    for j in range(max_j):
        for i in range(max_i):
            if (j, i) not in quarantined_cells:
                if is_infected[j][i]:
                    unions += [set()]
                    borders += [set()]
                    walls_quantities += [bfs(j, i, max_j, max_i, is_infected, unions[-1], borders[-1], quarantined_cells)]
                    infected_cells += len(borders[-1])
    return unions, borders, walls_quantities, infected_cells


def bfs(j: int, i: int, max_j: int, max_i: int, is_infected: list[list[int]], union: set, borders: set, quarantined_cells: set) -> int:
    res = 0
    # do not cross the borders:
    if 0 <= j < max_j and 0 <= i < max_i:
        # not a quarantined cell:
        if (j, i) not in quarantined_cells:
            # locates a solo union:
            if is_infected[j][i]:
                # adds infected cell to the union set:
                union |= {(j, i)}
                # visiting the cell:
                is_infected[j][i] = 0
                # get neighs:
                for dj, di in walk:
                    # bfs moves wider:
                    res += bfs(j + dj, i + di, max_j, max_i, is_infected, union, borders, quarantined_cells)
                return res
            elif (j, i) not in union:
                borders |= {(j, i)}
                res += 1
    return res                                                                        # 36 366 98 989 98989 LL LL


def print_grid(is_infected: list[list[int]], s: str):
    print(f'{s}')
    for row in is_infected:
        print(f'{row}')


test_ex = [
    [0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

test_ex_1 = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

test_ex_2 = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0]
]

test_ex_3 = [[0]]

test_ex_4 = [[1]]

test_ex_z = [
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 1]
]

print(f'test ex res -> {contain_virus(test_ex)}')                                     # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {contain_virus(test_ex_1)}')
print(f'test ex 2 res -> {contain_virus(test_ex_2)}')
print(f'test ex 3 res -> {contain_virus(test_ex_3)}')
print(f'test ex 4 res -> {contain_virus(test_ex_4)}')
print(f'test ex z res -> {contain_virus(test_ex_z)}')
