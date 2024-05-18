# accepted on codewars.com
import time
from collections import defaultdict as d

walk = ((0, 1), (1, 0), (0, -1), (-1, 0))
dir_names = ['R', 'D', 'L', 'U']

# aux:
counter: int
good_positions: int
already_hashed_figs_counter: int
rec_counter: int
unique_fold_counter: int
t1: int
t2: int
t3: int
t4: int


class Figure:
    """class representing a current figure state"""

    def __init__(self, symbol: str, ind: int):
        # main pars:
        self.name = symbol
        self.cells: set[tuple[int, int]] = set()
        # coords milestones:
        self.j_max = None
        self.j_min = None
        self.i_max = None
        self.i_min = None
        # auxiliary pars:
        self._hash_ = 0
        self._ind = ind
        self._moves = []

    def add_cell(self, j: int, i: int):
        """appends a cell to the list"""
        self.cells |= {(j, i)}

    def add_cells(self, cells: set[tuple[int, int]], powers: list[int], i_max: int) -> None:
        """appends a set of cell to the list, redefines max and min coords and recomputes the figure's hash"""
        self.cells |= cells
        self.setup()
        # hash changing:
        # important! 0 means empty space therefore figures' indices must start from 1; we numerate them starting from 0,
        # but add 1 to each of them in the formula below:
        self._hash_ += (self._ind + 1) * sum(powers[j_ * i_max + i_] for j_, i_ in cells)

    def move(self, dir_: int):
        """adds the current move to the figure's list of moves"""
        self._moves.append(f'{self.name}{dir_names[dir_]}')

    @property
    def moves(self):
        return self._moves

    @property
    def hash(self):
        return self._hash_

    @property
    def size(self):
        return len(self.cells)

    def setup(self):
        """redefines j_max, j_min, i_max, i_min"""
        self.j_max = max(self.cells, key=lambda k: k[0])[0]
        self.j_min = min(self.cells, key=lambda k: k[0])[0]
        self.i_max = max(self.cells, key=lambda k: k[1])[1]
        self.i_min = min(self.cells, key=lambda k: k[1])[1]

    def copy(self) -> 'Figure':
        """makes a deep copy of the current Figure state"""
        # creates a new figure at first:
        f_copied = Figure(self.name, self._ind)
        # copies the figure's cells:
        f_copied.cells |= self.cells
        # then copies coords milestones:
        f_copied.j_max = self.j_max
        f_copied.j_min = self.j_min
        f_copied.i_max = self.i_max
        f_copied.i_min = self.i_min
        # finally, copies auxiliary pars:
        f_copied._hash_ = self._hash_
        f_copied._moves += self._moves
        # returns the copy made:
        return f_copied

    # for testing and representing only:
    def __str__(self):  # 36 366 98 989 98989 LL
        return f'<{self.size}>[j:{self.j_max, self.j_min} | i:{self.i_max, self.i_min}]({self.moves})'

    def __repr__(self):
        return str(self)


def solver(grid: tuple[str, ...]):
    """main method for the task solving"""  # 36 366 98 989 98989 LL
    global rec_counter, unique_fold_counter, counter, good_positions, already_hashed_figs_counter, t1, t2, t3, t4
    print(f'{grid = }')
    # let us reformat the board a bit:
    board = [[ch for ch in s] for s in grid]
    print_board(grid)
    # searching for all the figures on the board, shaping visited set:
    visited = set()
    figures: dict[str, Figure] = {}
    j_max, i_max = len(board), len(board[0])
    f_ind = 0
    for j in range(j_max):
        for i in range(i_max):
            if (ch := board[j][i]).isalpha():
                visited.add((j, i))
                if ch not in figures.keys():  # 36 366 98 989 98989 LL
                    figures[ch] = Figure(ch, f_ind)
                    f_ind += 1
                figures[ch].add_cell(j, i)
    # sets up coords milestones for all the figures found:
    for figure in figures.values():
        figure.setup()
    # figures found showing:
    for k, v in figures.items():
        print(f'Figure: {k}')
        print(f'...pars: {v}')
    # recursive methods part:
    rec_counter = 0
    unique_fold_counter = 0
    figs = list(figures.values())
    # sorts figures in descending order (in terms of cells quantity):
    figs.sort(key=lambda x: -x.size)  # bottleneck of optimisation
    print(f'sorted figs = {[f.name for f in figs]}')
    base = len(figs) + 1  # base for hash calculating
    powers = [base ** (j * i_max + i) for j in range(j_max) for i in
              range(i_max)]  # precalculated powers for fast hashing
    print(f'{powers = }')
    print(f'{base = }')
    # finds all the possible sizes for every figure (in terms of the only space)
    print(f'initial_size: {j_max * i_max}')
    figs_sizes = []
    for f in figs:
        f_sizes = []
        size_ = f.size
        while size_ <= j_max * i_max:
            f_sizes += [size_]
            size_ *= 2
        figs_sizes += [f_sizes]
    print(f'{figs_sizes = }')
    # check for the possible sizes combs:
    counter = 0
    good_positions = 0
    t1 = time.time_ns()
    res_dict = rec_seeker(initial_size := j_max * i_max, figs_sizes)
    t2 = time.time_ns()
    print(f'{res_dict = }')
    # figs folding, building shapes list (possible shapes for the every figure):
    shapes = []
    already_hashed_figs_counter = 0
    for fig in figs:
        figures_ = d(list)
        rec_fig_seeker(initial_size, fig, visited, board, powers, j_max, i_max, set(), figures_)
        shapes.append(figures_)
        # print(f'{fig.name} shapes quantity: {len(figures_)}')
        # for k, v in figures_.items():
        #     print(f'->shapes of a size {k}')
        #     for n, shape in enumerate(v):
        #         print(f'...{n + 1} | size: {shape.size}')
        #         print_fig(shape, board, j_max, i_max)
    t3 = time.time_ns()
    # now we should connect shapes with space constraints to the possible full placement:
    print(f'rec connecting:')
    result = rec_connector(j_max * i_max, 0, shapes, set(), board, res_dict, j_max, i_max, [fig.size for fig in figs],
                           [])
    t4 = time.time_ns()
    # result processing:
    if result is None:
        print(f'NO SOLUTION...')
        return None
    else:
        print(f'A SOLUTION EXISTS')
    # showing the result board:
    print_figures(result, board, j_max, i_max)
    # returns the moves:
    return sum([f.moves for f in result], start=[])


