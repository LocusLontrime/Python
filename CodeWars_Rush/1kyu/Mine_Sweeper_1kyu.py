# accepted on codewars.com
import time
from itertools import combinations as combs


# (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)
directions = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]
groups: list['Group']
grid: list[list['str']]
stop_flag: bool
mines_remained: int
get_groups_time: int
transform_time: int
check_groups_time: int
smart_check_combs_time: int

def solve_mine(game_map: str, n: int):
    global grid, groups, stop_flag, mines_remained, get_groups_time, transform_time, check_groups_time, smart_check_combs_time
    mines_remained = n
    # building a grid from game map:
    grid = make_grid_from_blueprint(game_map)
    get_groups_time, transform_time, check_groups_time, smart_check_combs_time = 0, 0, 0, 0
    # the core:
    avalanche()
    res = make_map_from_grid(grid)
    if res.count('?') == mines_remained:
        res.replace('?', 'x')
    # returning the result:
    return '?' if '?' in res else res

def get_degrees_of_freedom():
    return len([1 for row in grid for j in row if j == '?']) - mines_remained

def avalanche():
    global get_groups_time, transform_time, check_groups_time, smart_check_combs_time
    while True:
        # get groups list from the current grid state:
        get_groups()
        transform_groups()
        # cells opening and flagging:
        if check_groups() == 0:
            # cells groups building:
            opened_cells = [(j, i) for i in range(len(grid[0])) for j in range(len(grid)) if '?' in [grid[c[0]][c[1]] for c in get_neighs((j, i))] and grid[j][i].isdigit()]
            closed_cells = [(j, i) for i in range(len(grid[0])) for j in range(len(grid)) if grid[j][i] == '?']
            neighbouring_closed_cells = list({cc for oc in opened_cells for cc in get_neighs(oc) if cc in closed_cells})
            # smart combs algorithm starts:
            cells_to_be_opened = []
            for ncc in neighbouring_closed_cells:
                for mines_q in range(max(0, mines_remained - 1 - (len(closed_cells) - len(neighbouring_closed_cells))), min(mines_remained, len(neighbouring_closed_cells))):
                    poss_partitions = [list(comb) + [ncc] for comb in combs(neighbouring_closed_cells, mines_q) if ncc not in comb]
                    if check_combs(poss_partitions):
                        break
                else:
                    cells_to_be_opened.append(ncc)
            # stop-condition (if no cell been flagged or opened) and there are no cells to be opened in smart section:
            # check:
            if mines_remained == 0:
                cells_to_be_opened += closed_cells
            elif mines_remained == len(closed_cells):
                for (j, i) in closed_cells:
                    flag((j, i))
            if len(cells_to_be_opened) == 0:
                break
            # opening phase:
            for (j, i) in cells_to_be_opened:
                value = open(j, i)
                grid[j][i] = str(value)

def check_combs(combs_list):
    for comb in combs_list:
        for group in groups:
            if group.val != len(group.group.intersection(comb)):
                break
        else:
            return True
    return False

def get_neighs(cell: tuple[int, int]):
    return [(cell[0] + dy, cell[1] + dx) for dy, dx in directions if is_cell_valid((cell[0] + dy, cell[1] + dx))]

def is_cell_valid(cell: tuple[int, int]):
    return 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0])

def get_ms(t1, t2):
    return (t2 - t1) // 10 ** 6

def check_groups():
    global groups
    outer_counter = 0
    for group in groups:
        outer_counter += group.check()
    return outer_counter

def transform_groups():
    global groups, stop_flag
    # starting a groups' transformation:
    while True:
        stop_flag = True
        for j in range(0, len(groups) - 1):
            i = j + 1
            while i < len(groups):
                # print(f'j, i: {j, i}, group[{j}] -->> {groups[j]}, group[{i}] -->> {groups[i]}]')
                # significantly increases performance, 0-valued groups should be processed in check_groups() method instead of transform_groups one:
                if groups[j].val != 0 and groups[i].val != 0:
                    if groups[j] + groups[i]:
                        # case of deleting a group from groups' list:
                        i -= 1
                i += 1
        # checks if there have been some transformation during the current step if no -->> breaks:
        if stop_flag:
            break

def get_groups():
    global groups
    # getting initials groups list:
    groups = []
    for j, row in enumerate(grid):
        for i, el in enumerate(row):
            if el.isdigit():
                new_group = Group(int(el), (j, i))
                new_group.get_closed_neighs()
                if len(new_group.group) > 0:
                    groups.append(new_group)

def flag(cell: tuple[int, int]):
    global grid, mines_remained
    mines_remained -= 1
    grid[cell[0]][cell[1]] = 'x'


class Group:
    def __init__(self, val: int, cell=None):
        self.val = val
        self.group = set()
        self.cell = cell

    def get_closed_neighs(self):
        global grid
        for direction in directions:
            new_j, new_i = self.cell[0] + direction[0], self.cell[1] + direction[1]
            if 0 <= new_j < len(grid) and 0 <= new_i < len(grid[0]):
                if grid[new_j][new_i] == '?':
                    self.group.add((new_j, new_i))
                elif grid[new_j][new_i] == 'x':
                    self.val -= 1

    # check group after groups transformation:
    def check(self):
        global groups, grid
        counter = 0
        if self.val == 0:
            for cell in self.group:
                if grid[cell[0]][cell[1]] == '?':
                    value = open(cell[0], cell[1])
                    grid[cell[0]][cell[1]] = str(value)
            counter = 1
        elif self.val == len(self.group):
            # flagging all mines found
            for cell in self.group:
                if grid[cell[0]][cell[1]] == '?':
                    flag(cell)
            counter = 1
        return counter

    def __eq__(self, other: 'Group'):
        return self.group == other.group

    def __ne__(self, other: 'Group'):
        return not (self == other)

    def __str__(self):
        return f'{self.cell}, {self.val}: {self.group}'

    def __repr__(self):
        return str(self)

    def __isub__(self, other: 'Group'):
        # validity check in outer methods
        self.group -= other.group
        self.val -= other.val

    # core method of groups' unifying:
    def __add__(self, other: 'Group'):
        global groups, stop_flag
        # 1. if two groups are the same -->> one of them (other) should be removed:
        if self == other:
            groups.remove(other)
            return True
        # 2. if one of two groups contains another one --> we subtract a less group from a larger one:
        larger_g, less_g = (self, other) if len(self.group) > len(other.group) else (other, self)
        if less_g.group.issubset(larger_g.group):
            larger_g -= less_g
            stop_flag = False
            return False
        # 3. if two groups have some common elements:
        else:
            larger_g, less_g = (self, other) if self.val > other.val else (other, self)
            common_g = self.group.intersection(other.group)
            if larger_g.val - (len(larger_g.group) - len(common_g)) == less_g.val:
                new_group = Group(less_g.val)
                new_group.group = common_g
                larger_g -= new_group
                less_g -= new_group
                groups.append(new_group)
            return False

def make_grid_from_blueprint(game_map: str):
    return [[cell for cell in row.split(' ')] for row in game_map.split('\n')]

def make_map_from_grid(grid_in: list[list[str]]):
    return "\n".join([f'{" ".join(row)}' for row in grid_in])







