import time
from collections import defaultdict as d

rec_counter: int


def solve_puzzle(board: list[str], pieces: list[list[int]]):  # 36 366 98 989 LL
    global rec_counter
    # your code goes here. you can do it!
    # print(f'len: {len(pieces)}')
    # print(f'pieces: {pieces}')
    # for row in board:
    #     print(f'{row}')
    # reconstructing the board:
    board_nums = []
    short_nums = {}
    long_nums = {}
    short_num = 0
    for j, string in enumerate(board):
        board_nums.append([])
        for i, x in enumerate(string):
            if x == ' ':
                board_nums[j].append(1)
            else:
                board_nums[j].append(0)
                long_num = j * len(board[0]) + i
                short_nums[long_num] = short_num
                long_nums[short_num] = long_num
                short_num += 1
    print(f'board: ')
    for row in board_nums:
        print(f'{row}')
    print(f'short_nums: {short_nums}')
    print(f'long_nums: {long_nums}')
    area = sum([row.count(0) for row in board_nums])
    print(f'area: {area}')
    # precalculating some prefix arrays:
    prefix_sums = [[0 for _ in range(len(board[0]) + 1)] for _ in range(len(board))]
    for j in range(len(board)):
        for i in range(len(board[0])):
            prefix_sums[j][i + 1] = prefix_sums[j][i] + board_nums[j][i]
    # equal pieces counting:
    pieces_dict = d(int)
    translate = {}
    counter = 0
    for j, i in pieces:
        if (piece := (j, i)) not in pieces_dict.keys():
            translate[piece] = counter
            counter += 1
        pieces_dict[piece] += 1
    print(f'pieces_q: {pieces_dict}')
    print(f'translate: {translate}')
    reversed_translate = {v: k for k, v in translate.items()}
    print(f'reversed_translate: {reversed_translate}')
    pieces_q = {translate[k]: v for k, v in pieces_dict.items()}
    print(f'pieces_q: {pieces_q}')
    # building rows for every shape (piece):
    piece_number = 0
    pieces_placements = {}
    for h, w in pieces:
        print(f'PIECE: {h, w}...............................................................')
        pieces_placements[(h, w)] = construct_rows(board_nums, [h, w], short_nums, prefix_sums)
        if h != w:
            pieces_placements[(h, w)] += construct_rows(board_nums, [w, h], short_nums, prefix_sums)
        piece_number += 1
    # starting knuth's algorithm x:
    rec_counter = 0
    empty_cells = {_ for _ in range(area)}
    print(f'empty_cells: {empty_cells}')
    sol = rec_placement(pieces_placements, pieces_dict, empty_cells, [])
    sol.sort(key=lambda k: k[0])
    # sol = [[ln.j, *divmod(long_nums[ln.i], len(board[0])), ln.orientation] for ln in sol]
    # sol.sort(key=lambda k: k[0])
    # sol = [el[1:] for el in sol]
    # print(f'solutions: ')
    print(f'{sol}')
    print(f'rec_counter: {rec_counter}')
    return sol


def get_indices(j: int, i: int, piece: list[int], i_max: int, short_nums: dict[int, int]) -> set[int]:
    return {short_nums[i_max * j_ + i_] for i_ in range(i, i + piece[1]) for j_ in range(j, j + piece[0])}


def construct_rows(board: list[list[int]], piece: list[int], short_nums: dict[int, int],
                   prefix_sums: list[list[int]]):
    # print(f'piece: {piece}')
    # rows:
    rows = []
    # creating aux matrix:
    for i in range(len(board[0]) + 1 - piece[1]):
        consecutives = 0
        for j in range(len(board)):
            if prefix_sums[j][i + piece[1]] - prefix_sums[j][i] == 0:
                consecutives += 1
            else:
                consecutives = 0
            if consecutives >= piece[0]:
                rows.append(get_indices(j + 1 - piece[0], i, piece, len(board[0]), short_nums))
    print(f'rows built: ')
    for i, row in enumerate(rows, 1):
        print(f'{i}th: {row}')
    # returning rows built:
    return rows


def rec_placement(pieces_placements: dict[tuple[int, int], list[set[int]]], pieces_dict: d[tuple[int, int], int],
                  empty_cells: set[int], sol: list):
    global rec_counter
    rec_counter += 1
    if rec_counter % 10_000 == 0:
        print(f'rec_counter: {rec_counter}')
    # print(f'{rec_counter}th placing... {pieces_dict}, empty cells: {empty_cells}')
    # border case:
    if len(empty_cells) == 0:
        print(f'SOLUTION FOUND!!!')
        return sol
    # body of rec:
    for piece in sorted(pieces_dict.keys(), key=lambda x: (-x[0] * x[1], -max(*x))):
        if pieces_dict[piece] > 0:
            pieces_dict[piece] -= 1
            # cycling through all the possible placements of this piece:
            for placement in pieces_placements[piece]:
                if placement <= empty_cells:
                    if r := rec_placement(pieces_placements, pieces_dict, empty_cells - placement,
                                          sol + [(piece, placement)]):
                        return r
            # backtracking:
            pieces_dict[piece] += 1


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

# solve_puzzle(board_1, pieces_1)
# solve_puzzle(board_2, pieces_2)
# solve_puzzle(board_3, pieces_3)
# solve_puzzle(board_8, pieces_8)
# solve_puzzle(board_9, pieces_9)
# solve_puzzle(board_10, pieces_10)
solve_puzzle(board_11, pieces_11)

# set1 = {1, 3, 5}
# set2 = {1, 3, 5, 7, 9, 8, 98}
# print(f'{set1 < set2}')
# print(f'{set2 - set1}')
