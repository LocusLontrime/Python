import time
from itertools import combinations as combs

class MineSweeper:
    # (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]

    def __init__(self, game_map: str, n: int):
        self.grid = self.make_grid_from_blueprint(game_map)
        self.mines_remained = n
        self.groups = []

    def solve(self):
        self.avalanche()   # the core:
        res = self.make_map_from_grid()  # string representation of res:
        self.show_grid()  # showing the grid:
        return '?' if '?' in res else res  # returning the result:

    def avalanche(self):
        while True:
            self.get_groups()  # get groups list from the current grid state:
            self.transform_groups()  # transforming groups according to the groups-addition rules:
            self.show_grid()  # showing the grid at the every step of the main avalanche cycle::
            # cells opening and flagging:
            if self.check_groups() == 0:
                # cells groups building:
                opened_cells = [(j, i) for i in range(len(self.grid[0])) for j in range(len(self.grid)) if '?' in [self.grid[c[0]][c[1]] for c in self.get_neighs((j, i))] and self.grid[j][i].isdigit()]
                closed_cells = [(j, i) for i in range(len(self.grid[0])) for j in range(len(self.grid)) if self.grid[j][i] == '?']
                neighbouring_closed_cells = list({cc for oc in opened_cells for cc in self.get_neighs(oc) if cc in closed_cells})
                # smart combs algorithm starts:
                cells_to_be_opened = []
                for ncc in neighbouring_closed_cells:
                    for mines_q in range(max(0, self.mines_remained - 1 - (len(closed_cells) - len(neighbouring_closed_cells))), min(self.mines_remained, len(neighbouring_closed_cells))):
                        poss_partitions = [list(comb) + [ncc] for comb in combs(neighbouring_closed_cells, mines_q) if ncc not in comb]
                        if self.check_combs(poss_partitions): break
                    else: cells_to_be_opened.append(ncc)  # the cell can be opened!
                # stop-condition (if no cell been flagged or opened) and there are no cells to be opened in smart section:
                cells_to_be_opened += closed_cells if self.mines_remained == 0 else []
                if self.mines_remained == len(closed_cells): self.flag(closed_cells)
                if len(cells_to_be_opened) == 0: break
                # opening phase:
                self.open(cells_to_be_opened)

    def open(self, cells):
        for (j, i) in cells:
            value = open(j, i)
            self.grid[j][i] = str(value)

    def flag(self, cells):
        for (j, i) in cells:
            self.mines_remained -= 1
            self.grid[j][i] = 'x'

    def check_combs(self, combs_list):
        for comb in combs_list:
            for group in self.groups:
                if group.val != len(group.group.intersection(comb)): break
            else: return 1

    def get_neighs(self, cell: tuple[int, int]):
        return [(cell[0] + dy, cell[1] + dx) for dy, dx in self.walk if self.is_cell_valid((cell[0] + dy, cell[1] + dx))]

    def is_cell_valid(self, cell: tuple[int, int]):
        return 0 <= cell[0] < len(self.grid) and 0 <= cell[1] < len(self.grid[0])

    def check_groups(self):
        return sum([group.check(self) for group in self.groups])

    def transform_groups(self):
        # starting a groups' transformation:
        while True:
            actions = 0
            for j in range(0, len(self.groups) - 1):
                i = j + 1
                while i < len(self.groups):
                    # significantly increases performance, 0-valued groups should be processed in check_groups() method instead of transform_groups one:
                    if self.groups[j].val != 0 and self.groups[i].val != 0:
                        actions += (k := self.groups[j].unify(self.groups[i], self.groups))
                        if k == 1: i -= 1  # case of deleting a group from groups' list:
                    i += 1
            if actions == 0: break # checks if there have been some transformation during the current step if no -->> breaks:

    def get_groups(self):
        # getting initials groups list:
        self.groups = []
        for j, row in enumerate(self.grid):
            for i, el in enumerate(row):
                if el.isdigit():
                    new_group = Group(int(el), (j, i))
                    new_group.get_closed_neighs(self.grid)
                    if len(new_group.group) > 0: self.groups.append(new_group)
    @staticmethod
    def make_grid_from_blueprint(game_map: str):
        return [[cell for cell in row.split(' ')] for row in game_map.split('\n')]

    def make_map_from_grid(self):
        return "\n".join([f'{" ".join(row)}' for row in self.grid])

    def show_grid(self):
        for row in self.grid:
            for cell in row:
                if type(cell) == str:
                    if cell == '?':
                        print("\033[35m{}".format('?'), end='')
                        print("\033[0m{}".format(' '), end='')
                    elif cell == 'x':
                        print("\033[31m{}".format('x'), end='')
                        print("\033[0m{}".format(' '), end='')
                    else:
                        print("\033[32m{}".format(cell), end='')
                        print("\033[0m{}".format(' '), end='')
                else:
                    print(f'{cell}', end=' ')
            print()
        print()


