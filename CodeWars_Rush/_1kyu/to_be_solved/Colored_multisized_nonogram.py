# accepted on codewars.com
import time
from CodeWars_Rush._1kyu.to_be_solved.Nonogram_ru_parser import NonogramsOrg


lines_solved: int
dp_iters: int


class ColoredCell:
    def __init__(self, j: int, i: int, colours: set[int]):
        self.j, self.i = j, i
        self._colours = colours
        self.colour = '?'

    def __str__(self):
        return f'{self.colours}'

    def __repr__(self):
        return str(self)

    @property
    def colours_q(self):
        return len(self._colours)

    @property
    def solved(self):
        return self.colours_q == 1

    @property
    def colours(self):
        return self._colours

    @colours.setter
    def colours(self, colours):
        self._colours = colours
        if self.solved:
            self.colour = f'{min(self._colours)}'


def solve(clues: tuple, colours: dict):
    global lines_solved, dp_iters
    lines_solved, dp_iters = 0, 0
    # clues and sizes:
    column_clues, row_clues = clues
    mj, mi = len(row_clues), len(column_clues)
    # convenient board:
    board = [[ColoredCell(j, i, set(colours.keys())) for i in range(mi)] for j in range(mj)]
    print(f'set(colours.keys()): {set(colours.keys())}')
    # board's area:
    cells = mj * mi
    # cycling now:
    print(f'colours_q: {len(colours)}')
    solved_cells, iteration = cycle(board, row_clues, column_clues, mj, mi, cells, len(colours))
    aggr_solved_cells = solved_cells
    aggr_iteration = iteration
    # guessing (not smart):
    # TODO: SAT or something else...
    questioned_cells = [(j, i) for j in range(mj) for i in range(mi) if board[j][i] == '?']
    questioned_cells.sort(  # chooses the cell that belongs to most solved row/column...
        # TODO: FIX THIS!!! (already FIXED), now CHECK THIS!!!
        key=lambda x: min(
            sum(row_clues[x[0]]) - sum(1 for ch in board[x[0]] if ch.colour != '?'),
            sum(column_clues[x[1]]) - sum(1 for j in range(len(board)) if board[j][x[1]].colour != '?')
        )
    )
    for qj, qi in questioned_cells:
        # tries to place 'X:
        temp_board = [[board[j][i] for i in range(mi)] for j in range(mj)]
        board[qj][qi] = 'X'
        r = cycle(board, row_clues, column_clues, mj, mi, cells, len(colours))
        if r is None:
            # backtracking:
            board = [[temp_board[j][i] for i in range(mi)] for j in range(mj)]
            board[qj][qi] = '.'
            aggr_solved_cells += 1
            # continue
        else:
            solved_cells, iteration = r
            aggr_iteration += iteration
            if aggr_solved_cells + solved_cells + 1 == cells:  # one cell been placed before the cycle algorithm starts...
                break
            # backtracking:
            board = [[temp_board[j][i] for i in range(mi)] for j in range(mj)]
    # result
    print(f'RESULT: ')
    show_board(board)

    print(f'TEST: ')
    show_colours_cell(board)

    print(f'solved_Cells: {solved_cells}, cells: {cells}')
    # print(f'aggr_iteration: {aggr_iteration}')
    print(f'lines solved: {lines_solved}')
    print(f'dp iters: {dp_iters}')

    return tuple(tuple(board[j]) for j in range(mj))


def cycle(board, row_clues, column_clues, mj, mi, cells, colours_q: int) -> tuple[int, int] | None:
    # main cycle of solving the board:
    prev_solved_cells = -1
    iteration = 0
    # cells filled with 'X' or '.':
    solved_cells = 0
    _rows_changed, columns_changed_ = [{_ for _ in range(x)} for x in [mj, mi]]
    while prev_solved_cells < solved_cells < cells:
        rows_changed_ = set()
        # next step preparation:
        prev_solved_cells = solved_cells
        iteration += 1
        # a. row lines solving
        if (solved_cells := solve_lines(board, row_clues, _rows_changed, columns_changed_, solved_cells, colours_q)) is None:
            return None
        # b. column lines solving (board 90-degrees rotation):
        if (solved_cells := solve_lines(board, column_clues, columns_changed_, rows_changed_, solved_cells, colours_q, True)) is None:
            return None
        # ops with sets:
        _rows_changed, columns_changed_ = rows_changed_, set()
    return solved_cells, iteration


def solve_lines(board, clues, _rows_changed, columns_changed_, solved_cells, colours_q: int, zipped=False) -> int | None:
    # a. row lines solving
    for j in _rows_changed:
        # monochromatic line solving:
        line = [board[i][j] for i in range(len(board))] if zipped else [board[j][i] for i in range(len(board[0]))]  # row or column
        if (delta_solved_cells := solve_line(line, clues[j], columns_changed_, board, j, colours_q, zipped)) is None:
            return None
        solved_cells += delta_solved_cells
    # return already solved cells:
    return solved_cells


