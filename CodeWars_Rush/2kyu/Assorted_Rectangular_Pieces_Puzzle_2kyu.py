# accepted on codewars.com
import random
import time
from collections import defaultdict as d

rec_counter: int
THRESHOLD = 1_000
DELTA = 2  # important par for random run...


def solve_puzzle(board: list[str], pieces: list[list[int]]):  # 36 366 98 989 LL
    global rec_counter
    rec_counter, counter = 0, 0
    print(f'len: {len(pieces)}')
    print(f'pieces: {pieces}')
    for row in board:
        print(f'"{row}",')
    # pieces' indices dict and equal pieces counting::
    pieces_indices, pieces_dict = d(set), d(int)
    for i, (h, w) in enumerate(pieces):
        pieces_indices[h, w].add(i)
        pieces_dict[(h, w)] += 1
    # reconstructing the board:
    board_nums = [[1 if board[j][i] == ' ' else 0 for i in range(len(board[0]))] for j in range(len(board))]
    # precalculating some prefix arrays:
    prefix_sums = [[0 for _ in range(len(board[0]) + 1)] for _ in range(len(board))]
    for j in range(len(board)):
        for i in range(len(board[0])):
            prefix_sums[j][i + 1] = prefix_sums[j][i] + board_nums[j][i]
    # building rows for every shape (piece):
    pieces_placements = {}
    for h, w in pieces_dict.keys():
        pieces_placements[(h, w)] = construct_rows(board_nums, [h, w], prefix_sums, rotated=False)
        pieces_placements[(h, w)] += construct_rows(board_nums, [w, h], prefix_sums, rotated=True) if h != w else []
    # starting rec algo:
    empty_cells = {j * len(board[0]) + i for i in range(len(board[0])) for j in range(len(board)) if board_nums[j][i] == 0}
    sol = None
    while not sol:
        rec_counter = 0
        sol = rec_placement(pieces_placements, pieces_dict, empty_cells, [])
        counter += 1
    res = [None for _ in range(len(pieces))]
    for piece, orientation, plcmnt in sol:
        i = pieces_indices[piece].pop()
        res[i] = [*divmod(min(plcmnt), len(board[0])), int(orientation)]
    print(f'res: {res}')
    print(f'rec counter: {rec_counter}')
    print(f'counter: {counter}')
    return res


def get_indices(j: int, i: int, piece: list[int], i_max: int) -> set[int]:
    return {i_max * j_ + i_ for i_ in range(i, i + piece[1]) for j_ in range(j, j + piece[0])}


def construct_rows(board: list[list[int]], piece: list[int], prefix_sums: list[list[int]], rotated: bool = False):
    rows = []
    for i in range(len(board[0]) + 1 - piece[1]):
        consecutives = 0  # 98
        for j in range(len(board)):
            # horizontal sum retrieving from prefix arrays:
            if row_sum(j, i, piece, prefix_sums) == 0:
                consecutives += 1
            else:
                consecutives = 0
            if consecutives >= piece[0]:
                rows.append((rotated, get_indices(j + 1 - piece[0], i, piece, len(board[0]))))
    # returning rows built:
    return rows


def row_sum(j: int, i: int, piece: list[int], prefix_sums: list[list[int]]) -> int:
    sum_ = prefix_sums[j][i + piece[1]] - prefix_sums[j][i]
    return sum_


