step = 0


def dry_ground(mountain: list[str]):
    if len(mountain):
        return 0, 0, 0, 0
    global step
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if dy * dx == 0 and (dy, dx) != (0, 0)]
    grid = [[(0 if (m := mountain[j][i]) == '^' else ('.' if m == ' ' else '-')) for i in range(len(mountain[0]))] for j in range(len(mountain))]

    def get_neighs(y_, x_):
        return [(y_ + walk[i][0], x_ + walk[i][1]) for i in range(len(walk)) if
                0 <= y_ + walk[i][0] < len(mountain) and 0 <= x_ + walk[i][1] < len(mountain[0])]

    def wave_(wave_):
        global step
        new_wave = []
        for cell_ in wave_:
            for neigh_ in get_neighs(cell_[0], cell_[1]):
                if grid[neigh_[0]][neigh_[1]] == 0:
                    grid[neigh_[0]][neigh_[1]] = step + 1
                    new_wave.append(neigh_)
        if new_wave: step += 1
        return new_wave

    def show():
        for row_ in grid:
            for cell_ in row_:
                print(f'{cell_}', end='')
            print()
        print()

    wave = []
    step, river_front = 0, []
    for y, row in enumerate(mountain):
        for x, cell in enumerate(row):
            if cell == '-': river_front.append((y, x))
            elif cell == "^":
                if y in [0, len(mountain) - 1] or x in [0, len(mountain[0]) - 1]:
                    grid[y][x] = 1
                    wave.append((y, x))
                else:
                    for neigh in get_neighs(y, x):
                        if mountain[neigh[0]][neigh[1]] in {" ", '-'}:
                            grid[y][x] = 1
                            wave.append((y, x))
                            break
    # bird calculations for mountain heights:
    print(f'bird calculations for mountain heights: ')
    if wave:
        step += 1
        print(f'current height: {step}, grid:')
        show()
    while wave:
        wave = wave_(wave)
        print(f'current height: {step}, grid:')
        show()

    def flood(y_, x_, step_, new_river_front_):
        g = grid[y_][x_]
        if type(g) is int and g == step_:
            new_river_front_.append((y_, x_))
            return 0
        elif type(g) is str or (type(g) is int and g < step_):
            # flooding:
            k = 1 if grid[y_][x_] != '-' else 0
            grid[y_][x_] = '-'
            # proceeding to the neighbouring cells:
            for neigh_y_, neigh_x_ in get_neighs(y_, x_):
                if grid[neigh_y_][neigh_x_] != '-':
                    k += flood(neigh_y_, neigh_x_, step_, new_river_front_)
            return k
        return 0

    area = len(mountain) * len(mountain[0]) - len(river_front)
    res = [area]
    # bird's flooding calculations:
    print(f"bird's flooding calculations: ")
    print(f'initial area: {area}')
    for step in range(1, 3 + 1):
        print(f'flooding, step {step}th, grid: ')
        print(f'river_front: {river_front}')
        new_river_front = []
        flooded_cells = sum(flood(y, x, step, new_river_front) for y, x in river_front)
        print(f'flooded_cells: {flooded_cells}')
        area -= flooded_cells
        res.append(area)
        print(f'area remained: {area}')
        if new_river_front: river_front = new_river_front[:]
        show()

    return res


map_of_mountain_and_river = [
    "  ^^^^^^             ",
    "^^^^^^^^       ^^^   ",
    "^^^^^^^  ^^^         ",
    "^^^^^^^  ^^^         ",
    "^^^^^^^  ^^^         ",
    "---------------------",
    "^^^^^                ",
    "   ^^^^^^^^  ^^^^^^^ ",
    "^^^^^^^^     ^     ^ ",
    "^^^^^        ^^^^^^^ ",
]


# print(f'Flooded regions: {dry_ground(map_of_mountain_and_river)}')
t = (1, 2, 3, 98)
print(f'length: {len(t)}')


