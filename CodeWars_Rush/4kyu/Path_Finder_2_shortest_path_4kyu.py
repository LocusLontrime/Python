directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def path_finder(maze):
    # converting maze-string to maze-table:
    maze_table = convert_str_to_table(maze)
    print(f'maze_table: {maze_table}')
    # wave-spreading algorithm Lee
    front_wave = [(0, 0)]
    wave_spreading_step = 1
    while front_wave:
        new_front_wave = []
        for front_cell in front_wave:
            if (f_j := front_cell[0], f_i := front_cell[1]) == (len(maze_table) - 1, len(maze_table[0]) - 1):
                print(f'table: ')
                for t in maze_table:
                    print(t)
                return maze_table[f_j][f_i]
            for neigh in get_valid_neighs(maze_table, front_cell):
                maze_table[neigh[0]][neigh[1]] = wave_spreading_step
                new_front_wave.append(neigh)
        front_wave = new_front_wave.copy()
        wave_spreading_step += 1
    print(f'table: ')
    for t in maze_table:
        print(t)
    return False


# the valid neighbouring cells to be added in new front wave at the next step of main cycle:
def get_valid_neighs(table: list[list[int]], point: tuple[int, int]) -> list[tuple[int, int]]:
    neighs = []
    for direction in directions:
        new_j, new_i = point[0] + direction[0], point[1] + direction[1]
        if is_point_valid(table, new_j, new_i):
            neighs.append((new_j, new_i))
    return neighs


# checks if the next possible neigh is valid:
def is_point_valid(table: list[list[int]], j: int, i: int) -> bool:
    return 0 <= j < len(table) and 0 <= i < len(table[0]) and table[j][i] == 0 and (j, i) != (0, 0)


def convert_str_to_table(maze: str) -> list[list[int]]:
    table = []
    for j, row in enumerate(maze.split('\n')):
        table.append([])
        for el in row:
            table[j].append(-1 if el == 'W' else 0)
    return table


a = "\n".join([
          ".W...",
          ".W...",
          ".W.W.",
          "...W.",
          "...W."])


print(path_finder(a))


