import functools
import time
from collections import defaultdict as d

import arcade

from contextlib import closing
from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import urlopen

from six import (
    binary_type
)

# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050

# Moore's neighbourhood:
moore_walk = tuple((j, i) for j in range(-1, 2) for i in range(-1, 2) if j | i)

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


class Cell:
    def __init__(self, j: int, i: int, shape: arcade.Shape):
        self.j, self.i = j, i
        self.shape = shape


class ConwaysGameOfLife(arcade.Window):
    def __init__(self, width: int, height: int, cells: list[list[int]], generations: int, tile_size: int = 4,
                 time_step: int = 100):
        super().__init__(width, height)
        self.CURSOR_HAND = 'hand'
        # choosing the main background colour:
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        # initialization of important fields:
        self.n, self.m = len(cells), len(cells[0])
        self.gens = generations
        # visualization pars:
        self.tile_size = tile_size
        self.shapes_list = arcade.ShapeElementList()  # -> for fast and furious Batch Painting...
        # now setup:
        self.living_cells: dict[tuple[int, int], Cell] = ...
        self.setup(cells)
        # managing pars:
        self.stop = False
        # time section:
        self.time_step = time_step  # ms
        self._time = time.time_ns() // 10 ** 6

    def setup(self, cells: list[list[int]]):
        self.living_cells = {(j, i): Cell(j, i, self.get_shape(j, i)) for j in
                             range(self.n) for i in range(self.m) if cells[j][i]}
        # adding shapes to the list:
        for _, cell in self.living_cells.items():
            self.shapes_list.append(cell.shape)

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
        if not self.stop and time.time_ns() // 10 ** 6 - self._time > self.time_step:
            self.evolve()
            print(f'ShapeList size -> {len(self.shapes_list)}')
            self._time = time.time_ns() // 10 ** 6

    def on_key_press(self, symbol: int, modifiers: int):
        # is called when user press the symbol key:
        # if self.permission_of_movement:
        match symbol:
            case arcade.key.SPACE:
                self.stop = not self.stop
        # case of winning the game:
        ...

    def evolve(self) -> None:

        sleeping_cells_living_neighs_q = d(int)

        # cycling over all the living cells:
        set_ = set(self.living_cells.keys())  # 36 366 98 989 98989 LL
        for living_cell in set_:
            # print(f'{living_cell = }')
            moores_neighs = self.get_moores_neighs(*living_cell)
            sleeping_cells = moores_neighs - set_  # 36 366 98 989 98989 LL
            # print(f'...{moores_neighs = }')
            # print(f'...{sleeping_cells = }')
            for sleeping_cell in sleeping_cells:
                sleeping_cells_living_neighs_q[sleeping_cell] += 1
            living_neighs_q = 8 - len(sleeping_cells)
            if 2 <= living_neighs_q <= 3:
                # living cell stays alive, so nothing happens...                        # 36 366 98 989 98989 LL
                ...
            else:
                # living cell gets sleeping one -> removing shape from the list:
                self.shapes_list.remove(self.living_cells[living_cell].shape)
                # then removing the cell from dict:
                del self.living_cells[living_cell]

        # cycling over all the sleeping cells:
        for sleeping_cell, living_neighs_q in sleeping_cells_living_neighs_q.items():
            sj, si = sleeping_cell
            if living_neighs_q == 3:
                # adding new living cell rto the dict:
                self.living_cells[sleeping_cell] = Cell(sj, si, shape_ := self.get_shape(sj, si))
                # adding new shape to the list:
                self.shapes_list.append(shape_)

    @staticmethod
    def get_moores_neighs(j: int, i: int) -> set[tuple[int, int]]:
        return {(j + dj, i + di) for dj, di in moore_walk}

    def get_shape(self, j: int, i: int) -> arcade.Shape:
        # center of coords moved to the center of the display...
        return arcade.create_rectangle(
            self.tile_size + self.tile_size * i,
            self.height - self.tile_size - self.tile_size * j,
            self.tile_size - 1,
            self.tile_size - 1,
            arcade.color.BLACK,
            filled=True
        )