def fold(figure: Figure, visited: set[tuple[int, int]], powers: list[int], j_max: int, i_max: int,
         dir_: int) -> tuple:
    """tries to fold the figure in the direction chosen"""

    def dist(x):
        return 2 * f_borders[dir_] - x + (1 if dir_ < 2 else -1)

    def cyclic_shift_left(arr_, delta: int) -> list:
        return arr_[delta:] + arr_[:delta]

    # print(f'folding figure {figure.name} in the dir of {direction}')
    global unique_fold_counter
    f_borders = [figure.i_max, figure.j_max, figure.i_min, figure.j_min]
    maxes = [i_max, j_max]
    new_cells = {cyclic_shift_left((coords[dir_ % 2], dist(coords[(dir_ + 1) % 2])), dir_ % 2)
                 for coords in figure.cells} if (0 <= dist(f_borders[(dir_ + 2) % 4]) < maxes[dir_ % 2]) else set()
    # validation:
    if len(figure.cells) != len(new_cells) or new_cells.intersection(visited):
        # empty set for the case of invalid move:
        return ()
    unique_fold_counter += 1
    f_copy = figure.copy()
    f_copy.add_cells(new_cells, powers, i_max)
    f_copy.move(dir_)
    return f_copy, new_cells


def rec_seeker(cells_rem: int, figs_sizes: list[list[int]], fig_ind: int = 0) -> dict:
    global counter, good_positions
    counter += 1
    res = {}
    # border case:
    if cells_rem == 0 and fig_ind == len(figs_sizes):
        good_positions += 1
        return {0: True}
    # if we still are not out of bounds:
    if fig_ind < len(figs_sizes):
        for size_ in figs_sizes[fig_ind]:
            if cells_rem - size_ >= 0:
                # next fig index recursive call:
                dict_ = rec_seeker(cells_rem - size_, figs_sizes, fig_ind + 1)
                if dict_:
                    res[size_] = dict_
    return res


def rec_fig_seeker(rem_cells: int, fig: Figure, visited: set[tuple[int, int]], board,
                   powers: list[int], j_max: int, i_max: int, hashes: set[int], figures: d[int, list[Figure]]):
    global already_hashed_figs_counter
    # print(f'{fig}')
    # print_fig(fig, board, j_max, i_max)
    if rem_cells >= 0:
        # if a figure has not been already hashed:
        if fig.hash not in hashes:
            # hashing figure:
            hashes |= {fig.hash}
            # adding the figure to the figures list:
            figures[fig.size] += [fig]
            for dir_ in range(4):
                # tries to fold the figure in the direction chosen:
                if info := fold(fig, visited, powers, j_max, i_max, dir_):
                    fig_, new_cells = info
                    # recursive call:
                    rec_fig_seeker(rem_cells - len(new_cells), fig_, visited | new_cells, board, powers, j_max, i_max,
                                   hashes, figures)
        else:
            already_hashed_figs_counter += 1


