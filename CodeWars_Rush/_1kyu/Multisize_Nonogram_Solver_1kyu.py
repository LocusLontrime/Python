# accepted on codewars.com
import time
from CodeWars_Rush._1kyu.to_be_solved.Nonogram_ru_parser import NonogramsOrg


# lines_solved: int
# dp_iters: int


def solve(clues: tuple):
    # global lines_solved, dp_iters
    # lines_solved, dp_iters = 0, 0
    # clues and sizes:
    column_clues, row_clues = clues
    mj, mi = len(row_clues), len(column_clues)
    # convenient board:
    board = [['?' for _ in range(mi)] for _ in range(mj)]
    # board's area:
    cells = mj * mi
    # cycling now:
    solved_cells, iteration = cycle(board, row_clues, column_clues, mj, mi, cells)
    aggr_solved_cells = solved_cells
    aggr_iteration = iteration
    # guessing:
    questioned_cells = [(j, i) for j in range(mj) for i in range(mi) if board[j][i] == '?']
    for qj, qi in questioned_cells:
        # tries to place 'X:
        temp_board = [[board[j][i] for i in range(mi)] for j in range(mj)]
        board[qj][qi] = 'X'
        r = cycle(board, row_clues, column_clues, mj, mi, cells)
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
    print(f'aggr_iteration: {aggr_iteration}')
    # print(f'lines solved: {lines_solved}')
    # print(f'dp iters: {dp_iters}')
    return tuple(tuple(board[j]) for j in range(mj))


def cycle(board, row_clues, column_clues, mj, mi, cells) -> tuple[int, int] | None:
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
        if (solved_cells := solve_lines(board, row_clues, _rows_changed, columns_changed_, solved_cells)) is None:
            return None
        # b. column lines solving (board 90-degrees rotation):
        if (solved_cells := solve_lines(board, column_clues, columns_changed_, rows_changed_, solved_cells, True)) is None:
            return None
        # ops with sets:
        _rows_changed, columns_changed_ = rows_changed_, set()
    return solved_cells, iteration


def solve_lines(board, clues, _rows_changed, columns_changed_, solved_cells, zipped=False) -> int | None:
    # a. row lines solving
    for j in _rows_changed:
        # monochromatic line solving:
        line = ''.join([board[i][j] for i in range(len(board))]) if zipped else ''.join(board[j])  # row or column
        if (delta_solved_cells := solve_line(line, clues[j], columns_changed_, board, j, zipped)) is None:
            return None
        solved_cells += delta_solved_cells
    # return already solved cells:
    return solved_cells


def solve_line(line: str, groups: list[int], columns_changed_, board: list[list[str]], j: int, zipped=False) -> int | None:
    # global lines_solved
    # lines_solved += 1
    ll, gl = len(line), len(groups)
    # is it possible to place black or white at every index?
    whites = [False for _ in range(ll + 1)]
    blacks = [False for _ in range(ll + 1)]
    # blacks already placed (for convenience and speed):
    blacks_filled = [False if ch == 'X' else True for ch in line]
    # building prefix arrays:
    prefix_whites = [0 for _ in range(ll + 1)]
    for i in range(ll):
        prefix_whites[i + 1] = prefix_whites[i] + (1 if line[i] == '.' else 0)
    # memoization and dynamic programming start:
    memo_table = {}
    dp(0, 0, False, ll, gl, groups, whites, blacks, blacks_filled, prefix_whites, memo_table)
    # line recovering:
    solved_cells = 0
    for i in range(ll):
        j_, i_ = (i, j) if zipped else (j, i)
        wi, bi = whites[i], blacks[i]
        if wi and bi:
            board[j_][i_] = '?'
        elif wi:
            board[j_][i_] = '.'
            if line[i] == '?':
                solved_cells += 1
                columns_changed_.add(i)
        elif bi:
            board[j_][i_] = 'X'
            if line[i] == '?':
                solved_cells += 1
                columns_changed_.add(i)
        else:
            return None
    return solved_cells


# bottleneck of OPTIMIZATION!!!
def dp(n: int, k: int, black: bool, ll: int, gl: int, groups: list[int], whites: list[bool], blacks: list[bool],
       blacks_filled: list[bool], prefix_whites: list[int], memo_table: dict[tuple[int, int, int], bool]) -> bool:
    # global dp_iters
    # dp_iters += 1
    if (n, k, black) not in memo_table.keys():
        # border cases:
        if n > ll:
            return False
        if n == ll:
            return True if k == gl else False
        res = False
        # main part:
        # 1. whites check:
        if blacks_filled[n]:
            if dp(n + 1, k, False, ll, gl, groups, whites, blacks, blacks_filled, prefix_whites, memo_table):
                whites[n] = True
                res = True
        # 2. blacks check:
        if k < gl and not black:
            if (n_ := n + groups[k]) <= ll:
                if prefix_whites[n_] - prefix_whites[n] == 0:
                    if dp(n_, k + 1, True, ll, gl, groups, whites, blacks, blacks_filled, prefix_whites, memo_table):
                        for ind in range(n, n_):
                            blacks[ind] = True
                        res = True
        # memo table update:
        memo_table[(n, k, black)] = res
    # returns res:
    return memo_table[(n, k, black)]