class Group:
    def __init__(self, val: int, cell=None):
        self.val = val
        self.group = set()
        self.cell = cell

    def get_closed_neighs(self, grid):
        for direction in MineSweeper.walk:
            new_j, new_i = self.cell[0] + direction[0], self.cell[1] + direction[1]
            if 0 <= new_j < len(grid) and 0 <= new_i < len(grid[0]):
                if grid[new_j][new_i] == '?': self.group.add((new_j, new_i))
                elif grid[new_j][new_i] == 'x': self.val -= 1

    # check group after groups transformation:
    def check(self, mine_sweeper):
        if self.val == 0:
            # opening all mines:
            for cell in self.group:
                if mine_sweeper.grid[cell[0]][cell[1]] == '?':
                    MineSweeper.open(mine_sweeper, [cell])
            return 1
        elif self.val == len(self.group):
            # flagging all mines found
            for cell in self.group:
                if mine_sweeper.grid[cell[0]][cell[1]] == '?':
                    MineSweeper.flag(mine_sweeper, [cell])
            return 1
        return 0

    def __eq__(self, other: 'Group'):
        return self.group == other.group

    def __isub__(self, other: 'Group'):
        # validity check in outer methods
        self.group -= other.group
        self.val -= other.val

    # core method of groups' unifying:
    def unify(self, other: 'Group', groups):
        # 1. if two groups are the same -->> one of them (other) should be removed:
        if self == other:
            groups.remove(other)
            return 1
        # 2. if one of two groups contains another one --> we subtract a less group from a larger one:
        larger_g, less_g = (self, other) if len(self.group) > len(other.group) else (other, self)
        if less_g.group.issubset(larger_g.group):
            larger_g -= less_g
            return 2
        # 3. if two groups have some common elements:
        else:
            larger_g, less_g = (self, other) if self.val > other.val else (other, self)
            common_g = self.group.intersection(other.group)
            # the condition of simplifiability:
            if larger_g.val - (len(larger_g.group) - len(common_g)) == less_g.val:
                new_group = Group(less_g.val)
                new_group.group = common_g
                larger_g -= new_group
                less_g -= new_group
                groups.append(new_group)
                return 3
        return 0

class Cell:
    def __init__(self, j, i):
        self.j, self.i = j, i
        self.neighs = []

    def get_neighs(self):
        pass

    def __eq__(self, other):
        return self.j, self.i == other.j, other.i

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return f'{self.j, self.i}'

    def __repr__(self):
        return str(self)


def get_ms(t1, t2):
    return (t2 - t1) // 10 ** 6


g1 = """
0 0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? 0 0
0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 ? ? ? 0
? ? ? 0 0 0 0 ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 ? ? ? 0
? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 ? ?
? ? ? ? ? 0 0 ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ?
? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 ? ?
? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 ? ? ? 0 0 ? ?
0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0
0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0
0 0 ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0
0 ? ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ?
0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ?
0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ?
0 0 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? 0 ? ? ? 0 0 0 0 0 0 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0
? ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 ? ? ? ? ? ? ? ? ? 0
0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 0
0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0
""".strip()