def solve_line(line: list[ColoredCell], groups: list[tuple[int, int]], columns_changed_, board: list[list[ColoredCell]], j: int, colours_q: int, zipped=False) -> int | None:
    global lines_solved
    lines_solved += 1
    ll, gl = len(line), len(groups)
    # is it possible to place colour j at index i (for the every index i in the line and every colour j in the roster)?
    # colours = [[False for _ in range(ll + 1)] for _ in range(colours_q)]
    colours = {i: set() for i in range(ll)}
    # memoization and dynamic programming start:
    memo_table = {}
    dp(0, 0, 0, ll, gl, line, groups, colours, memo_table)
    # print(f'COLOURS: ')
    # for colour_ in range(colours_q):
    #     print(f'{colour_}: {["T" if el else "F" for el in colours[colour_]]}')
    # line recovering:
    solved_cells = 0
    for i, colours_set_ in colours.items():
        j_, i_ = (i, j) if zipped else (j, i)
        if line[i].colour == '?' and len(colours_set_) == 1:
            solved_cells += 1
        if len(colours_set_) < line[i].colours_q:
            columns_changed_.add(i)
        if not colours_set_:
            return None
        board[j_][i_].colours = colours_set_
    return solved_cells


# bottleneck of OPTIMIZATION!!!
def dp(n: int, k: int, last_colour: int, ll: int, gl: int, line: list[ColoredCell], groups: list[tuple[int, int]],
       colours: dict[int, set[int]], memo_table: dict[tuple[int, int, int], bool]) -> bool:
    # print(f'n, k, last_colour: {n, k, last_colour}')
    global dp_iters
    dp_iters += 1
    if (n, k, last_colour) not in memo_table.keys():
        # border cases:
        if n > ll:
            return False
        if n == ll:
            return True if k == gl else False
        res = False
        # main part:
        # 1. whites check:
        if 0 in line[n].colours:  # checks if white colour can be placed...
            if dp(n + 1, k, 0, ll, gl, line, groups, colours, memo_table):
                colours[n].add(0)  # white colour is already 0 (empty colour)
                res = True
        # 2. blacks check:
        if k < gl:
            if (colour_ := groups[k][1]) != last_colour:
                if (n_ := n + groups[k][0]) <= ll:
                    for cell_ in line[n: n_]:  # ind in (rng := range(n, n_))
                        if colour_ not in cell_.colours:
                            break
                    else:
                        if dp(n_, k + 1, colour_, ll, gl, line, groups, colours, memo_table):
                            for ind in range(n, n_):
                                colours[ind].add(colour_)
                            res = True
        # memo table update:
        memo_table[(n, k, last_colour)] = res
    # returns res:
    return memo_table[(n, k, last_colour)]


def show_board(board: list[list[ColoredCell]]):
    for row in board:
        r = ''.join([c.colour for c in row])
        print(f'{r}')


def show_colours_cell(board: list[list[ColoredCell]]):
    for row in board:
        r = ''.join(str(c) for c in row)
        print(f'{r}')


# BLACK'n'WHITE:
# hellish_clues_150x150 = NonogramsOrg.read(f'50861')
# nana_deviluke_200x149 = NonogramsOrg.read(f'66644')
# jaguar_200x200 = NonogramsOrg.read(f'66136')
# motherland_140x200 = NonogramsOrg.read(f'47617')
# b_letter_96x96 = NonogramsOrg.read(f'19043')
# gargantua_200x200 = NonogramsOrg.read(f'51237')
# pulp_fiction_155x190 = NonogramsOrg.read(f'52053')
# gargoyle_148x120 = NonogramsOrg.read(f'18417')
# biker_girl_90x100 = NonogramsOrg.read(f'65764')

# COLOURED:
# link_11x12 = NonogramsOrg.read(f'67122')
poppy_139_166 = NonogramsOrg.read(f'9596')
# lovers_120x120 = NonogramsOrg.read(f'36040')
# queen_sektonia_121x104 = NonogramsOrg.read(f'59615')
# doggy_22x28 = NonogramsOrg.read(f'26828')
# schooner_80x120 = NonogramsOrg.read(f'11824')
# wolf_89x87 = NonogramsOrg.read(f'11617')
# northern_america_200x200 = NonogramsOrg.read(f'21553')
# villina_with_book_150x200 = NonogramsOrg.read(f'57147')
# goth_dream_girl_161x200 = NonogramsOrg.read(f'53826')
# too_big_momo_125x200 = NonogramsOrg.read(f'33190')
# brunette_105x185 = NonogramsOrg.read(f'59505')

start = time.time_ns()  # 36 366 98 989 LL
solve(*poppy_139_166)  # hellish_clues_150x150, nana_deviluke_200x149, jaguar_200x200, motherland_140x200, b_letter_96x96, gargantua_200x200, pulp_fiction_155x190, gargoyle_148x120, biker_girl_90x100, poppy_139_166, lovers_120x120, queen_sektonia_121x104, doggy_22x28, schooner_80x120, wolf_89x87, northern_america_200x200, villina_with_book_150x200, goth_dream_girl_161x200, too_big_momo_125x200, brunette_105x185
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')