def rec_connector(rem_cells: int, ind: int, shapes: list[d[int, list[Figure]]], visited, board, res_dict, j_max, i_max,
                  sizes, figs):
    global rec_counter
    rec_counter += 1
    if rec_counter % 100_000 == 0:
        print(f'{rec_counter = }')
    # print(f'{rem_cells = } | {ind = }')
    # base case:
    if rem_cells == 0:
        print(f'resulted figs: ')
        for f in figs:
            print(f'{f.name} -> {f.moves = }')
            print_fig(f, board, j_max, i_max)
        return figs
    if ind < len(shapes):
        # res_dict, then shapes a bit faster than vice versa...
        for shape_size in sorted(res_dict.keys(),
                                 reverse=True):  # we can omit sorting, but dict can violate the order of key-sizes...
            if shape_size in shapes[ind].keys():  # res_dict.keys():
                for shape in shapes[ind][shape_size]:
                    if not shape.cells.intersection(visited):
                        interim_res = rec_connector(rem_cells - shape.size, ind + 1, shapes, visited | shape.cells,
                                                    board, res_dict[shape_size], j_max, i_max, sizes, figs + [shape])
                        if interim_res is not None:
                            return interim_res
    return None


def print_board(board, shift: int = 0):
    print(f'Board: ')
    for row_ in board:
        print(f'|{" " * shift}{row_}|')


def print_fig(fig: Figure, board: list[list[str]], j_max: int, i_max: int):
    # print(f'fig -> {fig.name}')
    print(f'       ' + f'-' * i_max)
    for j in range(j_max):
        print(f'      |', end='')
        for i in range(i_max):
            print(f'{fig.name if (j, i) in fig.cells else " "}', end='')
        print(f'|')
    print(f'       ' + f'-' * i_max)


def print_figures(figures: list[Figure], board: list[list[str]], j_max: int, i_max: int):
    for fig in figures:
        for j, i in fig.cells:
            board[j][i] = fig.name
    print(f'result board: ')
    print(f' ' + f'-' * i_max)
    for row in board:
        string_ = ''.join(row)
        print(f'|', end='')
        print(f'{string_}', end='')
        print(f'|')
    print(f' ' + f'-' * i_max)


def print_res_dict(res_dict: dict):
    """a very suspicious method..."""

    def print_res_dict_(res_dict_: dict, shift: int = 0):
        if isinstance(res_dict_, dict):
            for k, dict_ in res_dict_.items():
                print(f' ' * shift + f'{{{k}: ')
                print_res_dict_(dict_, shift + 2)
                print(f' ' * shift + f'}}')
        else:
            print(f' ' * shift + f'{res_dict_}')

    print_res_dict_(res_dict)


s_ = (
    'AAA   ',
    ' A    ',
    '   B B',
    '      ',
    '  C D ',
    '      ',
)
s_x = (
    '    ',
    '    ',
    '  A ',
    '  A ',
    ' B  ',
    ' B  ',
    '    ',
    '    '
)
s_xx = (
    '   A',
    ' B  ',
    '    ',
    '    ',
    '    '
)
s_xxx = (
    '    ',
    ' A  ',
    '  B ',
    '    ',
    ' C  ',
    '    ',
    '    '
)
s_xxxx = (
    '      ',
    ' A    ',
    '   B  ',
    '      ',
    '  C   ',
    '      '
)  # False
s_m = (
    '  A       ',
    'BB   CD   ',
    '  A     E ',
    '        E ',
    '   F      ',
    '        G ',
    '          ',
    '          '
)  # False
s_k = (
    '     A  ',
    '      B ',
    '        ',
    'C   D  E',
    '        ',
    '        ',
    '        ',
    '        ',
)

s_l = '        \n R   N  \n        \n        \n  SS    \n I S    \n     XX \n        \n       L'

s_l = tuple(s for s in s_l.split('\n') if s)

s_mega = '            \n            \n         X  \nDDDD        \n            \n            \n    JJ      \n            \n            \n         C  \n            \n  A         '

s_mega_ = (
    '            ',
    '            ',
    '         X  ',
    'DDDD        ',
    '            ',
    '            ',
    '    JJ      ',
    '            ',
    '            ',
    '         C  ',
    '            ',
    '  A         ',
)

s_super = (
    '       X    JJ  ',
    '            JJ  ',
    'FFF             ',
    'FFF             ',
    '                ',
    '                ',
    '  HH            ',
    '              S ',
    '                ',
    '    TT          ',
    '                ',
    '                ',
    '            YYYY',
    '                ',
    '                ',
    'AA              ',)

s_susp = (
    '        X ',
    '          ',
    'Y  Z  W  W',
    '  ZZ      ',
    '          ',
    '      W  W',
    '     U    ',
    '          '
)

