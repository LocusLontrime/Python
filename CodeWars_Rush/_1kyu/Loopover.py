# accepted on codewars.com
import time
from typing import List, Optional

alphabet = f"abcdefghijklmnopqrstuvwxyz"


def loopover(mixed_up_board: List[List[str]], solved_board: List[List[str]]) -> Optional[List[str]]:
    game_board = Board(mixed_up_board, solved_board)
    solvable = game_board.reset()
    if solvable:
        return game_board.moves
    return None


def board(board_str: str) -> list[list[str]]:
    return [[ch for ch in row] for row in board_str.split('\n')]


class Board(object):
    def __init__(self, mixed_up_board: List[List[str]], solved_board: List[List[str]]):
        self.board = mixed_up_board
        self.init = solved_board
        self.size_y, self.size_x = len(mixed_up_board), len(mixed_up_board[0])
        self.moves = []

    def print(self):
        for row in self.board:
            print(row)

    # Here we are moving the board back to the initial alphabetical
    # state given, recording the moves meanwhile:
    def reset(self):
        goal_row, goal_col = 0, 0
        # core cycle:
        while True:
            letter = self.init[goal_row][goal_col]
            row_dx, col_dx = self.find(letter)
            self.move(row_dx, col_dx, goal_row, goal_col)
            goal_row, goal_col = self.increment(goal_row, goal_col)
            # the last row is always ordered correctly, so once we
            # place the left-most letter in the row we're done
            if goal_row == self.size_y - 1 and goal_col == 1:
                break
        # last row check:
        if self.board[-1] != self.init[-1]:
            # solution found or not:
            return self.move_secretly()
        # solution found:
        return True

    # increment the goal row and column indexes, wrapping as needed
    def increment(self, goal_r, goal_c):
        goal_c += 1
        if goal_c == self.size_x:
            goal_c = 0
            goal_r += 1
        return goal_r, goal_c

    # rotate the provided row index to the left,
    # returning the new column index for the provided column index (including wrapping)
    def left(self, rdx, cdx):
        row = self.board[rdx]
        self.board[rdx] = row[1:] + [row[0]]
        self.moves += [f'L{rdx}']
        cdx -= 1
        if cdx < 0:
            cdx = self.size_x - 1
        return cdx

    # rotate the provided row index to the right,
    # returning the new column index for the provided column index (including wrapping)
    def right(self, rdx, cdx):
        row = self.board[rdx]
        self.board[rdx] = [row[-1]] + row[0:-1]
        self.moves += [f'R{rdx}']
        cdx += 1
        if cdx == self.size_x:
            cdx = 0
        return cdx

    # rotate the provided column index up,
    # returning the new row index for the provided row index (including wrapping)       # 36 366 98 989 98989 LL
    def up(self, cdx, rdx):
        last = self.board[0][cdx]
        for r in range(0, self.size_y)[::-1]:
            tmp = self.board[r][cdx]
            self.board[r][cdx] = last
            last = tmp
        self.moves += [f'U{cdx}']
        rdx -= 1
        if rdx < 0:
            rdx = self.size_y - 1
        return rdx

    # rotate the provided column index down,
    # returning the new row index for the provided row index (including wrapping)
    def down(self, cdx, rdx):
        last = self.board[self.size_y - 1][cdx]
        for r in range(0, self.size_y):
            tmp = self.board[r][cdx]
            self.board[r][cdx] = last
            last = tmp
        self.moves += [f'D{cdx}']
        rdx += 1
        if rdx == self.size_y:
            rdx = 0
        return rdx

    # move the current index location to the goal index location
    # without disturbing prior letters
    # side effects both board and moves
    def move(self, rdx, cdx, goal_r, goal_c):
        # no change needed
        if rdx == goal_r and cdx == goal_c:
            return

        # letter just needs to move left to the start of the row
        if rdx == goal_r and goal_c == 0:
            while cdx > 0:
                cdx = self.left(rdx, cdx)
            return

        # if letter is on same row as goal row, move it down a row without permanently disturbing previously set letters to left and above
        if rdx == goal_r:
            rdx = self.down(cdx, rdx)  # move letter down a row
            origc = cdx
            cdx = self.left(rdx, cdx)  # move letter to left
            self.up(origc, rdx)  # move orig column without letter back up

        # move letter to right of goal column
        if goal_c == self.size_x - 1:
            while cdx > 0:
                cdx = self.left(rdx, cdx)
        else:
            while cdx <= goal_c:
                cdx = self.right(rdx, cdx)
            while cdx > goal_c + 1:
                cdx = self.left(rdx, cdx)

        # rotate goal column down so goal row is next to current row
        times = 0
        for i in range(goal_r, rdx):
            times += 1
            self.down(goal_c, rdx)

        # rotate row left to put letter into column
        cdx = self.left(rdx, cdx)

        # rotate column back up to original place
        for i in range(0, times):
            rdx = self.up(cdx, rdx)

    def move_secretly(self) -> bool:
        flag = True
        row_fingerprint = self.board[-1][:]
        while self.board[-1] != self.init[-1]:
            # finding indices:
            # 1. wi:
            wi = 1
            while wi < self.size_x:
                if self.board[self.size_y - 1][wi] != self.init[self.size_y - 1][wi]:
                    break
                wi += 1
            # 2. ri:
            ri = 1
            while ri < self.size_x:
                if self.board[self.size_y - 1][ri] == self.init[self.size_y - 1][wi]:
                    break
                ri += 1
            # swapping elements:
            flag = self.swap(wi, ri, flag)
            # check:
            if self.board[-1] == row_fingerprint:
                # raise ValueError(f'NO SOLUTION!!!')
                return False

        # check:
        if self.board == self.init:
            return True

        # tries to place the aux EL correctly:
        self.recharge_cycle()

        # new section:
        if self.board[0][-1] != self.init[0][-1]:
            self.up(self.size_x - 1, 0)
            self.fast_swap_col()
            self.up(self.size_x - 1, 0)
            # self.left(self.size_y - 1, 0)
            self.recharge_cycle_col()

        # fast-check:
        if self.board != self.init:
            # raise ValueError(f'NO SOLUTION!!!')
            return False

        return True

    def swap(self, wi: int, ri: int, flag: bool = True):
        # 5:
        while wi != self.size_x - 1:
            wi = self.right(self.size_y - 1, wi)
            # 7:
            ri = (ri + 1) % self.size_x
        # 6:
        if flag:
            self.down(self.size_x - 1, 0)
        else:
            self.up(self.size_x - 1, 0)
        # 8:
        while ri != self.size_x - 1:
            ri = self.right(self.size_y - 1, ri)
            # 10:
            wi = (wi + 1) % self.size_x
        # 9:
        if flag:
            self.up(self.size_x - 1, 0)
        else:
            self.down(self.size_x - 1, 0)
        # 11:
        while wi != self.size_x - 1:
            wi = self.right(self.size_y - 1, wi)
            # 7:
            ri = (ri + 1) % self.size_x
        # 12:
        if flag:
            self.down(self.size_x - 1, 0)
        else:
            self.up(self.size_x - 1, 0)
        # returning the last row to the initial position:
        i = self.find_row()
        while i != 0:
            i = self.left(self.size_y - 1, i)
        # returning not flag:
        return not flag

    def fast_swap_col(self):
        # wi = self.size_y - 2
        # ri = self.size_y - 1
        self.down(self.size_x - 1, 0)
        self.right(self.size_y - 1, 0)
        self.up(self.size_x - 1, 0)
        self.left(self.size_y - 1, 0)
        self.down(self.size_x - 1, 0)
        self.right(self.size_y - 1, 0)

    def recharge_cycle(self):
        for i in range(self.size_x + 1):
            if i % 2:
                self.down(self.size_x - 1, 0)
            else:
                self.up(self.size_x - 1, 0)
            self.right(self.size_y - 1, 0)

    def recharge_cycle_col(self):
        for j in range(self.size_y + 1):
            if j % 2:
                self.right(self.size_y - 1, 0)
            else:
                self.left(self.size_y - 1, 0)
            self.down(self.size_x - 1, 0)

    # find the row and col indexes of the letter
    def find(self, letter):
        for rdx in range(0, len(self.board)):
            row = self.board[rdx]
            for cdx in range(0, len(row)):
                if row[cdx] == letter:
                    return rdx, cdx
        raise Exception("letter not found")

    def find_row(self) -> int:
        for i in range(self.size_x):
            if self.board[self.size_y - 1][i] == self.init[self.size_y - 1][0]:
                return i
        raise Exception("letter not found")