def rec_placement(pieces_placements: dict[tuple[int, int], list[tuple[bool, set[int]]]],
                  pieces_dict: d[tuple[int, int], int],
                  empty_cells: set[int], sol: list):
    global rec_counter
    rec_counter += 1
    if rec_counter <= THRESHOLD:
        # border case:
        if len(empty_cells) == 0:
            return sol
        # searching fo the best piece:
        best_piece = sorted([k for k, v in pieces_dict.items() if v > 0], key=lambda k: (len(pieces_placements[k]), max(k)))[0]
        if best_piece:
            pieces_dict[best_piece] -= 1
            #  cycling through all the possible placements of this piece:
            used = set()
            for i in range(l_ := len(pieces_placements[best_piece])):  # , key=lambda el: min(el[2]))
                ind_ = random.randint(i, min(i + DELTA, l_ - 1))
                if ind_ not in used:
                    used.add(ind_)
                    orientation, placement = pieces_placements[best_piece][ind_]
                    if placement <= empty_cells:
                        # pieces_placements' changes done:
                        copy = {key: [(_, plcmnt) for _, plcmnt in val] for key, val in pieces_placements.items()}
                        for j, piece in enumerate(pieces_dict.keys()):  # enumerate(pieces := [i for i, v in pieces_dict.items() if v > 0])
                            pieces_placements[piece] = [(_, plcmnt) for _, plcmnt in pieces_placements[piece] if not plcmnt.intersection(placement)]
                        # recurrent relation:
                        if r := rec_placement(pieces_placements, pieces_dict, empty_cells - placement, sol + [(best_piece, orientation, placement)]):
                            return r
                        # pieces_placements' changes undone (backtracking):
                        for key, val in copy.items():
                            pieces_placements[key] = val
            # backtracking:
            pieces_dict[best_piece] += 1


board_1, pieces_1 = [
    '     0  ',
    ' 00  0  ',
    ' 00     ',
    ' 00     ',
    '   0    ',
    '       0',
    '       0',
    '0000   0'], [[1, 1], [1, 2], [1, 3], [1, 4], [2, 3]]

board_2 = [
    '          ',
    '          ',
    '  00  00  ',
    '  00  00  ',
    '          ',
    ' 0  00  0 ',
    ' 00    00 ',
    '  000000  ',
    '  000000  ',
    '          '
]

pieces_2 = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 4], [2, 2], [2, 2]]

board_3 = [
    "   0000000000   ",
    "      0000      ",
    "      0000      ",
    " 00000000000000 ",
    " 00000000000000 ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "     00000      ",
    "    000 00   00 ",
    "  0000  0000000 ",
    " 000    0000000 ",
    "                "
]

pieces_3 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [1, 4], [1, 4], [1, 4], [1, 5], [1, 7], [1, 7], [1, 12], [2, 2], [2, 2], [2, 3], [2, 4], [2, 5]]

board_4 = [
    "  00       0    ",
    "          00    ",
    " 0000      00   ",
    "  0000000   0000",
    " 000   00   0000",
    " 000  0000000000",
    "0000  0 00000000",
    "0   000 0000 000",
    "0 000   0000 000",
    "  000   0000  00",
    "  000  00000   0",
    "  000000        ",
    "     000000     ",
    " 00  00   00    ",
    " 00  00    0    ",
    " 00  00    0    "
]

pieces_4 = [[1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [1, 4], [1, 4], [1, 7], [2, 2], [2, 2], [2, 3], [2, 5], [3, 3], [3, 4], [4, 4], [4, 5]]

board_5 = [
    "     0          ",
    "     0      0   ",
    " 00000   0  0   ",
    " 0000     0000  ",
    " 0000000000  0  ",
    " 000000000  00  ",
    " 0000000000000  ",
    " 000000000000   ",
    "  00000000000   ",
    "   0000000   0  ",
    "    0  000   000",
    "           0    ",
    "        00 0    ",
    "     0000000    ",
    " 000000    0 0  ",
    "00           0  "]

pieces_5 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3],
            [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 6], [1, 6], [2, 2], [3, 3], [4, 6], [5, 5]]

board_6 = [
    "00     000     ",
    " 000           ",
    " 000  0  0000  ",
    " 000  00 00000 ",
    " 000  00  0000 ",
    "  00  00     0 ",
    "  00  00  00000",
    "  00000000000  ",
    "   00    0     ",
    "   00  000 00  ",
    "       000  00 ",
    "       000  00 ",
    "        0    0 ",
    "            00 ",
    "            0  "]

