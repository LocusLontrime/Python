import functools
import random
import time
from collections import defaultdict as d

import arcade

# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050

# debugging:
is_debug = False


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
        # print(f'{self.powers = }')
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
    def solve(self) -> list[Figure] | None:
        """tries to solve the board and finds solution if it exists"""
        self.t1 = time.time_ns()
        # finds the every possible folding for each figure:
        n = len(self.visited)
        for fig in self.figures:
            figures_ = d(list)
            self.rec_fig_seeker(self.j_max * self.i_max - n, fig, self.visited - fig.cells, set(), figures_)
            self.shapes.append(figures_)
            # reversed sorting for fast rec seeking and consequently performance:
            self.figs_sizes += [[_ for _ in sorted(figures_.keys(), reverse=True)]]
            # print(f'{fig.name} shapes quantity: {len(figures_)}')
            # for k, v in figures_.items():
            #     print(f'->shapes of a size {k}')
            #     for n, shape in enumerate(v):
            #         print(f'...{n + 1} | size: {shape.size}')
            #         print_fig(shape, self.j_max, self.i_max)
        self.t2 = time.time_ns()
        print(f'possible {self.figs_sizes = }')
        # check for the possible sizes combs:
        # self.res_dict = self.rec_tree_cutter(self.j_max * self.i_max)
        # print(f'{self.res_dict = }')
        result = self.rec_tree_cutter(self.j_max * self.i_max, [])
        self.t3 = time.time_ns()
        # now we should connect shapes with space constraints to the possible full placement:
        # print(f'rec connecting:')
        # print(f'{len(self.shapes) = }')
        # result = self.rec_shapes_connector(self.j_max * self.i_max, 0, set(), self.res_dict, [])
        self.t4 = time.time_ns()
        # result processing:
        if result is None:
            print(f'NO SOLUTION...')
            return None
        else:
            print(f'resulted figs: ')
            for f in result:
                print(f'{f.name} -> {f.moves = }')
                print(f"... fig's hash: {hash(f)}")
            print(f'A SOLUTION EXISTS')
            # time data:
        self.print()
        # returns the moves:
        return result

    @counted
    def rec_fig_seeker(self, rem_cells: int, fig: Figure, visited: set[tuple[int, int]], hashes: set[int],
                       figures: d[int, list[Figure]]) -> None:
        """seeks for all the possible figures' shapes on the board separately..."""
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

    # recursive part:
    @counted
    def rec_tree_cutter(self, cells_rem: int, sizes: list[int], fig_ind: int = 0) -> list[Figure] | None:
        """now checks valid combs on the fly, not building full rec_dict beforehand (this required too much time)"""
        if fig_ind < len(self.figs_sizes):
            for size_ in self.figs_sizes[fig_ind]:
                # print(f'{self.figs_sizes[fig_ind] = }')
                if cells_rem - size_ > 0:
                    # next fig index recursive call:
                    if res := self.rec_tree_cutter(cells_rem - size_, sizes + [size_], fig_ind + 1):
                        return res
                # border case (slightly faster than upper one variation):
                elif cells_rem - size_ == 0 and fig_ind == len(self.figs_sizes) - 1:
                    self.good_positions += 1
                    if figs := self.rec_shapes_connector(self.j_max * self.i_max, 0, set(), sizes + [size_], []):
                        return figs

    @counted
    def rec_shapes_connector(self, rem_cells: int, ind: int, visited: set[tuple[int, int]], sizes: list[int],
                             figs: list[Figure]) -> list[Figure] | None:
        """seeks for full figures' placement among the current good sizes comb"""
        # base case:
        if rem_cells == 0:
            return figs
        if ind < len(sizes):
            for shape in self.shapes[ind][sizes[ind]]:
                # all instead of sets intersection -> 2 times faster...
                if all(cell not in visited for cell in shape.cells):
                    if interim_res := self.rec_shapes_connector(rem_cells - sizes[ind], ind + 1,
                                                                visited | shape.cells, sizes,
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


class FoldingTilesGame(arcade.Window):
    def __init__(self, width: int, height: int, game_map: tuple[str, ...]):
        super().__init__(width, height)
        self.CURSOR_HAND = 'hand'
        # choosing the main background colour:
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        # initialization of important fields:
        self.grid: tuple[str, ...] = game_map
        self.shapes: list[Figure] | None = None
        self.folding_time_ms = None
        self.colours = None
        # visualization pars:
        self.tile_size = None
        self.y_max, self.x_max = len(game_map), len(game_map[0])
        self.shapes_list = arcade.ShapeElementList()  # -> for fast and furious Batch Painting...

    @staticmethod
    def make_grid_from_blueprint(game_map: str):
        ...

    def solver(self) -> list[Figure] | None:
        """main method for the task solving"""  # 36 366 98 989 98989 LL
        board = Board(self.grid)
        return board.solve()

    @staticmethod
    def get_ms(start, finish):
        return (finish - start) // 10 ** 6

    def setup(self):
        # game set up is located below:

        # 1. complex initialization:
        self.shapes = self.solver()

        if self.shapes:
            # 1.1 colours and tiles:
            x = int(255 / (len_ := len(self.shapes)))
            nums = [x * i for i in range(len_)]
            nums2 = nums[::]
            random.shuffle(nums)
            nums3 = nums[::]
            random.shuffle(nums)

            colours = [(nums[i], nums2[i], nums3[i]) for i in range(len_)]
            self.tile_size = int(min(self.width / (self.x_max + 2), self.height / (self.y_max + 2)))

            # 2. sprites/shapes etc...
            for i, shape in enumerate(self.shapes):
                for y, x in shape.cells:
                    self.shapes_list.append(arcade.create_rectangle(
                        self.tile_size + self.tile_size * x,
                        self.height - self.tile_size - self.tile_size * y,
                        self.tile_size - 1,
                        self.tile_size - 1,
                        colours[i],
                        filled=True
                    ))

    def on_draw(self):
        # renders this screen:
        arcade.start_render()
        # image's code:
        # border:
        ...
        # cells:
        self.shapes_list.draw()

    def update(self, delta_time: float):
        # game logic and movement mechanics lies here:
        ...

    def on_key_press(self, symbol: int, modifiers: int):
        # is called when user press the symbol key:
        # if self.permission_of_movement:
        match symbol:
            case arcade.key.SPACE:
                self.get_hint()
        # case of winning the game:
        ...


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
    'AA              ',
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


s_hell_ = (  # 32 * 32 [9 pieces]
    'X                              W',
    '                               W',
    '                                ',
    '                                ',
    '                                ',
    '                     J          ',
    '                                ',
    '                                ',
    ' F                            RR',
    '                              RR',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '               Q                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                               S',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                                ',
    '                             Y  ',
    'Z                               ',
)


s_super_hell_ = (  # 64 * 128 [9 pieces]
    'X                                                                                                                              W',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                              RR',
    '                                                                                                                              RR',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                S                                                               ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    'Q                                                                                                                               ',
    'Q                                                                                                                               ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                         J                                      ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    'U                                                                                                                               ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    '                                                                                                                                ',
    'Z                                                                                                                               ',
    '                                                                                                                              YY',
)


def main():
    game = FoldingTilesGame(SCREEN_WIDTH, SCREEN_HEIGHT, s_super_hell_)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
