# accepted on codewars.com
import functools
import time
from collections import defaultdict as d

is_debug = False

# styles:
BOLD = "\033[1m"
# colours:
BLACK = "\033[30m{}"
RED = "\033[31m{}"
GREEN = "\033[32m{}"
YELLOW = "\033[33m{}"
BROWN = "\033[34m{}"
PURPLE = "\033[35m{}"
CYAN = "\033[36m{}"
X = "\033[37m{}"
END = "\033[0m"
COLOURS = [BLACK, RED, GREEN, YELLOW, BROWN, PURPLE, CYAN, X]


# non_recursive timer decorator:
def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start_ = time.perf_counter()
        f = func(*args, **kwargs)
        runtime = round(1000 * (time.perf_counter() - start_), 2)
        print(f'{_wrapper.__name__} time elapsed: {runtime} milliseconds')
        _wrapper.time_elapsed = runtime
        return f

    return _wrapper


# depth and calls for recursive function (slows a lot):
def counted(func):
    def reset():
        _wrapper.rec_depth = 0
        _wrapper.rec_calls = 0

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        nonlocal _depth
        # depth and calls incrementation:
        _depth += 1
        _wrapper.rec_calls += 1
        # max depth defining:
        _wrapper.rec_depth = max(_wrapper.rec_depth, _depth)
        f = func(*args, **kwargs)
        # depth backtracking:
        _depth -= 1
        return f

    print(f"I am a {func.__name__}'s decorator!!!")
    # starts a wrapper:
    _depth = 0
    reset()
    return _wrapper if is_debug else func


def get_rec_counter(func) -> tuple[int, int] | str:
    return (func.rec_calls, func.rec_depth) if 'rec_calls' in func.__dict__.keys() else '(->not in debug mode<-)'


class Figure:
    """class representing a current figure state"""
    dir_names = ['R', 'D', 'L', 'U']
    attrs = ['i_max', 'j_max', 'i_min', 'j_min']

    # a bit of optimisation (no)...
    __slots__ = ['name', '_ind', 'j_max', 'j_min', 'i_max', 'i_min', '_hash_', 'cells', '_moves']

    # for copy section:
    _copyable = __slots__[2:-2]

    def __init__(self, symbol: str, ind: int):
        # main pars:
        self.name = symbol
        self.cells: set[tuple[int, int]] = set()
        # coords milestones:
        self.j_max = None  # can be implemented as list: [..., ..., ..., ...]
        self.j_min = None
        self.i_max = None
        self.i_min = None
        # auxiliary pars:                                                             # 36 366 98 989 98989 LL
        self._hash_ = 0
        self._ind = ind
        self._moves = []

    def add_cell(self, j: int, i: int) -> None:
        """appends a cell to the list"""
        self.cells |= {(j, i)}

    def add_cells(self, cells: set[tuple[int, int]], powers: list[int], i_max: int) -> None:
        """appends a set of cell to the list and recomputes the figure's hash"""
        self.cells |= cells
        # hash changing:
        # important! 0 means empty space therefore figures' indices must start from 1; we numerate them starting from 0,
        # but add 1 to each of them in the formula below:
        self._hash_ += (self._ind + 1) * sum(powers[j_ * i_max + i_] for j_, i_ in cells)

    def fold(self, visited: set[tuple[int, int]], powers: list[int], j_max: int, i_max: int,
             dir_: int) -> tuple:
        """tries to fold the figure in the direction chosen and returns a copy of the figure folded and the length of
        new_cells set if possible or empty tuple otherwise"""

        def dist(x: int) -> int:
            return 2 * self.f_borders[dir_] - x + (1 if dir_ < 2 else -1)  # 36 366 98 989 98989 LL

        def cyclic_shift_left(arr_: tuple | list, delta: int) -> tuple | list:
            return arr_[delta:] + arr_[:delta]

        # print(f'folding figure {figure.name} in the dir of {direction}')
        maxes = [i_max, j_max]
        new_cells = {cyclic_shift_left((coords[dir_ % 2], dist(coords[(dir_ + 1) % 2])), dir_ % 2)
                     for coords in self.cells} if (
                0 <= (new_extremum := dist(self.f_borders[(dir_ + 2) % 4])) < maxes[dir_ % 2]) else set()
        # validation:
        if len(self.cells) != len(new_cells) or new_cells.intersection(visited):
            # empty set for the case of invalid move:
            return ()

        # creates a copy of the figure and adds new cells to it:
        f_copy = self.copy()
        f_copy.add_cells(new_cells, powers, i_max)
        # setup milestones:
        setattr(f_copy, Figure.attrs[dir_], new_extremum)  # 36 366 98 989 98989 LL
        # makes a move:
        f_copy.move(dir_)
        # print(f'{f_copy.hash = }')
        return f_copy, len(new_cells)

    def move(self, dir_: int) -> None:
        """adds the current move to the figure's list of moves"""
        self._moves.append(f'{self.name}{Figure.dir_names[dir_]}')

    @property
    def moves(self):
        return self._moves

    @property
    def size(self):
        return len(self.cells)

    @property
    def f_borders(self):
        """returns array of coords milestones, attrs isn't used in order to prevent performance losses"""
        return [self.i_max, self.j_max, self.i_min, self.j_min]

    def setup(self) -> None:
        """redefines j_max, j_min, i_max, i_min"""
        extrema = [max, min]
        for q in range(4):
            i1, i2 = q // 2, (q + 1) % 2
            setattr(self, Figure.attrs[q], extrema[i1](self.cells, key=lambda k: k[i2])[i2])

    def copy(self) -> 'Figure':
        """makes a deep copy of the current Figure state"""
        # creates a new figure at first:
        f_copied = Figure(self.name, self._ind)
        # copies usual attrs:
        self.smart_core(f_copied, Figure._copyable)
        # a bit subtler copying:
        f_copied.cells |= self.cells
        f_copied._moves += self._moves
        # returns the copy made:
        return f_copied

    def smart_core(self, other: 'Figure', attributes: list[str]):
        """core for copying and restoring"""
        for attribute in attributes:
            setattr(other, attribute, getattr(self, attribute))

    # for compatibility with hashed structures like set and dict (also known as hash getter)...
    def __hash__(self):
        return self._hash_

    # for testing and representing only:
    def __str__(self):  # 36 366 98 989 98989 LL
        return f'<{self.size}>[j:{self.j_max, self.j_min} | i:{self.i_max, self.i_min}]({self.moves})'

    def __repr__(self):
        return str(self)