s_mega = tuple(s for s in s_mega.split('\n') if s)

s_g = '      FF\n        \n P   S Y\n     S Y\n H S Z  '

s_g = tuple(s for s in s_g.split('\n') if s)

s_great = '   QQ       \n L QQ       \n            \n       U K  \nZ Z         \n            \n            \n            '
s_great = tuple(s for s in s_great.split('\n') if s)

s_huge = '   S        \n            \n          J \n          J \n   H H      \n            \n            \nM M D       \n M D D      \n    D K K   '
s_huge = tuple(s for s in s_huge.split('\n') if s)

s_extra = '        \n        \n        \nC CC    \n        \n        \n      J \n V      \n        \n        \n        \n A      '
s_extra = tuple(s for s in s_extra.split('\n') if s)

s_tera = '            \n            \n  X      O  \n            \n            \n            \n     J      \n     J      \n        L   \nG       L   \n        L   \n        L   '
s_tera = tuple(s for s in s_tera.split('\n') if s)

s_no = '  CL  \n  LL  \n      \n      \n      \n    MM\n X I M\n  II  '
s_no = tuple(s for s in s_no.split('\n') if s)

s_no_way = '      RRRR  \n        RR  \n      Y     \nHH        HH\n         OO \n            \n        I   \n   ZZZ  I   '
s_no_way = tuple(s for s in s_no_way.split('\n') if s)

s_giga = '          \n    I     \n  AA A    \n          \n          \n          \n G     Y  \n          \nM       S \n          '
s_giga = tuple(s for s in s_giga.split('\n') if s)

s_new = '         \nQQQ      \n         \n      BBB\n         \n      FFF\nW    N   \n     N   \n  I      \n  I      \n         \n         '
s_new = tuple(s for s in s_new.split('\n') if s)

s_exa = '         H  \n            \n  Z         \n            \n            \n      MM    \n            \n            \n        DDDD\n  N         \n            \n            '
s_exa = tuple(s for s in s_exa.split('\n') if s)

s_zero = '    FF  BB\n JJ F   BB\n  JC     B\nJ CC      \n V        \nVV   VV   \n     VVX  \n      XX  '
s_zero = tuple(s for s in s_zero.split('\n') if s)

s_none = '   O  MMM   \n   O        \n            \n KK         \nRR        RR\n     V      \n  CC        \n  CCCC      '
s_none = tuple(s for s in s_none.split('\n') if s)  # 36 366 98 989 98989 LL

s_smth = '          \n Q    M   \nKQ    M   \nKK        \n          \n        C \n L   O    \n          '
s_smth = tuple(s for s in s_smth.split('\n') if s)

start = time.time_ns()
print(f'moves: {solver(s_giga)}')
# counter = 0
# good_positions = 0
# result_d = rec_seeker(100, [[9, 18, 36, 72], [1, 2, 4, 8, 16, 32, 64], [25, 50, 100], [1, 2, 4, 8, 16, 32, 64]], 0)
# print(f'{result_d = }')
# print_res_dict(result_d)
finish = time.time_ns()

# rec_counter = 0
# start = time.time_ns()
# # f_sizes = rec_seeker(80 - 10, [2, 2, 1, 1, 2, 1, 1])
# # f_sizes = rec_seeker(120 - 9, [1, 4, 2, 1, 1])
# f_sizes = rec_seeker(80 - 5, [1, 1, 1, 1, 1])
# finish = time.time_ns()
print(f'{counter = }')
print(f'{good_positions = }')
print(f'{unique_fold_counter = }')  # 36 366 98 989 98989 LL
print(f'{already_hashed_figs_counter = }')
print(f'{rec_counter = }')
print(f'poss ways time elapsed: {(t2 - t1) // 10 ** 6} milliseconds')
print(f'rec figs time elapsed: {(t3 - t2) // 10 ** 6} milliseconds')
print(f'rec connecting time elapsed: {(t4 - t3) // 10 ** 6} milliseconds')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
#
# print(f'sizes length: {len(f_sizes)}')

# print(f'f_sizes: ')
# for row in f_sizes:
#     print(f'{row}')

# print(f'{math.log2(16 / 9) == int(math.log2(16 / 9))}')

# 295220129939960414271
# 2804589813513781821503


# class F:
#     def __init__(self, val: int):
#         self.val = val
#
#     def __str__(self):
#         return f'F[{self.val}]'
#
#     def __repr__(self):
#         return str(self)
#
#
# array = [F(1), F(2), F(3), F(4), F(5)]
# k_ = array[3]
# print(f'{k_}')
# array[3].val = 98
# print(f'{k_}')

# TODO: 1. decide whether figure hashing still needed... verdict: needed +
# TODO: 2. optimise poss ways and rec connecting methods a bit...
