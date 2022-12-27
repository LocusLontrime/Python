# accepted on codewars.com
import random

en_alphabet = 'abcdefghijklmnopqrstuvwxyz123456789!@$%^&*|-+'
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
names = ['Up', 'Right', 'Down', 'Left']
colour_block_symbol = 'B'
empty_cell_symbol = '.'
# visualisation:
colours: dict[tuple[int, int]]


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
    global colours
    colours = dict()
    grid = []
    colour_blocks = []
    rows = game_map.split('\n')  # [1:-1]
    for j, row in enumerate(rows):
        grid.append([])
        for i, cell in enumerate(row):
            if cell == colour_block_symbol:
                colour_blocks.append(block := (j, i))
                colours[block] = en_alphabet[len(colours)]
            grid[j].append(cell)
    return grid, colour_blocks


def rec_filler(grid, colour_blocks):
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
            ninety_degrees_right_next_j, ninety_degrees_right_next_i = new_j + directions[curr_dir_ind][0], new_i + directions[curr_dir_ind][1]
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
    print(f'grid: ')
    for row in grid:
        print(f'{row}')


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


def create_map_blueprint(j_max: int, i_max: int, inv_freq: int):
    def create_border_line(length: int):
        return '+' + '-' * (length - 2) + '+'

    def create_line(length: int):
        line = ''
        for i in range(i_max - 2):
            r = random.randrange(0, 10000)
            if r > 10000 - 10000 // inv_freq:
                line += 'B'
            else:
                line += '.'
        return f'|{line}|'

    if j_max < 3:
        print(f'j_max cannot be less than 3')
        return None
    if i_max < 3:
        print(f'i_max cannot be less than 3')
        return None
    map_blueprint = ''
    s = f'{create_border_line(i_max)}'
    for j in range(j_max - 2):
        map_blueprint += f'{create_line(i_max)}\n'
    return f'{s}\n{map_blueprint}{s}'


game_map_huge = f'''{create_map_blueprint(25, 25, 55)}'''
print(f'{game_map_huge}')


# print(play_flou(game_map_1))
# print(play_flou(game_map_2))
# print(play_flou(game_map_3))
# print(play_flou(game_map_v))
print(play_flou(game_map_huge))

# print(f'{[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][1:-1]}')
# print(f'{[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:3]}')

# make_grid_from_blueprint(game_map_x)