class Board:
    """class representing a game Board"""

    def __init__(self, grid: tuple[str, ...]):
        # 1. board-connected pars:
        # remakes the board a bit:
        self.board = [[ch for ch in s] for s in grid]
        print_board(grid)
        self.j_max, self.i_max = len(self.board), len(self.board[0])
        # 2. figure-connected pars:
        self.visited = set()
        self.figures: list[Figure] = []
        # 3. process some data:
        self.setup()
        # 4. aux-pars:
        self.base = len(self.figures) + 1  # base for hash calculating
        # ...precalculated powers for fast hashing:
        self.powers = [self.base ** (j * self.i_max + i) for j in range(self.j_max) for i in range(self.i_max)]
        print(f'{self.powers = }')
        print(f'{self.base = }')
        # 5. figs sizes:
        self.figs_sizes = []
        # ...figs folding, building shapes list (possible shapes for the every figure):
        self.shapes = []
        # 6. possible sizes dict (shortens dead ends in the recursive tree):
        self.res_dict = {}
        # 7. rec counters init:
        self.unique_fold_counter = 0
        self.already_hashed_figs_counter = 0
        self.good_positions = 0
        # 8. time constants:
        self.t1, self.t2, self.t3, self.t4 = 0, 0, 0, 0

    def setup(self):
        """init-outer logic"""
        self.scan()
        # figures found showing:
        for f in self.figures:
            print(f'Figure: {f.name}')
            print(f'...pars: {f}')
            print_fig(f, self.j_max, self.i_max)
        # sorts figures in descending order (in terms of cells quantity):
        self.figures.sort(key=lambda x: -x.size)  # bottleneck of optimisation
        print(f'sorted figs = {[f.name for f in self.figures]}')

    def scan(self) -> None:
        """searching for all the figures on the board, shaping visited set"""
        f_ind = 0
        figures = {}
        for j in range(self.j_max):
            for i in range(self.i_max):
                if (ch := self.board[j][i]).isalpha():
                    self.visited.add((j, i))
                    if ch not in figures.keys():  # 36 366 98 989 98989 LL
                        figures[ch] = Figure(ch, f_ind)
                        f_ind += 1
                    figures[ch].add_cell(j, i)
        # sets up coords milestones for all the figures found:
        for figure in figures.values():
            figure.setup()
        # writes data to self.figures:
        self.figures = [v for k, v in figures.items()]

    # the main solving method:
    @timer
    def solve(self):
        """tries to solve the board and finds solution if it exists"""
        self.t1 = time.time_ns()
        # finds the every possible folding for each figure:
        n = len(self.visited)
        for fig in self.figures:
            figures_ = d(list)
            self.rec_fig_seeker(self.j_max * self.i_max - n, fig, self.visited - fig.cells, set(), figures_)
            self.shapes.append(figures_)
            self.figs_sizes += [[_ for _ in figures_.keys()]]
            # print(f'{fig.name} shapes quantity: {len(figures_)}')
            # for k, v in figures_.items():
            #     print(f'->shapes of a size {k}')
            #     for n, shape in enumerate(v):
            #         print(f'...{n + 1} | size: {shape.size}')
            #         print_fig(shape, self.j_max, self.i_max)
        self.t2 = time.time_ns()
        print(f'possible {self.figs_sizes = }')
        # check for the possible sizes combs:
        self.res_dict = self.rec_tree_cutter(self.j_max * self.i_max)
        print(f'{self.res_dict = }')
        self.t3 = time.time_ns()
        # now we should connect shapes with space constraints to the possible full placement:
        print(f'rec connecting:')
        print(f'{len(self.shapes) = }')
        result = self.rec_shapes_connector(self.j_max * self.i_max, 0, set(), self.res_dict, [])
        self.t4 = time.time_ns()
        # result processing:
        if result is None:
            print(f'NO SOLUTION...')
            return None
        else:
            print(f'resulted figs: ')
            for f in result:
                print(f'{f.name} -> {f.moves = }')
                print_fig(f, self.j_max, self.i_max)
                print(f"... fig's hash: {hash(f)}")
            print(f'A SOLUTION EXISTS')
        # showing the result board:
        print_figures(result, self.board, self.i_max)
        # time data:
        self.print()
        # returns the moves:
        return sum([f.moves for f in result], start=[])

    # recursive part:
    @counted
    def rec_tree_cutter(self, cells_rem: int, fig_ind: int = 0) -> dict:
        # if cells_rem == 0 and fig_ind == len(self.figs_sizes):
        #     self.good_positions += 1
        #     return {0: True}
        # if we still are not out of bounds:
        if fig_ind < len(self.figs_sizes):
            res = {}
            for size_ in self.figs_sizes[fig_ind]:
                if cells_rem - size_ > 0:
                    # next fig index recursive call:
                    if dict_ := self.rec_tree_cutter(cells_rem - size_, fig_ind + 1):
                        res[size_] = dict_
                # border case (slightly faster than upper one variation):
                elif cells_rem - size_ == 0 and fig_ind == len(self.figs_sizes) - 1:
                    self.good_positions += 1
                    res[size_] = {0: True}
            return res

    @counted
    def rec_fig_seeker(self, rem_cells: int, fig: Figure, visited: set[tuple[int, int]], hashes: set[int],
                       figures: d[int, list[Figure]]) -> None:
        if rem_cells >= 0:
            # if a figure has not been already hashed:
            if hash(fig) not in hashes:
                # hashing figure:
                hashes |= {hash(fig)}
                # adding the figure to the figures list:
                figures[fig.size] += [fig]
                for dir_ in range(4):
                    # tries to fold the figure in the direction chosen:
                    if info := fig.fold(visited, self.powers, self.j_max, self.i_max, dir_):
                        self.unique_fold_counter += 1
                        fig_, n = info
                        # recursive call:
                        self.rec_fig_seeker(rem_cells - n, fig_, visited, hashes, figures)
            else:
                self.already_hashed_figs_counter += 1

    @counted
    def rec_shapes_connector(self, rem_cells: int, ind: int, visited: set[tuple[int, int]], res_dict: dict,
                             figs: list[Figure]) -> list[Figure] | None:
        # base case:
        if rem_cells == 0:
            return figs
        if ind < len(self.shapes):
            # res_dict, then shapes a bit faster than vice versa...
            for shape_size in sorted(res_dict.keys(), reverse=True):  # dict can violate the order of key-sizes...
                for shape in self.shapes[ind][shape_size]:
                    if all(cell not in visited for cell in
                           shape.cells):  # all instead of sets intersection -> 2 times faster...
                        if interim_res := self.rec_shapes_connector(rem_cells - shape.size, ind + 1,
                                                                    visited | shape.cells, res_dict[shape_size],
                                                                    figs + [shape]):
                            return interim_res

    def print(self):
        print(f'rec tree cutter counter/depth: {get_rec_counter(self.rec_tree_cutter)}')
        print(f'{self.good_positions = }')
        print(f'rec fig seeker counter/depth: {get_rec_counter(self.rec_fig_seeker)}')
        print(f'{self.unique_fold_counter = }')  # 36 366 98 989 98989 LL
        print(f'{self.already_hashed_figs_counter = }')
        print(f'rec shapes connector counter/depth {get_rec_counter(self.rec_shapes_connector)}')
        print(f'rec figs seeker time elapsed: {(self.t2 - self.t1) // 10 ** 6} milliseconds')
        print(f'rec tree cutter time elapsed: {(self.t3 - self.t2) // 10 ** 6} milliseconds')
        print(f'rec shapes connector time elapsed: {(self.t4 - self.t3) // 10 ** 6} milliseconds')
        print(f'algo section time elapsed: {(self.t4 - self.t1) // 10 ** 6} milliseconds')


