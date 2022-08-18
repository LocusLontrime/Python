# accepted on codewars.com
directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # 36 366 98 989 Locus Lontrime
symbols_counter = 0
path_length = 0


def line(grid) -> bool:
    global directions, symbols_counter, path_length

    symbols_counter = 0
    memo_table = [[0] * len(grid[0]) for _ in range(len(grid))]
    x_coords = list()

    for curr_j in range(len(grid)):
        for curr_i in range(len(grid[0])):
            if grid[curr_j][curr_i] != " ":
                symbols_counter += 1
                if grid[curr_j][curr_i] == 'X':
                    x_coords.append([curr_j, curr_i])

    print(f'x coords: {x_coords[0][0], x_coords[0][1]}, {x_coords[1][0], x_coords[1][1]}')

    def recursive_seeker(k: int, j: int, i: int, prev_index_of_dir: int, length: int):
        global directions, path_length
        print(f'{j, i}, {grid[j][i]}')

        if grid[j][i] == 'X' and (j != x_coords[k][0] or i != x_coords[k][1]):
            path_length = length
            print(f'The line is valid, True')
            return True

        res = False
        mini_counter = 0
        possible_indexes = []

        match grid[j][i]:
            case '+':
                possible_indexes = [(prev_index_of_dir + 1) % len(directions), (prev_index_of_dir + 3) % len(directions)]
            case '-':
                possible_indexes = [el for el in [1, 3] if el == prev_index_of_dir]
            case '|':
                possible_indexes = [el for el in [0, 2] if el == prev_index_of_dir]
            case 'X':
                indexes = [[1, 3], [0, 2]]
                symbols = [['-', 'X', '+'], ['|', 'X', '+']]
                for ind in range(len(indexes)):
                    for el in indexes[ind]:
                        n_coords = [j + directions[el][0], i + directions[el][1]]
                        if 0 <= n_coords[0] < len(grid) and 0 <= n_coords[1] < len(grid[0]):
                            if grid[n_coords[0]][n_coords[1]] in symbols[ind]:
                                possible_indexes.append(el)

        for index_of_dir in possible_indexes:
            if prev_index_of_dir == -1 or index_of_dir != (prev_index_of_dir + 2) % len(directions):
                new_coords = [j + directions[index_of_dir][0], i + directions[index_of_dir][1]]
                if 0 <= new_coords[0] < len(grid) and 0 <= new_coords[1] < len(grid[0]):
                    if memo_table[new_coords[0]][new_coords[1]] != 1:
                        if grid[new_coords[0]][new_coords[1]] != " ":
                            memo_table[j][i] = 1
                            res = res or recursive_seeker(k, j + directions[index_of_dir][0], i + directions[index_of_dir][1], index_of_dir, length + 1)
                            memo_table[j][i] = 0
                            mini_counter += 1

        print(f'min counter: {mini_counter}, {j, i}')
        return res if mini_counter == 1 else False

    return (recursive_seeker(0, x_coords[0][0], x_coords[0][1], -1, 1) and path_length == symbols_counter) or (recursive_seeker(1, x_coords[1][0], x_coords[1][1], -1, 1) and path_length == symbols_counter)


grid_good = [
    "                    ",
    "     +--------+     ",
    "  X--+        +--+  ",
    "                 |  ",
    "                 X  ",
    "                    "
]

grid_good_1 = [
    "                     ",
    "    +-------------+  ",
    "    |             |  ",
    " X--+      X------+  ",
    "                     "
]

grid_bad = [
    "   |--------+    ",
    "X---        ---+ ",
    "               | ",
    "               X "
]

grid_bad_1 = [
    "      +------+",
    "      |      |",
    "X-----+------+",
    "      |       ",
    "      X       "
]

grid_edge_case = [
    "        ",
    "   ++   ",
    "  ++++  ",
    "  ++++  ",
    " X-++-X ",
    "        "
]

grid_edge_case_1 = [
    "        ",
    "  ++++  ",
    " X++++X ",
    "        "
]

grid_spiral = [
    "         ",
    " +-----+ ",
    " |+---+| ",
    " ||+-+|| ",
    " |||X+|| ",
    " X|+--+| ",
    "  +----+ ",
    "         "
]

grid_easy = [
    "                      ",
    "   +-------+          ",
    "   |      +++---+     ",
    "X--+      +-+   X     "
]

grid_near = [
    "        ",
    " XX---+ ",
    " |    | ",
    " |    | ",
    " +----+ ",
    "        "
]

# print(line(grid_good))
# print(line(grid_good_1))
# print(line(grid_bad))
# print(line(grid_bad_1))
# print(line(grid_edge_case))
# print(line(grid_edge_case_1))
# print(line(grid_spiral))
# print(line(grid_easy))
print(line(grid_near))

print(True or False)