def show_board(board: list[list[str | int]]):
    for row in board:
        r = ''.join(row)
        print(f'{r}')


# thread = threading.Thread(target=main)
# sys.setrecursionlimit(1_000_000)
# threading.stack_size(0x8000000)
# thread.start()  # 36 366 98 989 LL

clues_ = (
    (
        (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
        (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
        (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
    ), (
        (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
        (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
        (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
    )
)

_clues = (
    (
        (1, 1, 3), (3, 2, 1, 3), (2, 2), (3, 6, 3), (3, 8, 2), (15,), (8, 5), (15,),
        (7, 1, 4, 2), (7, 9,), (6, 4, 2,), (2, 1, 5, 4), (6, 4), (2, 6), (2, 5),
        (5, 2, 1), (6, 1), (3, 1), (1, 4, 2, 1), (2, 2, 2, 2)
    ), (
        (2, 1, 1), (3, 4, 2), (4, 4, 2), (8, 3), (7, 2, 2), (7, 5), (9, 4), (8, 2, 3),
        (7, 1, 1), (6, 2), (5, 3), (3, 6, 3), (2, 9, 2), (1, 8), (1, 6, 1), (3, 1, 6),
        (5, 5), (1, 3, 8), (1, 2, 6, 1), (1, 1, 1, 3, 2)
    )
)

big_clues = (
    (
        (), (13,), (9, 13), (9, 27), (9, 27), (9, 27), (9, 6, 27), (9, 6, 27), (9, 6, 27), (9, 6, 6, 2, 16),
        (9, 6, 6, 2, 16), (9, 6, 6, 2, 16), (6, 2, 16), (23, 2, 5), (18, 7, 5), (18, 3, 2, 5), (18, 3, 2, 5),
        (4, 13, 7, 3), (31,), (13, 9, 10), (13, 9, 10), (11, 12, 7), (9, 39), (43,), (2, 9, 28), (2, 9, 28),
        (5, 2, 5, 7, 4), (5, 2, 5, 7, 4), (5, 2, 5, 13), (5, 2, 5, 13), (12, 5, 1, 6), (12, 5, 1, 6), (8, 19, 6),
        (8, 19, 6), (4, 1, 19, 1, 3), (10, 1, 19, 6), (10, 24, 6), (10, 24, 6), (10, 13, 15), (5, 13, 15), (5, 35),
        (5, 35), (8, 28), (8, 28), (8, 28), (8, 13), (8,), (3, 3), (3, 3), (8,)
    ), (
        (4, 4), (4, 4), (10, 4, 4), (10, 4, 4), (10, 4, 4), (10, 4, 4), (10, 29), (10, 37), (10, 11, 24),
        (10, 9, 27), (10, 4, 16, 8, 1), (8, 4, 4, 5, 1), (13, 4, 8), (6, 6, 5, 8, 8), (6, 6, 5, 2, 14),
        (6, 13, 2, 6), (6, 19, 6), (6, 19, 6), (6, 11, 10), (11, 10), (11, 10), (32,), (32,), (42,), (11, 1, 23),
        (16, 23), (16, 4, 13), (18, 4, 6, 5), (12, 4, 4, 6, 5), (6, 1, 4, 4, 6, 5), (23, 6, 5), (23, 6, 5),
        (6, 8, 6, 5), (6, 8, 6, 5), (23, 13), (23, 13), (43,), (16, 8, 8), (16, 8, 8), (12, 8, 8), (12, 8, 8),
        (12, 8, 8), (12, 8, 8), (12, 4, 18), (12, 4, 6, 11), (12, 12, 11), (12, 24), (12, 24), (12, 24), (12,)
    )
)

strange_clues = (
    (
        (), (), (), (), (), (), (), (), (), (9, 10), (9, 10), (9, 10), (9, 10), (9, 10), (16, 10), (16, 10),
        (9, 10), (9, 10), (9, 10), (11, 10), (5, 10), (5,), (5,), (5, 12), (5, 12), (5, 12), (5, 12), (5, 12),
        (9,), (7,), (9, 10), (9, 10), (13, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10),
        (10, 10), (10,), (10,), (10,), (), (), (), (), (), (), ()
    ), (
        (), (), (), (), (), (), (10,), (10,), (18,), (18,), (19,), (6, 5), (6, 5), (6, 12), (6, 12), (11, 10),
        (11, 10), (7, 8), (7, 8), (7, 8), (7, 8), (7, 5, 8), (7, 5, 8), (7, 5), (5,), (5,), (5,), (5,), (5,),
        (5,), (5,), (5,), (5,), (), (), (), (), (12, 13), (12, 13), (12, 13), (12, 13), (12, 13), (12, 13),
        (12, 13), (12, 13), (12, 13), (12, 13), (), (), ()
    )
)

great_clues = (
    (
        (50,), (50,), (50,), (50,), (31, 10), (16, 13, 10), (5, 22, 10), (5, 1, 6, 26), (5, 9, 20, 1),
        (5, 9, 18, 1), (5, 9, 18, 1), (5, 9, 20, 1), (5, 12, 18, 4), (5, 12, 18, 4), (5, 12, 6, 2, 4),
        (5, 12, 6, 4), (29, 2), (9, 12, 2, 2), (9, 12, 7, 2), (9, 12, 7, 2), (9, 12, 7, 2), (9, 12, 3, 2, 2),
        (12, 4, 7, 3, 3, 2), (12, 4, 7, 3, 3, 2), (21, 7, 3, 3, 2), (29, 3, 4, 4), (22, 5, 3, 11),
        (22, 5, 3, 11), (5, 14, 5, 3, 11), (5, 14, 5, 3, 11), (5, 14, 13, 11), (5, 14, 26), (5, 14, 26),
        (5, 14, 2, 21), (5, 14, 2, 11, 9), (5, 14, 2, 11, 9), (5, 14, 26), (5, 14, 6, 14), (5, 14, 14),
        (5, 14, 14), (5, 3, 8, 8, 2), (11, 8, 11, 2), (12, 9, 11, 2), (24, 11, 2), (2, 20, 11, 2),
        (2, 11, 5, 11, 2), (1, 12, 5, 17), (2, 46), (50,), (50,)
    ), (
        (47, 2), (46, 3), (44, 3), (44, 1, 2), (50,), (6, 12, 9), (6, 12, 9), (6, 12, 9), (6, 34), (17, 28),
        (7, 9, 28), (7, 9, 18, 8), (17, 16, 7), (17, 16, 7), (17, 18, 7), (17, 21, 3), (5, 11, 21, 3),
        (5, 39, 3), (7, 33, 3), (7, 38), (7, 38), (12, 6, 25), (12, 10, 8), (26, 8), (38, 3), (38, 3),
        (33, 2, 3), (33, 2, 3), (33, 2, 3), (14, 8, 3), (14, 7, 3), (4, 7, 7, 3), (4, 7, 7, 3), (4, 7, 7, 9),
        (4, 8, 20, 9), (4, 8, 20, 9), (4, 7, 32), (14, 3, 19), (14, 3, 19), (9, 3, 32), (9, 3, 16, 14), (8, 28),
        (8, 25), (8, 24), (8, 14, 4), (8, 14, 4), (16, 15, 4), (4, 4, 15, 4), (4, 38), (4, 38)
    )
)

mini_clues = (
    (
        (1, 1), (4,), (1, 1, 1), (3,), (1,)
    ), (
        (1,), (2,), (3,), (2, 1), (4,)
    )
)

clues_again = (
    (
        (6,), (6,), (6,), (6,), (6,), (6,), (10,), (12, 10), (12, 10), (16, 5, 10), (16, 5, 10), (3, 28, 3),
        (8, 23, 3), (7, 6, 16, 3), (14, 23), (14, 23), (14, 3, 9), (3, 3, 9), (12, 4), (12, 4), (12, 4),
        (12, 4), (12, 4), (23, 4), (13, 2, 4), (13, 10), (5, 13, 16), (6, 10, 16), (1, 3, 2, 7, 16), (6, 30),
        (37,), (10, 14), (2, 1, 14), (2, 1, 3, 3), (21, 3), (21, 3), (5, 25), (32,), (2, 8, 20), (5, 3, 12),
        (5, 3, 12), (5, 3, 12), (11, 4, 12), (11, 4, 3), (2, 8, 4, 3), (11, 4, 3), (11, 4, 3), (11, 4, 5), (5,),
        (2,)
    ), (
        (8, 8), (8, 5, 2), (8, 5, 2), (2, 5, 8), (8, 8), (8, 3, 4, 14), (8, 4, 1, 14), (4, 3, 4, 2, 4, 5, 3),
        (3, 4, 4, 2, 14), (8, 8, 14), (8, 8, 2, 2, 6), (21, 2, 2, 2, 6), (25, 5, 6), (17, 6, 14), (6, 6, 6, 14),
        (6, 6, 6, 14), (2, 3, 7, 12), (2, 13, 13), (17, 6, 5, 6), (10, 6, 3, 5, 6), (9, 6, 10, 6), (9, 14, 5, 6),
        (6, 24, 5), (6, 7, 14), (6, 7, 14, 2), (6, 7, 18, 3), (6, 7, 8, 14), (6, 22, 13), (22, 13), (22, 7),
        (27, 7), (10, 7, 7), (5, 2, 7, 7), (5, 2, 7, 7), (5, 2, 17), (5, 2, 17), (5, 2, 17), (10,), (10,), (10,)
    )
)

clues_45x35 = (
    (
        (3, 6, 9, 2, 6), (2, 6, 11, 2, 5), (1, 5, 9, 2, 4), (2, 5, 1, 7, 4, 1, 3), (1, 3, 2, 4, 7, 2, 3),
        (1, 1, 4, 3, 9, 1, 3), (4, 3, 1, 11, 2, 2), (7, 3, 13, 2, 2), (1, 6, 4, 14, 1, 2), (1, 6, 4, 10, 1, 2),
        (1, 6, 3, 9, 4, 1, 2), (1, 7, 3, 7, 5, 1, 1), (1, 6, 3, 4, 7, 1, 1), (2, 6, 4, 2, 9, 1, 1),
        (2, 6, 3, 11, 1, 1), (2, 6, 3, 14, 1, 1), (3, 6, 3, 14, 1, 1), (2, 6, 3, 12, 2, 1), (2, 5, 2, 10, 1),
        (2, 6, 3, 9, 2), (1, 2, 6, 3, 8, 1), (2, 1, 5, 3, 6, 2, 2), (1, 5, 4, 1, 2, 1), (2, 1, 3, 3, 2, 3),
        (2, 2, 4, 1, 2), (3, 8, 4, 3, 1), (2, 6, 2, 2, 1), (1, 4, 4, 1, 2), (1, 11, 1, 2), (1, 8), (1, 5, 8),
        (2, 7, 1, 2), (2, 12, 1, 2), (2, 3, 5, 3, 1), (2, 2, 5, 4, 8), (3, 4, 4, 5, 8), (3, 3, 2, 8, 2, 1),
        (3, 4, 1, 6, 2, 1), (4, 3, 2, 8, 8), (4, 4, 4, 5, 7), (5, 2, 5, 4, 1), (6, 3, 5, 3, 1), (7, 13, 1),
        (8, 7), (9, 5)
    ), (
        (3, 9, 2, 18), (3, 1, 6, 3, 14), (2, 1, 5, 5, 2, 10), (1, 2, 9, 3, 2, 7), (1, 3, 12, 1, 5),
        (3, 17, 2, 4), (4, 18, 1, 2, 3), (4, 16, 1, 1, 2), (3, 1, 12, 1, 1, 5, 1), (2, 6, 9, 1, 2, 9),
        (2, 11, 2, 2, 1, 10), (1, 13, 2, 2, 1, 2, 1, 1, 1, 2), (2, 16, 2, 1, 1, 1, 1, 1, 1, 1),
        (6, 11, 2, 1, 11), (6, 4, 4, 2, 1, 4, 4), (6, 7, 3, 2, 1, 5, 5), (5, 7, 8, 1, 7, 7),
        (4, 7, 7, 3, 1, 4, 1, 1, 4), (4, 8, 8, 4, 1, 3, 3, 3), (3, 7, 8, 3, 2, 3, 5, 3), (3, 8, 9, 3, 1, 15),
        (2, 7, 9, 1, 13), (2, 8, 9, 2, 2, 11), (1, 7, 9, 2, 2, 7), (6, 9, 2, 1), (1, 6, 9, 1, 3), (2, 5, 8, 2),
        (2, 3, 7, 3, 2, 5), (3, 7, 3, 2, 6), (1, 4, 3, 2, 2, 2), (2, 12, 2, 2, 2), (3, 18), (6, 2, 2, 2),
        (11, 6, 2, 2), (18, 6, 2, 2)
    )
)

clues_50x30 = (
    (
        (9, 6), (9, 6), (3, 6), (3, 6, 6), (9, 6, 6), (9, 6), (9, 6), (18, 10), (5, 3, 10), (5, 15), (1, 24),
        (1, 19, 3), (1, 19, 3), (1, 6, 5, 3), (1, 6, 5, 4), (1, 1, 9, 4), (1, 12, 4), (1, 12, 4), (18, 4),
        (6, 9, 4), (5, 9, 4), (8, 5, 4), (14, 5, 4), (13, 7, 4), (3, 15, 2, 4), (3, 9, 8, 4), (3, 8, 9, 4),
        (3, 3, 9, 4), (3, 13, 4), (3, 4, 8, 4), (4, 4, 8, 4), (18, 10), (14, 14), (5, 11, 12), (5, 24), (5, 24),
        (27,), (27,), (2, 7, 1), (2, 7, 1), (2, 7, 1), (5, 7, 1), (2, 2, 7, 1), (5, 7, 1), (5, 2, 1), (5, 2, 1),
        (12, 2, 1), (12, 10), (12, 10), (12, 10)
    ), (
        (31, 4, 9), (10, 18, 9), (10, 18, 1, 7), (2, 6, 6, 20), (2, 6, 9, 19), (2, 4, 2, 6, 2, 2, 4),
        (2, 4, 9, 6, 7, 4), (2, 4, 5, 3, 6, 7, 4), (2, 4, 5, 3, 5, 7, 4), (1, 28, 4), (1, 28, 4), (1, 28, 4),
        (1, 3, 11, 10), (1, 3, 9, 1, 3, 7), (1, 3, 7, 9, 5), (2, 6, 7, 9, 11), (2, 6, 7, 22), (2, 6, 7, 11, 10),
        (2, 4, 22), (2, 4, 2, 6, 12), (2, 7, 28), (7, 26), (7, 7, 3), (7, 7, 3), (14, 7, 3), (11, 7, 3),
        (11, 24, 3), (38, 3), (38, 3), (50,)
    )
)

clues_80x10 = (
    (
        (10,), (2, 2), (2, 2), (2, 2), (2, 2), (10,), (10,), (4,), (4,), (3,), (3,), (4,), (10,), (5, 4), (2, 7),
        (2, 2, 2), (2, 2, 2), (5, 2), (5, 2), (10,), (2, 5), (2, 5), (2, 5), (10,), (10,), (10,), (10,), (10,),
        (4, 5), (1, 3), (1, 3), (1, 3, 3), (1, 1, 1, 3), (1, 1, 3), (1, 1, 1, 3), (1, 3, 3), (1, 3), (1, 3),
        (10,), (10,), (10,), (2, 3), (2, 3), (2, 2, 3), (2, 1, 1, 3), (2, 1, 3), (2, 1, 1, 3), (2, 2, 3), (2, 3),
        (2, 3), (10,), (10,), (10,), (10,), (10,), (10,), (10,), (2, 2), (2, 1, 2), (2, 2), (2, 1, 1, 2), (3, 2),
        (3, 1, 2), (3, 1, 2), (2, 2, 2), (2, 2), (2, 2), (2, 2), (10,), (2, 7), (2, 3, 1, 1), (10,), (10,),
        (4, 5), (2, 2, 3), (2, 2, 4), (10,), (3, 6), (10,), (10,)
    ), (
        (7, 68), (7, 17, 42), (1, 2, 2, 3, 6, 1, 1, 3, 7, 3, 1, 3, 4), (1, 2, 8, 6, 1, 1, 3, 5, 7, 1, 1, 9, 2),
        (1, 2, 8, 5, 1, 1, 3, 1, 1, 7, 1, 1, 1, 5, 6), (1, 2, 1, 1, 10, 5, 3, 1, 1, 7, 1, 1, 6, 4),
        (1, 4, 4, 10, 3, 7, 2, 3, 5), (1, 10, 38, 12), (70, 9), (80,)))

clues_42x48 = (
    (
        (10,), (10,), (7, 10, 20), (7, 10, 20), (7, 10, 20), (4, 6, 20), (4, 6, 6, 10), (4, 6, 6, 10),
        (7, 10, 6, 10), (7, 23, 10), (15, 10, 10), (20, 24), (7, 5, 14), (9, 5, 14), (5, 20, 4, 1),
        (5, 20, 1, 4), (5, 8, 6, 9), (5, 8, 6, 2), (5, 20, 2), (5, 5, 22, 3), (5, 5, 22, 2), (5, 11),
        (11, 1, 11), (11, 7, 11), (11, 7, 11), (11, 8, 2, 4), (20, 2, 4), (20, 2, 4), (3, 23, 4), (3, 32),
        (3, 32), (22, 14), (22, 14), (3, 4, 4, 2), (3, 13, 2), (13, 13, 1, 3), (13, 13, 6), (13, 13, 4, 2),
        (3, 13, 3, 2), (13, 1, 2), (7,), (1,)
    ), (
        (10,), (10,), (10,), (10,), (3, 4, 26), (3, 4, 26), (3, 31), (18, 2, 3), (19, 2, 3), (5, 6, 2, 3),
        (5, 6, 2, 3), (3, 6, 6, 2, 3), (3, 6, 6, 2, 3), (3, 4, 11, 3), (3, 4, 11, 3), (8, 10, 7, 3),
        (8, 10, 8, 3), (8, 10, 10), (8, 10, 10), (8, 10, 10), (8, 5, 10), (12, 10), (12, 17), (7, 3, 17),
        (7, 3, 12), (14, 3, 12), (14, 3, 3, 6), (14, 3, 3, 6, 1), (14, 3, 3, 6), (19, 1, 3, 6), (19, 3, 6),
        (4, 10, 12), (4, 10, 12), (4, 10, 12), (4, 29), (12, 14), (12, 1, 6, 4, 2), (12, 6, 4, 4),
        (12, 2, 6, 4, 4, 1), (12, 3, 6, 4, 3, 1), (12, 3, 6, 4, 2, 1), (12, 3, 14, 2, 1), (12, 1, 14, 1, 1),
        (12, 1, 1, 14, 4), (12, 1, 14, 4), (1, 1), (5,), (5,)
    )
)

clues2_40x40 = (
    (
        (40,), (40,), (40,), (40,), (40,), (8, 20), (8, 15), (8, 1, 12), (8, 9, 10), (4, 3, 10, 2, 8),
        (4, 3, 2, 10, 1, 7), (4, 3, 1, 10, 2, 6), (4, 3, 6, 7, 1, 5), (4, 3, 2, 1, 5, 2, 1, 4),
        (4, 3, 1, 7, 1, 3), (4, 3, 2, 4, 3, 2), (4, 3, 1, 2, 9, 2, 2), (3, 3, 3, 3, 6, 1, 1),
        (3, 3, 10, 12, 2, 1), (3, 5, 2, 2), (3, 5, 3, 2, 5, 6), (3, 5, 6, 1, 3, 5), (3, 5, 6, 2, 3, 3, 5),
        (3, 12, 1, 3, 8), (3, 6, 3, 1, 1, 2, 9), (3, 5, 2, 2, 2, 9), (3, 5, 2, 14), (2, 5, 2, 14),
        (2, 5, 2, 16), (2, 7, 2, 16), (2, 15, 19), (2, 35), (2, 1, 35), (5, 7), (5, 18), (5, 31), (40,), (40,),
        (40,), (40,)
    ), (
        (40,), (40,), (27, 7), (17, 8), (9, 7), (33, 4), (33, 4), (33, 4), (5, 14, 4), (5, 14, 5),
        (5, 4, 3, 2, 4, 5), (5, 2, 2, 2, 2, 4, 5), (5, 2, 3, 2, 3, 3, 5), (5, 5, 1, 5, 3, 5), (5, 5, 1, 5, 3, 5),
        (5, 5, 1, 5, 3, 5), (5, 4, 1, 1, 3, 1, 3, 5), (5, 4, 2, 2, 1, 1, 3, 5), (5, 5, 4, 1, 3, 5),
        (5, 6, 3, 2, 3, 5), (6, 2, 5, 4, 1, 2, 5), (6, 7, 2, 5, 5), (6, 2, 7, 1, 4, 6), (6, 1, 7, 2, 3, 6),
        (6, 2, 5, 1, 6, 6), (7, 2, 1, 3, 1, 1, 5, 6), (7, 2, 3, 1, 8, 6), (7, 2, 3, 2, 7, 6),
        (8, 2, 1, 1, 10, 6), (8, 2, 1, 1, 10, 6), (9, 3, 1, 2, 7, 6), (9, 1, 3, 9, 6), (10, 1, 13, 6),
        (11, 3, 18), (12, 1, 1, 17), (13, 1, 20), (14, 1, 20), (15, 20), (17, 21), (40,)
    )
)

clues3_40x40 = (
    (
        (), (6,), (6, 2), (6, 5, 2), (24, 2), (24, 2), (6, 7, 2), (6, 7, 2), (6, 7, 2), (6, 12), (9, 30),
        (9, 14), (7, 1, 2), (16,), (16,), (4, 2, 13), (4, 4, 6, 5, 6), (7, 4, 11, 1, 5), (7, 4, 5, 5, 1, 5),
        (7, 1, 9, 3, 1, 6), (4, 1, 2, 11, 6), (4, 1, 2, 2, 1, 3, 6), (1, 8, 3, 1, 3), (1, 4, 1, 2, 3),
        (1, 4, 1, 7, 3), (7, 8, 7, 3), (7, 8, 1, 7, 3), (7, 8, 1, 7, 3), (7, 8, 1, 3, 3), (7, 4, 3, 1, 3, 3),
        (13, 4, 3, 1, 3, 4), (13, 3, 4), (3, 1, 3, 4), (3, 7, 3, 4), (3, 7, 3, 4), (3, 7, 1), (3, 24, 1),
        (3, 16, 1, 9), (3, 18, 9), (24, 2, 10)
    ), (
        (12, 10), (12, 10), (12, 10), (12, 2, 1), (5, 5, 3, 2, 1), (5, 5, 3, 2, 1), (5, 5, 3, 7, 1),
        (5, 2, 2, 7, 1), (5, 5, 7, 1), (5, 2, 7, 1), (8, 2, 7, 1), (8, 2, 7, 1), (8, 27), (8, 6, 7), (11, 3, 7),
        (11, 3, 7), (2, 2, 7), (2, 2, 12, 7), (2, 2, 12, 7), (2, 2, 5, 9, 4), (2, 2, 5, 9, 4), (8, 8, 4, 4),
        (8, 8, 6, 4), (9, 6, 1, 6, 4), (8, 3, 12, 3), (8, 1, 4, 3), (8, 1, 2, 1, 4), (8, 6, 5, 4), (2, 6, 1, 1),
        (2, 8, 11, 3), (2, 2, 3, 11, 1, 1), (8, 8, 11, 4), (8, 4, 4), (1, 4, 4), (1, 1, 1, 9, 4),
        (1, 1, 6, 5, 4), (1, 6, 5, 3), (1, 19, 3), (1, 19, 3), (1, 24)
    )
)

clues_30x30 = (
    (
        (), (), (), (7,), (10,), (3, 12), (3, 7), (3, 7), (3, 3), (3, 3), (4,), (4,), (4,), (4, 4), (4, 4),
        (4, 4), (4,), (4,), (4,), (3, 4), (3, 4), (3, 9), (3, 8), (13,), (13,), (6,), (), (), (), ()
    ), (
        (), (), (), (5, 4), (5, 4), (5, 4), (), (), (), (), (), (3, 3), (3, 3, 3), (3, 3, 3), (3, 3, 3), (3, 3),
        (3, 5), (5, 4), (5, 4), (4, 4), (4, 4), (21,), (20,), (20,), (12,), (), (), (), (), ()
    )
)

clues_35x35 = (
    (
        (), (3,), (3, 13), (3, 1, 13), (2, 4, 13), (1, 13), (5, 1, 13), (5, 13), (5, 13), (2, 13), (18,),
        (6, 2, 18), (6, 2, 6), (8, 2, 6), (8, 2, 6, 1), (13, 6, 5), (13, 3), (13, 3), (5, 3), (5, 2, 3, 5),
        (5, 2, 2, 5), (5, 5, 5), (9, 5, 5), (9, 12), (9, 12), (6, 1, 8), (6, 5, 8), (13, 8, 6), (13, 8, 6),
        (13, 6), (13, 6), (13, 6), (13, 6), (11,), ()
    ), (
        (), (1, 5), (1, 5), (23,), (23,), (1, 23), (1, 23), (1, 23), (1, 7, 12), (3, 3, 7), (3, 3, 3, 3, 7),
        (3, 3, 3, 12), (3, 3, 7, 8), (4, 7, 8), (4, 7), (7,), (2,), (6, 3), (6, 3), (1, 6, 10), (6, 10), (6, 8),
        (14, 10), (10, 10), (10, 1, 1, 6), (10, 3), (10, 1, 7, 6), (10, 1, 6, 6), (10, 10, 6), (10, 10, 6),
        (10, 10, 6), (10, 6), (10,), (10,), (10,)
    )
)

backtrack_clues = (
    (
        (9,), (2, 1, 1, 1, 2), (9,), (), (5, 5, 5), (3, 3, 2, 1, 2, 3, 3), (5, 5, 5), (3, 3, 3), (5, 5, 5),
        (2, 2, 2, 2, 2, 2), (2, 2, 2, 2, 2, 2), (), (2, 1, 1), (2, 3, 1), (1, 2, 1), (1, 2), (2, 1), (1, 3),
        (2, 3), (1, 2, 1), (), (), (2, 2, 1), (4, 6, 3), (5, 8, 1, 4), (5, 1, 8, 7), (3, 1, 3, 3, 7),
        (2, 1, 2, 2, 7), (), (1,), (1,), (3,), (3,), (5,), (7,)
    ), (
        (1, 6), (1, 1, 1, 2, 6), (3, 3, 2, 1, 4), (5, 1, 5, 3), (1, 3, 1, 2), (5, 1, 2, 1, 1, 1),
        (3, 3, 6, 2), (1, 1, 2, 3, 4), (1, 1, 3, 6), (4,), (4, 2), (1, 5, 1), (1, 2, 4), (3, 2, 4),
        (1, 3, 4), (5, 3, 4), (1, 3, 5), (1, 3, 2, 4), (3, 1, 2), (1, 1, 1), (3,), (1, 1), (3,),
        (1, 1, 1, 1, 4), (3, 3, 3, 3), (1, 1, 5, 1, 3), (3, 1, 3, 4), (1, 5, 1, 6), (3, 3, 5), (1, 1, 5)
    )
)

backtrack_clues2 = (
    (
        (25,), (1, 1), (1, 2, 1), (1, 3, 1), (1, 5, 1), (1, 5, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1),
        (1, 7, 1), (1, 7, 1), (1, 6, 1), (1, 5, 1), (1, 4, 1), (1, 5, 1), (1, 7, 1), (1, 7, 1), (1, 9, 1),
        (1, 3, 6, 1), (1, 2, 2, 8, 1), (1, 1, 3, 2, 1, 2, 1), (2, 1, 4, 2, 2, 1), (4, 1, 1, 4, 3, 1),
        (1, 1, 1, 1, 1, 1, 2), (1, 2, 1, 1, 2, 2), (1, 2, 2, 2, 2, 1), (1, 2, 4, 1, 1), (1, 4, 3, 1),
        (1, 6, 3, 1), (1, 9, 1), (1, 8, 1), (1, 6, 1), (1, 3, 1), (1, 1), (25,)
    ), (
        (35,), (1, 2, 1), (1, 2, 1, 1), (1, 1, 1, 1), (1, 2, 1), (1, 1, 1), (1, 2, 5, 1), (1, 2, 8, 1),
        (1, 1, 9, 1), (1, 2, 3, 6, 1), (1, 1, 2, 1, 4, 1), (1, 3, 5, 2, 4, 1), (1, 6, 6, 1, 1, 2, 1),
        (1, 16, 4, 1, 3, 1), (1, 17, 1, 4, 1), (1, 24, 2, 1), (1, 18, 2, 1, 1, 1), (1, 9, 5, 1, 1),
        (1, 5, 2, 1), (1, 2, 1), (1, 4, 1), (1, 1, 2, 1), (1, 1, 1, 1), (1, 2, 1), (35,)
    )
)

backtracking_clues3 = (
    (
        (7,), (5,), (3,), (3,), (1,), (1,), (), (2, 1, 2, 2, 7), (3, 1, 3, 3, 7), (5, 1, 8, 7),
        (5, 8, 1, 4), (4, 6, 3), (2, 2, 1), (), (), (1, 2, 1), (2, 3), (1, 3), (2, 1), (1, 2),
        (1, 2, 1), (2, 3, 1), (2, 1, 1), (), (2, 2, 2, 2, 2, 2), (2, 2, 2, 2, 2, 2), (5, 5, 5),
        (3, 3, 3), (5, 5, 5), (3, 3, 2, 1, 2, 3, 3), (5, 5, 5), (), (9,), (2, 1, 1, 1, 2), (9,)
    ), (
        (6, 1), (6, 2, 1, 1, 1), (4, 1, 2, 3, 3), (3, 5, 1, 5), (2, 1, 3, 1), (1, 1, 1, 2, 1, 5),
        (2, 6, 3, 3), (4, 3, 2, 1, 1), (6, 3, 1, 1), (4,), (2, 4), (1, 5, 1), (4, 2, 1), (4, 2, 3),
        (4, 3, 1), (4, 3, 5), (5, 3, 1), (4, 2, 3, 1), (2, 1, 3), (1, 1, 1), (3,), (1, 1), (3,),
        (4, 1, 1, 1, 1), (3, 3, 3, 3), (3, 1, 5, 1, 1), (4, 3, 1, 3), (6, 1, 5, 1), (5, 3, 3),
        (5, 1, 1)
    )
)

backtrack_clues5 = (
    (
        (1, 6), (1, 1, 1, 2, 6), (3, 3, 2, 1, 4), (5, 1, 5, 3), (1, 3, 1, 2), (5, 1, 2, 1, 1, 1),
        (3, 3, 6, 2), (1, 1, 2, 3, 4), (1, 1, 3, 6), (4,), (4, 2), (1, 5, 1), (1, 2, 4), (3, 2, 4),
        (1, 3, 4), (5, 3, 4), (1, 3, 5), (1, 3, 2, 4), (3, 1, 2), (1, 1, 1), (3,), (1, 1), (3,),
        (1, 1, 1, 1, 4), (3, 3, 3, 3), (1, 1, 5, 1, 3), (3, 1, 3, 4), (1, 5, 1, 6), (3, 3, 5), (1, 1, 5)
    ), ((9,), (2, 1, 1, 1, 2), (9,), (), (5, 5, 5), (3, 3, 2, 1, 2, 3, 3), (5, 5, 5), (3, 3, 3), (5, 5, 5),
        (2, 2, 2, 2, 2, 2), (2, 2, 2, 2, 2, 2), (), (2, 1, 1), (2, 3, 1), (1, 2, 1), (1, 2), (2, 1),
        (1, 3), (2, 3), (1, 2, 1), (), (), (2, 2, 1), (4, 6, 3), (5, 8, 1, 4), (5, 1, 8, 7),
        (3, 1, 3, 3, 7), (2, 1, 2, 2, 7), (), (1,), (1,), (3,), (3,), (5,), (7,)
        )
)

backtrack_clues6 = (
    (
        (35,), (1, 2, 1), (1, 1, 1, 1), (1, 2, 1, 1), (1, 4, 1), (1, 2, 1), (1, 2, 5, 1), (1, 1, 5, 9, 1),
        (1, 1, 1, 2, 18, 1), (1, 2, 24, 1), (1, 4, 1, 17, 1), (1, 3, 1, 4, 16, 1), (1, 2, 1, 1, 6, 6, 1),
        (1, 4, 2, 5, 3, 1), (1, 4, 1, 2, 1, 1), (1, 6, 3, 2, 1), (1, 9, 1, 1), (1, 8, 2, 1), (1, 5, 2, 1),
        (1, 1, 1), (1, 2, 1), (1, 1, 1, 1), (1, 1, 2, 1), (1, 2, 1), (35,)
    ), (
        (25,), (1, 1), (1, 3, 1), (1, 6, 1), (1, 8, 1), (1, 9, 1), (1, 3, 6, 1), (1, 3, 4, 1),
        (1, 1, 4, 2, 1), (1, 2, 2, 2, 2, 1), (2, 2, 1, 1, 2, 1), (2, 1, 1, 1, 1, 1, 1), (1, 3, 4, 1, 1, 4),
        (1, 2, 2, 4, 1, 2), (1, 2, 1, 2, 3, 1, 1), (1, 8, 2, 2, 1), (1, 6, 3, 1), (1, 9, 1), (1, 7, 1),
        (1, 7, 1), (1, 5, 1), (1, 4, 1), (1, 5, 1), (1, 6, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1),
        (1, 7, 1), (1, 5, 1), (1, 5, 1), (1, 3, 1), (1, 2, 1), (1, 1), (25,)
    )
)


hellish_clues_150x150 = NonogramsOrg.read(f'50861')
# nana_deviluke_200x149 = NonogramsOrg.read(f'66644')
# jaguar_200x200 = NonogramsOrg.read(f'66136')
# motherland_140x200 = NonogramsOrg.read(f'47617')
# b_letter_96x96 = NonogramsOrg.read(f'19043')
# gargantua_200x200 = NonogramsOrg.read(f'51237')
# pulp_fiction_155x190 = NonogramsOrg.read(f'52053')
# gargoyle_148x120 = NonogramsOrg.read(f'18417')
# biker_girl_90x100 = NonogramsOrg.read(f'65764')

start = time.time_ns()
solve(hellish_clues_150x150)  # hellish_clues_150x150, nana_deviluke_200x149, jaguar_200x200, motherland_140x200, b_letter_96x96, gargantua_200x200, pulp_fiction_155x190, gargoyle_148x120, biker_girl_90x100
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')