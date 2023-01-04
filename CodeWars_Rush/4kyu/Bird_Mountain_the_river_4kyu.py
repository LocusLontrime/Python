def dry_ground(terrain):
    # your code here!
    return -1, -1, -1, -1


step = 0
steps_dict = {}


def peak_height(mountain: list[str]):
    global step, steps_dict
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if dy * dx == 0 and (dy, dx) != (0, 0)]
    grid = [[(0 if mountain[j][i] == '^' else '.') for i in range(len(mountain[0]))] for j in range(len(mountain))]

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
    wave = []
    step, river_counter, spaces_counter = 0, 0, 0
    for y, row in enumerate(mountain):
        for x, cell in enumerate(row):
            if cell == '-':
                river_counter += 1
            elif cell == ' ':
                spaces_counter += 1
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
    if wave:
        step += 1
        steps_dict[step] = wave
    else: steps_dict[step] = []
    wave = wave_(wave)
    if wave: steps_dict[step] = wave
    else: steps_dict[step] = []

    for row in grid:
        for cell in row:
            print(f'{cell}', end=' ')
        print()
    print()

    area = len(mountain) * len(mountain[0])

    print(f'steps_dict: {steps_dict}')

    print(f'dry ground: {(area - river_counter, area - river_counter - spaces_counter, area - river_counter - spaces_counter - len(steps_dict[1]), area - river_counter - spaces_counter - len(steps_dict[1]) - len(steps_dict[2]))}')
    return step


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


print(f'peak height: {peak_height(map_of_mountain_and_river)}')