pieces_6 = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [1, 4], [1, 5], [1, 8], [2, 2], [2, 2], [2, 4], [3, 3], [3, 4]]

board_7 = [
    "              ",
    "          000 ",
    "  00 00000000 ",
    "   0000 00000 ",
    "    00  00000 ",
    "    00     0  ",
    "  0 000000 0  ",
    " 00000   000  ",
    " 00000   00   ",
    "     0        ",
    "   00000000   ",
    "   00000000   ",
    "   00000000   ",
    "              "]

pieces_7 = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 4], [1, 5], [1, 6], [2, 2], [2, 2],
            [2, 4], [3, 4], [3, 7]]

board_8 = [
    "             ",
    "             ",
    " 0000    00  ",
    "000000  0000 ",
    "00     00  00",
    "00     00  00",
    "00 000 00  00",
    "00 000 00  00",
    "00  00 00  00",
    "000000  0000 ",
    " 0000    00  ",
    "             ",
    "             "
]

pieces_8 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3],
            [1, 3], [1, 4], [1, 4], [1, 4], [1, 4], [1, 5], [2, 2], [2, 4], [2, 5]]

board_9 = [
    "            ",
    " 0 0     0  ",
    "00000   00  ",
    " 0 0  0000  ",
    "00000   00  ",
    " 0 0    00  ",
    "        00  ",
    "        00  ",
    "        00  ",
    "        00  ",
    "      000000",
    "            "
]

pieces_9 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [2, 2], [2, 5]]

board_10 = [
    "                    ",
    "        0000        ",
    "       000000       ",
    "      00000000      ",
    "      00000000      ",
    "      00000000      ",
    "      00000000      ",
    "      00 00 00      ",
    "     0000000000     ",
    "    000000000000    ",
    "   00000000000000   ",
    "  0000000000000000  ",
    "  0000000000000000  ",
    " 00  0        0  00 ",
    " 0   0        0   0 ",
    " 0   0        0   0 ",
    "        0  0        ",
    "        0000        ",
    "         00         ",
    "                    "
]

pieces_10 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2],
             [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 7], [1, 8],
             [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 7], [2, 8], [3, 3]]

board_11 = [
    "00       00         ",
    "00       00         ",
    "00       00    0000 ",
    "0000     000000000  ",
    "0000000000 00  000  ",
    "00         00  000  ",
    "00         00  000  ",
    " 000000000000     0 ",
    "  0000  0   0000  0 ",
    "    000000000000  0 ",
    "    000000000000 000",
    "  0000 000000000 0  ",
    "  000000 0000000 0  ",
    "      0000       0  ",
    "                 0  ",
    "               000  ",
    "  0            00   ",
    " 000      000000    ",
    " 00       00        ",
    "   00   00000       "
]

pieces_11 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3],
             [1, 4], [1, 4], [1, 4], [1, 4], [1, 6], [1, 12], [2, 2], [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 4],
             [2, 4], [2, 5], [2, 7], [3, 5], [4, 7]]

board_12 = [
    "       00 ",
    "00  00000 ",
    "000  00   ",
    "00   00   ",
    "000  00   ",
    "00   00   ",
    "000  00   ",
    "          ",
    "   0000000",
    " 000      "
]

pieces_12 = [[1, 1], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 7], [2, 2], [2, 6]]

board_13 = [
    "0000        ",
    "   00000    ",
    "   0 000    ",
    "000000 000  ",
    "000000 0 000",
    "0000000000 0",
    "000 000000 0",
    "000000 00 0 ",
    "  0 000 0000",
    " 0000 00 0 0",
    "    000 0000",
    "    000 0   "
]

pieces_13 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2],
             [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 4], [2, 2], [2, 3], [2, 3], [2, 4], [2, 5],
             [3, 3]]

board_14 = [
    "         00     ",
    "         00     ",
    "         00     ",
    "   00000000     ",
    "   00000 000    ",
    "   000 0   0    ",
    "000000 000000000",
    "000000 000000000",
    "000 00 00000000 ",
    "000000 00000000 ",
    "0 0000 0000000  ",
    "  00 0 0000000  ",
    "  00 000000000  ",
    "  00 000   00   ",
    "  0000 000000   ",
    "           0    "
]