s1 = """
0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 2 1 1 0 0
0 0 1 1 1 1 1 1 0 1 1 1 1 1 1 0 0 1 x 2 2 x 1 1 x 2 x 1 0 0
0 0 0 0 0 1 x 1 0 1 x 1 1 x 1 0 0 1 2 4 x 3 1 1 1 2 2 2 1 0
1 1 0 0 0 1 1 1 0 1 1 1 2 3 3 1 0 0 1 x x 2 0 0 0 0 1 x 1 0
x 2 1 0 0 0 0 1 1 2 1 1 1 x x 1 0 0 1 2 2 1 0 0 0 0 1 1 1 0
3 x 4 2 1 0 0 1 x 2 x 1 1 2 2 1 0 0 0 0 0 0 0 0 1 1 1 0 1 1
3 x x x 1 0 0 1 1 2 1 1 0 0 0 0 0 0 0 1 1 1 0 0 1 x 1 0 2 x
x 4 4 3 1 0 0 0 0 0 1 1 1 0 0 1 1 1 0 1 x 1 0 1 2 2 1 0 2 x
1 2 x 1 0 0 0 1 1 1 2 x 3 2 1 2 x 1 0 1 1 1 0 1 x 1 0 0 1 1
0 1 1 1 0 0 0 1 x 1 2 x x 2 x 2 2 2 1 0 0 0 0 1 1 1 0 0 0 0
0 0 1 1 1 0 0 1 1 1 1 2 2 2 1 1 1 x 1 0 0 0 0 0 0 1 1 1 0 0
0 0 1 x 1 0 0 0 0 0 1 1 2 1 1 0 1 1 1 1 2 2 1 1 1 2 x 1 0 0
0 1 2 2 1 0 0 0 0 0 1 x 2 x 1 0 0 0 0 1 x x 2 1 x 2 1 2 1 1
0 1 x 1 0 0 0 1 1 1 1 1 2 1 1 0 1 1 1 1 4 x 3 1 1 1 0 1 x 1
0 1 1 1 0 0 0 1 x 2 1 0 0 0 0 0 1 x 1 0 2 x 2 0 0 0 0 1 1 1
0 0 0 0 0 0 1 2 3 x 1 0 0 0 0 1 2 2 1 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 1 2 x 2 1 1 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 x 2 1 1 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 1 1 1 0 0
0 0 1 2 x 3 2 1 0 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 2 x 2 0 0
0 0 1 x 3 3 x 1 0 0 0 0 0 0 1 2 2 1 0 0 0 0 1 x 1 2 x 2 0 0
1 1 1 1 2 x 2 1 0 0 0 0 0 0 1 x 1 0 0 1 1 2 2 2 1 1 1 1 1 1
x 3 2 1 1 1 1 0 0 0 0 0 0 1 3 3 3 1 1 1 x 2 x 1 0 0 1 1 2 x
2 x x 1 0 0 0 0 0 0 0 0 0 1 x x 2 x 1 1 2 3 2 2 1 1 1 x 2 1
1 2 2 2 1 1 0 0 0 0 0 0 0 1 2 3 3 2 1 0 1 x 1 1 x 1 1 1 1 0
0 0 0 1 x 1 0 0 0 0 0 0 0 0 1 3 x 2 0 0 1 1 1 1 1 2 1 1 0 0
0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 x x 2 0 0 0 0 0 0 0 1 x 1 0 0
""".strip()


g = """
0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0
? ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0
? ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? ?
? ? ? ? ? ? ? ? 0 0 ? ? ? 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ?
? ? 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 0 0 ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0
? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0
? ? 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0 0 0 0
? ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 0 0 0 0
""".strip()

s = """
0 0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 1 1 1 1 1 x 1 1 1 1 0 0
1 1 1 2 2 2 1 1 0 0 1 1 1 0 0 0 1 1 1 1 x 1 1 1 1 1 x 1 0 0
x 2 1 x 1 1 x 1 0 0 1 x 1 0 0 0 0 0 0 1 1 1 0 0 0 1 1 2 1 1
x 2 1 1 1 1 1 1 0 0 1 1 1 0 1 1 1 0 0 0 0 0 0 0 0 1 1 2 x 1
1 1 0 1 2 2 1 0 0 0 1 2 2 1 1 x 2 1 1 2 2 2 1 1 0 1 x 2 1 1
0 0 0 1 x x 2 0 0 1 3 x x 1 1 2 x 1 1 x x 2 x 1 0 1 1 1 0 0
1 1 0 1 3 x 2 0 0 1 x x 3 2 1 2 1 1 1 3 3 3 1 1 0 0 0 0 0 0
x 1 0 0 1 1 1 0 0 1 2 2 1 1 x 1 0 0 0 1 x 2 1 0 0 0 0 0 0 0
1 2 1 1 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 1 2 x 1 0 0 0 0 0 0 0
0 1 x 1 0 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0
""".strip()

# g = """
#
# """.strip()
#
# s = """
#
# """.strip()

# g = """
#
# """.strip()
#
# s = """
#
# """.strip()

# g = """
#
# """.strip()
#
# s = """
#
# """.strip()

# g = """
#
# """.strip()
#
# s = """
#
# """.strip()

# g = """
#
# """.strip()
#
# s = """
#
# """.strip()

# g = """
#
# """.strip()
#
# s = """
#
# """.strip()

def solve_mine(game_map: str, n: int):
    return MineSweeper(game_map, n).solve()

# built in method for tests at codewars.com:
def open(j: int, i: int):
    grid_in = MineSweeper.make_grid_from_blueprint(s)
    if (g := grid_in[j][i]) == 'x':
        raise Exception(f'BOOM!!! {j, i}')
    elif g == '?':
        Exception('NON-SOLVABLE CELL opening!!!')
    else:
        return int(g)

ms = MineSweeper(g, s.count('x'))
print(f'INITIAL GRID: ')
MineSweeper.show_grid(ms)
print(f'SOLUTION: ')
MineSweeper.show_grid(ms)
start = time.time_ns()
print(ms.solve())
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')



q = None
if q:
    print('LALA')