def solver(grid: tuple[str, ...]) -> list[str] | None:
    """main method for the task solving"""  # 36 366 98 989 98989 LL
    board = Board(grid)
    return board.solve()


# colour printing/returning and colour reset methods:
def colour_print(char: str, colour: str):
    print((BOLD + colour.format(char) + END), end=' ')


def colour_str(char: str, colour: str):
    return (BOLD + colour + END).format(char)


def colour_str_inv(char: str, colour: str):
    return char + (BOLD + colour).format('')


def print_board(board: tuple[str, ...], shift: int = 0):
    i_max = len(board[0])
    print(f'Board: ')
    print(f' ' + f'-' * i_max)
    for row_ in board:
        print(f'|{" " * shift}{row_}|')
    print(f' ' + f'-' * i_max)


def print_fig(fig: Figure, j_max: int, i_max: int):
    # print(f'fig -> {fig.name}')
    print(f'       ' + f'-' * i_max)
    for j in range(j_max):
        print(f'      |', end='')
        for i in range(i_max):
            print(f'{fig.name if (j, i) in fig.cells else " "}', end='')
        print(f'|')
    print(f'       ' + f'-' * i_max)


def print_figures(figures: list[Figure], board: list[list[str]], i_max: int):
    colour_dict = {fig.name: COLOURS[i] for i, fig in enumerate(figures)}
    for fig in figures:
        for j, i in fig.cells:
            board[j][i] = fig.name
    print(f'result board: ')
    print(f' ' + f'-' * i_max)
    for row in board:
        string_ = ''.join((ch if ch == ' ' else colour_str(ch, colour_dict[ch])) for ch in row)
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