pieces_14 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2],
             [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [2, 5],
             [2, 7], [3, 3], [5, 5]]

board_15 = [
    "       0            ",
    "       0  0000000000",
    "       0000  0000000",
    "       0000000      ",
    "      00000000000   ",
    "000  0000    0000   ",
    "000 000       000   ",
    "000 00        000   ",
    "000 00 000000 000   ",
    "    000000000 000   ",
    " 0000 0  0  0 000   ",
    "00  000000000 000   ",
    "00  00000000  000   ",
    "00  00 00000000000  ",
    "00   000        000 ",
    " 0   00 0   000 000 ",
    " 0   00 00000 00000 ",
    " 0      000000  000 ",
    " 0       0000       ",
    " 0       0000       "
]

pieces_15 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3],
             [1, 3], [1, 4], [1, 4], [1, 4], [1, 5], [1, 11], [2, 2], [2, 3], [2, 3], [2, 4], [2, 4], [2, 4], [2, 6],
             [2, 6], [2, 7], [3, 4], [3, 4], [3, 9], [4, 4]]

board_16 = [
    "00         0 0  ",
    "00  0 000   0  0",
    "00   0 00 00  0 ",
    "00  0 0  0   0  ",
    "0000 0000 0 0 0 ",
    "  00 0000  0 0  ",
    "  0  000 0  0 00",
    " 000 0000  0 0  ",
    " 000 0000 0 0 0 ",
    " 000 0 0  00  0 ",
    " 000 0000000 000",
    " 0 00    000    ",
    " 00 000000  0 0 ",
    " 00 00000 0  0  ",
    "00 0 0000 00  0 ",
    "     0000    0  "
]

pieces_16 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
             [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
             [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
             [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 4],
             [1, 4], [1, 5], [2, 2], [2, 2], [2, 3], [2, 4], [2, 4], [2, 5], [4, 4]]

board_17 = [
    "   00  0       0   0  0 ",
    "   00  0      0000000000",
    "    000000    0000000000",
    "  00000       0000000000",
    "   0000000    0000000000",
    "       0      0000000000",
    "000000000     0000000000",
    "000000000     0000000000",
    "0000000 000   0000000000",
    "       0000   0000000000",
    "      00000   0000000000",
    "00000000000 000    0000 ",
    "00000000000 00   00 0   ",
    "00000000000 00000 00    ",
    " 000 000    00000 0 0   ",
    "   00000  000000000  000",
    "   00     000  000000000",
    "   0000   0000000000000 ",
    "   0000   000000     00 ",
    "     00000000000     000",
    "        00000000 00  000",
    "        0000000 000  000",
    "        00000000000  00 ",
    "              00000  00 "
]
pieces_17 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2],
             [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 4], [1, 4], [1, 5],
             [1, 5],
             [1, 6], [2, 2], [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 3], [2, 4], [2, 4], [2, 4], [2, 4], [2, 4],
             [2, 5],
             [2, 9], [3, 6], [3, 7], [4, 5], [4, 6], [10, 10]]

inputs = [(board_1, pieces_1),
          (board_2, pieces_2),
          (board_3, pieces_3),
          (board_4, pieces_4),
          (board_5, pieces_5),
          (board_6, pieces_6),
          (board_7, pieces_7),
          (board_8, pieces_8),
          (board_9, pieces_9),
          (board_10, pieces_10),
          (board_11, pieces_11),
          (board_12, pieces_12),
          (board_13, pieces_13),
          (board_14, pieces_14),
          (board_15, pieces_15),
          (board_16, pieces_16),
          (board_17, pieces_17)]

start = time.time_ns()
for ind, input_ in enumerate(inputs, 1):
    print(f'board {ind}: ')
    solve_puzzle(*input_)
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