# parsing:
URL = f'https://conwaylife.com/patterns/'


class PbnNotFoundError(Exception):
    """Raised when trying to reach webpbn puzzle by non-existing id"""


def _get_utf8(string):
    if isinstance(string, binary_type):
        return string.decode('utf-8', errors='ignore')

    return string


def read(_id: str):
    path = 'https://conwaylife.com/patterns/'
    url = '{}{}'.format(path, _id)
    try:
        with closing(urlopen(url)) as page:
            return _get_utf8(page.read())  # pylint: disable=no-member
    except HTTPError as ex:
        if ex.code != 404:
            raise

    raise PbnNotFoundError(_id)


def parse(_id: str) -> list[list[int]]:
    res = read(_id)
    print(f'{type(res)}')

    res_list_: list[str] = res.split('\r\n')

    width = int(res_list_[4].split(',')[0].split(' ')[-1])

    print(f'{width = }')

    print(f'res -> ')
    for i, row in enumerate(res_list_):
        print(f'{i}: {row}')

    rows: list[str] = (interim_res := ''.join(res_list_[5:])).split('$')

    print(f'{interim_res = }')

    print(f'k -> ')
    for i, row in enumerate(rows):
        print(f'{i}: {row}')

    board = []
    empty_str = [0 for _ in range(width)]

    for row in rows:
        board_row = []
        ind_ = 0
        while ind_ < len(row):
            num_ = 0
            while ind_ < len(row) and row[ind_].isdigit():
                num_ = num_ * 10 + int(row[ind_])
                ind_ += 1
            if ind_ == len(row) and num_:
                # we should add some new empty (filled with only zeroes) lines:
                print(f'FAFA!!!')
                if len(board_row) < width:
                    board_row += [0 for _ in range(width - len(board_row))]
                print(f'...{len(board_row)}|{board_row = }')
                board += [board_row]
                for i_ in range(num_ - 1):
                    board += [empty_str]
                break
            else:
                ch = row[ind_]
                num_ = num_ if num_ else 1
                print(f'{num_ = }')
                if ch == 'o':
                    # living cell:
                    board_row += [1 for _ in range(num_)]
                elif ch == 'b':
                    # sleeping one:
                    board_row += [0 for _ in range(num_)]
                ind_ += 1
        else:
            if len(board_row) < width:
                print(f'LALA!')
                board_row += [0 for _ in range(width - len(board_row))]
            print(f'...{len(board_row)}|{board_row = }')
            board += [board_row]

    print(f'board height: {len(board)}')

    print_board(board)

    return board


def print_board(board: list[list[str]]):
    print(f'board: ')
    for row in board:
        row_str = ''.join(['*' if cell else ' ' for cell in row])
        print(f'{row_str}')


def main():
    cells_ = [
        [1, 1, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 1, 1, 1],
    ]

    gospers_glider_gun = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    hren_poimet_kak_budet_rabotat = [  # INVARIANTS MADNESS!!!
        [0, 1, 1, 0, 0],
        [1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1],
        [0, 0, 1, 1, 0],
    ]

    something_with_goose_shape = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
    ]

    dinuska_my_deepest_love = [
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
    ]

    smth = [
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
    ]

    perpetuum_mobile = [
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
    ]

    gens_ = 16

    board_ = parse("p67snarkloop.rle")  # 22cellquadraticgrowth.rle breeder1.rle "6bits.rle" piorbital.rle karelsp177.rle p172piheptominoshuttle.rle

    # print(f'board: ')
    # for row_ in board_:
    #     print(f'{row_}')

    game = ConwaysGameOfLife(SCREEN_WIDTH, SCREEN_HEIGHT, board_, gens_, 11, 10)
    arcade.run()


if __name__ == "__main__":
    main()