def find_initial_figs_placement(j_max: int, i_max: int, pieces_q: int) -> tuple[str, ...]:
    ...


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

s_super = (  # 16 * 16 [8 pieces]
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

s_hell = (  # 24 * 24 [4 pieces]
    'X X                   W ',
    ' X                   W W',
    'X X                   W ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    'Z Z                   Y ',
    ' Z                   Y Y',
    'Z Z                   Y ',
)

s_hells = (  # 32 * 32 [8 pieces]
    ' X                             W',
    'X                             W ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    'F                             R ',
    ' F                             R',
    ' F                              ',
    'F                               ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                              S ',
    '                               S',
    ' Q                             S',
    'Q                             S ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    'Z                             Y ',
    ' Z                             Y',
)

print(f'moves: {solver(s_super)}')
# counter = 0
# good_positions = 0
# result_d = rec_seeker(100, [[9, 18, 36, 72], [1, 2, 4, 8, 16, 32, 64], [25, 50, 100], [1, 2, 4, 8, 16, 32, 64]], 0)
# print(f'{result_d = }')
# print_res_dict(result_d)

# rec_counter = 0
# start = time.time_ns()
# # f_sizes = rec_seeker(80 - 10, [2, 2, 1, 1, 2, 1, 1])
# # f_sizes = rec_seeker(120 - 9, [1, 4, 2, 1, 1])
# f_sizes = rec_seeker(80 - 5, [1, 1, 1, 1, 1])
# finish = time.time_ns()

# print(f'rec_counter_: {rec_seeker.rec_counter}')

# print(f'info: {help(Figure)}')
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
# TODO: 2. optimise poss ways and rec connecting methods a bit... + (addition try to use all() instead of sets intersection in rec connector) +
# TODO: 3. implement res dict building for recursive tree cutting +
# TODO: 4. class Board for OOP design +
# TODO: 5. test section via decorators... + (debug flag) +
