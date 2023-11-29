# accepted on codewars.com
walk = ((0, 1), (1, 0), (0, -1), (-1, 0))
solution_found: bool
solved_board = []
moves: list[tuple[int, int]]
rec_counter: int


def solve(board: str):
    global solution_found, rec_counter, moves
    moves = []
    rec_counter = 0
    solution_found = False
    board = normalize_board(board)
    print(f'normalized_board: {board}')
    cells, counter, b_bitmask = numerate(board)
    print(f'cells: {cells}, counter: {counter}, cells_q: {len(cells)}')
    print(f'b_bitmask: {b_bitmask}')
    empty_cells = {(j, i) for j in range(len(board)) for i in range(len(board[0])) if board[j][i] == '.'}
    visited_states = {b_bitmask}
    rec_core(0, counter - 1, [], len(board), len(board[0]), board, empty_cells, b_bitmask, visited_states, cells)
    # solved_board:
    print(f'solved_board: ')
    for row in solved_board:
        print(f'{row}')
    return moves


def rec_core(counter: int, max_counter: int, res: list[tuple[int, int]], mj: int, mi: int, board: list[list[str]],
             empty_cells: set[tuple[int, int]], b_bitmask: int, visited_states: set, cells: dict):
    global solution_found, solved_board, rec_counter, moves
    rec_counter += 1
    if not solution_found:
        # base case:
        if counter == max_counter:
            solution_found = True
            # print(f'solution_found: {solution_found}')
            solved_board = [[_ for _ in row] for row in board]
            moves = res
        # body of rec:
        for j, i in empty_cells:
            # print(f'...j, i: {j, i}, counter: [{counter}/{max_counter}], mask: {bin(b_bitmask)}')
            for dj, di in walk:
                if not solution_found:
                    if is_valid(_j := j + dj, _i := i + di, mj, mi) and is_valid(j_ := _j + dj, i_ := _i + di, mj, mi):
                        if board[_j][_i] == 'O' and board[j_][i_] == 'O':
                            # new move:
                            new_b_bitmask = jump(j, i, dj, di, board, empty_cells, b_bitmask, cells)
                            if new_b_bitmask not in visited_states:
                                rec_core(counter + 1, max_counter, res + [(cells[j_, i_], cells[j, i])], mj, mi, board, empty_cells, new_b_bitmask,
                                         visited_states, cells)
                                visited_states.add(new_b_bitmask)
                            # backtracking:
                            unjump(j, i, dj, di, board, empty_cells)


def good_neighs(j: int, i: int, mj: int, mi: int, board: list[list[str]]) -> int:
    mark = 0
    for dj, di in walk:
        if is_valid(_j := j + dj, _i := i + di, mj, mi) and is_valid(j_ := _j + dj, i_ := _i + di, mj, mi):
            if board[_j][_i] == 'O' and board[j_][i_] == 'O':
                mark += 1
    return mark


def is_valid(j: int, i: int, mj: int, mi: int) -> bool:
    return 0 <= j < mj and 0 <= i < mi


def normalize_board(board: str) -> list[list[str]]:
    rows = board.split('\n')
    return [[_ for _ in row] for row in rows if row]


def numerate(board: list[list[str]]) -> tuple[dict, int, int]:
    cells = {}
    b_bitmask = 0
    bit = 1
    counter = 1
    pigs_q = 0
    for j in range(len(board)):
        for i in range(len(board[0])):
            if board[j][i] != '_':
                cells[(j, i)] = counter
                counter += 1
                if board[j][i] == 'O':
                    b_bitmask |= bit
                    pigs_q += 1
                bit <<= 1
    return cells, pigs_q, b_bitmask


def jump(j: int, i: int, dj: int, di: int, board: list[list[str]], empty_cells: set[tuple[int, int]], b_bitmask: int,
         cells: dict) -> int:
    # the second pig fills the empty spot:
    board[j][i] = 'O'
    # the first pig annihilated by the second one:
    board[j + dj][i + di] = '.'
    # the spot of the 2nd pig is now empty:
    board[j + 2 * dj][i + 2 * di] = '.'
    # updating the empty_cells set:
    empty_cells.remove((j, i))
    empty_cells.add((j + dj, i + di))
    empty_cells.add((j + 2 * dj, i + 2 * di))
    # bitmask updating:
    b_bitmask |= 1 << (cells[(j, i)] - 1)
    b_bitmask ^= 1 << (cells[(j + dj, i + di)] - 1)
    b_bitmask ^= 1 << (cells[(j + 2 * dj, i + 2 * di)] - 1)
    return b_bitmask


def unjump(j: int, i: int, dj: int, di: int, board: list[list[str]], empty_cells: set[tuple[int, int]]) -> None:
    board[j][i] = '.'
    board[j + dj][i + di] = 'O'
    board[j + 2 * dj][i + 2 * di] = 'O'
    # updating the empty_cells set:
    empty_cells.remove((j + dj, i + di))
    empty_cells.remove((j + 2 * dj, i + 2 * di))
    empty_cells.add((j, i))


example_board_1 = '''\
_O.
.OO
O..'''

example_board_2 = '''\
_O__
_.OO
_O.O
OOOO'''

example_board_3 = '''\
__OOO__
OOO.OOO
OOOOOOO
__OOO__'''

ex_4 = '''\
_OOOO_
OOOOOO
OO.OOO
OOOOOO
_OOOO_'''

ex_q = '''\
.___
OOO_
OOOO
.OO_
_O__'''


ex_z = '''\
_OOO_
___O_
___._
.O.OO'''

print(f'result: {solve(ex_4)}')
print(f'rec_counter: {rec_counter}')

# print(f'sum: {sum([[1], [1, 9], [2, 98]], start=[])}')
# print(f'{1 << 1}')
