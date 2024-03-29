# accepted on codewars.com
step = 0


def peak_height(mountain: list[str]):
    global step
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if dy * dx == 0 and (dy, dx) != (0, 0)]
    grid = [[(0 if mountain[j][i] == '^' else '.') for i in range(len(mountain[0]))] for j in range(len(mountain))]
    # gets the nearest neighbouring cells:
    def get_neighs(y_, x_):
        return [(y_ + walk[i][0], x_ + walk[i][1]) for i in range(len(walk)) if
                0 <= y_ + walk[i][0] < len(mountain) and 0 <= x_ + walk[i][1] < len(mountain[0])]
    # emits a one tick of wave, evaluating the grid's heights:
    def wave_(wave_):
        global step
        for cell_ in wave_:
            for neigh_ in get_neighs(cell_[0], cell_[1]):
                if grid[neigh_[0]][neigh_[1]] == 0:
                    grid[neigh_[0]][neigh_[1]] = step + 1
                    yield neigh_
    # defines initial front of wave:
    wave, step = [], 0
    for y, row in enumerate(mountain):
        for x, cell in enumerate(row):
            if cell == "^":
                if y in [0, len(mountain) - 1] or x in [0, len(mountain[0]) - 1]:
                    grid[y][x] = 1
                    wave.append((y, x))
                else:
                    for neigh in get_neighs(y, x):
                        if mountain[neigh[0]][neigh[1]] == " ":
                            grid[y][x] = 1
                            wave.append((y, x))
                            break
    # evaluating all the heights in cycle while there are some:
    while len(wave) > 0:
        step += 1
        wave = list(wave_(wave))
    # shows the heights map:
    for row in grid:
        for cell in row:
            print(f'{cell}', end=' ')
        print()
    print()
    # returns the max height on the map given:
    return step


mountain1 = [
    "^^^^^^        ",
    " ^^^^^^^^     ",
    "  ^^^^^^^     ",
    "  ^^^^^       ",
    "  ^^^^^^^^^^^ ",
    "  ^^^^^^      ",
    "  ^^^^        "
]

print(f'peak height: {peak_height(mountain1)}')
