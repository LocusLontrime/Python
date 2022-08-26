import sys
import threading
import time
from functools import reduce

board: list[list[int]]
flag: bool

# knight_moves = [[-2, -1, 1, 2, 2, 1, -1, -2], [1, 2, 2, 1, -1, -2, -2, -1]]  # -> js and is
knight_moves = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]


def get_moves(size: int) -> list[list[int]]:
    global board, flag

    flag = True
    board = [[0] * size for _ in range(size)]

    def is_move_valid(curr_j: int, curr_i: int):
        global board

        return 0 <= curr_j < len(board) and 0 <= curr_i < len(board[0])

    # Warnsdorf's heuristic
    def next_possible_moves(curr_j, curr_i):
        return reduce(lambda y, x: y + (1 if ( is_move_valid(curr_j + x[0], curr_i + x[1]) and board[curr_j + x[0]][curr_i + x[1]] == 0 ) else 0), knight_moves, 0)

    def recursive_seeker(j: int, i: int, counter: int):

        # time.sleep(0.1)

        def sort_by_warnsdorfs_heuristic(e):
            return e[2]

        global board, flag

        if counter == size * size + 1:
            flag = False

        best_coordinates = []

        # cycling all over knight moves from the position (j, i)
        for move in knight_moves:
            new_j, new_i = j + move[0], i + move[1]
            if is_move_valid(new_j, new_i) and board[new_j][new_i] == 0:
                best_coordinates.append([new_j, new_i, next_possible_moves(new_j, new_i)])

        best_coordinates = sorted(best_coordinates, key=sort_by_warnsdorfs_heuristic)

        print(f'best coordinates: {best_coordinates}, counter: {counter}')

        for best_move in best_coordinates:
            if flag:
                board[best_move[0]][best_move[1]] = counter
                recursive_seeker(best_move[0], best_move[1], counter + 1)
                if flag:
                    board[best_move[0]][best_move[1]] = 0

    board[0][0] = 1
    recursive_seeker(0, 0, 2)

    return board


sys.setrecursionlimit(1000000)
# threading.stack_size(200000000)
# t = threading.Thread(target=get_moves)
# t.start()

bs = get_moves(43)

for b in bs:
    print(b)