# board_ = board("mGBlYpd\nFaKhCnE\ngHLVASP\nTboiQJj\nWZUfcNO\nRDeIkXM")
# init_board = board("ABCDEFG\nHIJKLMN\nOPQRSTU\nVWXYZab\ncdefghi\njklmnop")

# board_x = board("iDηqSγ9α\nu6Xxδ1mV\nfJRθhd4W\ncεgF5YAβ\ntλlμEykU\ne20NKQbG\nζ7vjZLMa\ns8wBoIrH\nO3zPnTCp")
# init_board_x = board("ABCDEFGH\nIJKLMNOP\nQRSTUVWX\nYZabcdef\nghijklmn\nopqrstuv\nwxyz0123\n456789αβ\nγδεζηθλμ")

# board_y = board("goaqpLYA\nSPNlCZsb\nUeHKmVWi\njFIuBhfk\nrETJXQDt\ncvOnGMRd")
# init_board_y = board("ABCDEFGH\nIJKLMNOP\nQRSTUVWX\nYZabcdef\nghijklmn\nopqrstuv")

# board_z = board("FBDSM\nNHELG\nJCORK\nTQAPI")
# init_board_z = board("ABCDE\nFGHIJ\nKLMNO\nPQRST")

board_zzz = board("JKVGSBI\nHYZNXUQ\nEbMOADF\nPWRTaCL")
init_board_zzz = board("ABCDEFG\nHIJKLMN\nOPQRSTU\nVWXYZab")

print(f'res: {loopover(board_zzz, init_board_zzz)}')

print(f'INIT BOARD: ')
for row_ in init_board_zzz:
    print(f'{row_}')
