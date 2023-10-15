# accepted on codewars.com
import random

# need to be coloured!!!
rec_iters = 0
en_alphabet = 'abcdefghijklmnopqrstuvwxyz123456789!@$%^&*|-+'
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
names = ['Up', 'Right', 'Down', 'Left']
colour_block_symbol = 'B'
empty_cell_symbol = '.'
# visualisation:
colours: dict[tuple[int, int], str]
colours_dict = None

BOLD = "\033[1m"

BLACK = "\033[30m{}"
RED = "\033[31m{}"
GREEN = "\033[32m{}"
YELLOW = "\033[33m{}"
BROWN = "\033[34m{}"
PURPLE = "\033[35m{}"
CYAN = "\033[36m{}"
X = "\033[37m{}"
END = "\033[0m"

COLOURS = [RED, GREEN, YELLOW, BROWN, PURPLE, CYAN, BLACK, X]


def play_flou(game_map: str):
    # showing the starting game-map:
    print(f'game map: ')
    print(f'{game_map}')
    print()
    # creating a grid of cells:
    grid, colour_blocks = make_grid_from_blueprint(game_map)
    print(f'initial grid: ')
    show_grid(grid)
    print(f'colour blocks: {colour_blocks}')
    print(f'colours: {colours}')
    # starting recursive filling:
    result = rec_filler(grid, colour_blocks)
    # returning the result with coordinates changed:
    return [[cell[0] - 1, cell[1] - 1, cell[2]] for cell in result] if result else []


def make_grid_from_blueprint(game_map: str):
    global colours, colours_dict
    colours_dict = {}
    colours = dict()
    grid = []
    colour_blocks = []
    rows = game_map.split('\n')  # [1:-1]
    for j, row in enumerate(rows):
        grid.append([])
        for i, cell in enumerate(row):
            if cell == colour_block_symbol:
                colour_blocks.append(block := (j, i))
                s = colours[block] = en_alphabet[len(colours)]
                colours_dict[s] = COLOURS[len(colours) - 1]
                grid[j].append(s.upper())
            else:
                grid[j].append(cell)
    return grid, colour_blocks


def rec_filler(grid, colour_blocks):
    global rec_iters
    rec_iters += 1
    if rec_iters % 10000 == 0:
        print(f'rec_iter: {rec_iters}')
    res = []
    # we can start with any colour block remained:
    for ind, colour_block in enumerate(colour_blocks):
        # getting the possible directions of current colour block's moving:
        possible_dirs = get_poss_dirs(grid, colour_block)
        # there are no possible direction to move the block:
        if len(possible_dirs) == 0:
            return
        # cycling through all the possible directions:
        for possible_dir in possible_dirs:
            # trying to make a move:
            move_colour_block(grid, colour_block, possible_dir)
            # needed for tests:
            # adding the movement dir of current colour block to the res list:
            res.append([colour_block[0], colour_block[1], names[possible_dir]])
            # now we should try to move all the colour blocks remained:
            colour_blocks_remained = colour_blocks[:ind] + colour_blocks[ind + 1:]
            # if it was the last block:
            # base case:
            if len(colour_blocks_remained) == 0:
                if check_grid(grid):
                    print(f'solved grid: ')
                    show_grid(grid)
                    return res
                    # next step of recursion:
            further_movements = rec_filler(grid, colour_blocks_remained)
            # checks whether we can fill all the grid moving the colour blocks remained if so -->> we will get a solution:
            if further_movements:
                # merging two parts of solution together:
                res += further_movements
                return res
            # backtracking:
            move_back(grid, colour_block)
            res.pop()
    return res


def check_grid(grid):
    for row in grid:
        for cell in row:
            if cell == empty_cell_symbol:
                return False
    return True


def move_colour_block(grid, colour_block, dir_ind):
    curr_dir_ind = dir_ind
    flag_of_movement = True
    # here we make a move in accordance with the game rules:
    new_j, new_i = colour_block[0], colour_block[1]
    while flag_of_movement:
        # making one step of colour block:
        new_j += (d_j := directions[curr_dir_ind][0])
        new_i += (d_i := directions[curr_dir_ind][1])
        grid[new_j][new_i] = colours[colour_block]
        # checks next step possibility:
        next_j, next_i = new_j + d_j, new_i + d_i
        if grid[next_j][next_i] != empty_cell_symbol:
            # trying to change direction:
            curr_dir_ind = (curr_dir_ind + 1) % 4
            ninety_degrees_right_next_j, ninety_degrees_right_next_i = new_j + directions[curr_dir_ind][0], new_i + \
                                                                       directions[curr_dir_ind][1]
            # stop condition:
            if grid[ninety_degrees_right_next_j][ninety_degrees_right_next_i] != empty_cell_symbol:
                flag_of_movement = False


def move_back(grid, colour_block):
    for j, row in enumerate(grid):
        for i, cell in enumerate(row):
            if cell == colours[colour_block]:
                grid[j][i] = empty_cell_symbol


def get_poss_dirs(grid, colour_block: tuple[int, int]):
    possible_directions = []
    for ind, direction in enumerate(directions):
        new_j, new_i = colour_block[0] + direction[0], colour_block[1] + direction[1]
        if grid[new_j][new_i] == empty_cell_symbol:
            possible_directions.append(ind)
    return possible_directions


def show_grid(grid):
    global colours_dict
    print(f'grid: ')
    for row in grid:
        for cell in row:
            if colours_dict and cell in colours_dict.keys():
                colour_print(cell, colours_dict[cell])
            else:
                print(f'{cell}', end='')
        print()
    print()


def colour_print(char, colour):
    print(f"{(BOLD + colour.format(char) + END)}", end='')


game_map_x = '''+------+
|BB....|
|B.....|
|......|
|......|
|......|
|......|
+------+'''

game_map_v = '''+------+
|B.....|
|......|
|.....B|
|..B...|
|......|
|.....B|
+------+'''

game_map_1 = '''+----+
|B...|
|....|
|....|
|....|
+----+'''

game_map_2 = '''+----+
|B...|
|....|
|....|
|...B|
+----+'''

game_map_3 = '''+----+
|.B..|
|....|
|....|
|..B.|
+----+'''


def create_map_blueprint(j_max: int, i_max: int, colours_q: int):
    def generate_colours_positions() -> list[tuple[int, int]]:
        colours_positions_ = []
        possible_positions = [(j_, i) for i in range(i_max) for j_ in range(j_max)]
        for _ in range(colours_q):
            r = random.randrange(0, len(possible_positions))
            colours_positions_.append(possible_positions.pop(r))
        return colours_positions_

    colours_positions = generate_colours_positions()

    def create_border_line():
        return '+' + '-' * i_max + '+'

    def create_line(j_: int):
        line = ''
        for i in range(i_max):
            if (j_, i) in colours_positions:
                line += 'B'
            else:
                line += '.'
        return f'|{line}|'

    if j_max < 3:
        print(f'j_max cannot be less than 3')
        return
    if i_max < 3:
        print(f'i_max cannot be less than 3')
        return
    map_blueprint = ''
    s = f'{create_border_line()}'
    for j in range(j_max):
        map_blueprint += f'{create_line(j)}\n'
    return f'{s}\n{map_blueprint}{s}'


game_map_huge = f'''{create_map_blueprint(18, 36, 6)}'''

# print(play_flou(game_map_1))
# print(play_flou(game_map_2))
# print(play_flou(game_map_3))
# print(play_flou(game_map_v))
print(play_flou(game_map_huge))

# print(f'{[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][1:-1]}')
# print(f'{[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:3]}')

# make_grid_from_blueprint(game_map_x)
