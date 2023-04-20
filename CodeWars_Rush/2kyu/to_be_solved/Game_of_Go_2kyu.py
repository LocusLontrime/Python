import re
from functools import reduce


class Go:  # LL 36 366 98 989
    """represents a playable game of Go for two players"""

    class Hash:
        """aux class for Go game class, represents a board hash, mutable"""

        def __init__(self, height: int, width: int):
            self._height = height
            self._width = width
            self._hash = 0
            self._hashes_ordered = {0: 0}

        @property
        def hash(self):
            return self._hash

        @property
        def hashes_ordered(self):
            return self._hashes_ordered

        def show_hashes(self):
            for k, v in self._hashes_ordered.items():
                print(f'{k}th turn hash: {v}')

        def num(self, y: int, x: int) -> int:
            return y * self._width + x

        def yx(self, num: int) -> tuple[int, int]:
            return divmod(num, self._width)

        def dhash(self, stone: tuple[int, int], black: bool = True, add: bool = True) -> None:
            """calculates the hash change after appending (add = True) a black (black = True) or white (black = False) stone
            or after removing it (add = False)"""
            self._hash += (1 if add else -1) * (1 if black else 2) * 3 ** self.num(*stone)

        def check_ko_rule(self, turn: int) -> bool:
            """checks the enforcement of the following KO rule:
            player cannot recreate the same board as the board after one of the previous moves"""
            if turn > 2 and self.hash == self._hashes_ordered[turn - 2]:
                return False
            else:
                self._hashes_ordered[turn] = self.hash
                return True

        def order(self, turn: int) -> None:
            self._hashes_ordered[turn] = self.hash

        def reset(self):
            self._hash = 0
            self._hashes_ordered = {0: 0}

        def rollback(self, turn, turns: int):
            for turn_ in range(turn + 1, turn + turns + 1):
                del self._hashes_ordered[turn_]
            self._hash = self._hashes_ordered[turn]

        def get_board(self, turn: int):
            return self.decode_board(self._hashes_ordered[turn])

        def decode_board(self, hash_: int) -> list[list[str]]:
            board = [[Go.EMPTY for _ in range(self._width)] for _ in range(self._height)]

            def decoder(rem: int) -> list[int]:
                if rem > 0:
                    yield rem % (d := len(Go.symbols))
                    yield from decoder(rem // d)

            dec = list(decoder(hash_))
            # print(f'seq: {dec}')
            for ind, key in enumerate(dec):
                y_, x_ = self.yx(ind)
                board[y_][x_] = Go.symbols[key]
            return board

    alphas = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
    symbols = {0: '.', 1: 'x', 2: 'o'}
    BLACK, WHITE, EMPTY = 'x', 'o', '.'
    HANDICAPS = {
        9: [5, [(2, 6), (6, 2), (6, 6), (2, 2), (4, 4)]],
        13: [9, [(3, 9), (9, 3), (9, 9), (3, 3), (6, 6), (6, 3), (6, 9), (3, 6), (9, 6)]],
        19: [9, [(3, 15), (15, 3), (15, 15), (3, 3), (9, 9), (9, 3), (9, 15), (3, 9), (15, 9)]]
    }
    STONE_PAIRS = {BLACK: WHITE, WHITE: BLACK}

    def __init__(self, height: int, width: int = None) -> None:
        self._height = height
        self._width = width if width is not None else height
        if not (0 < self._width <= len(Go.alphas) and 0 < self._height < len(Go.alphas)):
            raise ValueError(f'Board cannot be larger than 25 by 25')
        # print(f'h, w: {self._height, self._width}')
        self._board = [[Go.EMPTY for _ in range(self._width)] for _ in range(self._height)]
        self._turn = 0
        # memoization: previous board's states:
        self._hash = Go.Hash(self._height, self._width)
        # handicap stones used:
        self._handicaps_used = False
        # core:
        self._black_islands: list[Island] = []
        self._white_islands: list[Island] = []

    def __str__(self) -> str:
        return '\n'.join([' '.join(row) for row in self._board])

    @property
    def hash(self):
        return self._hash

    @property
    def turn(self):
        return 'black' if self._turn % 2 == 0 else 'white'

    @property
    def board(self):
        return self._board

    @property
    def stone(self):
        return Go.BLACK if self._turn % 2 == 0 else Go.WHITE

    @property
    def black(self):
        return self._turn % 2 == 0

    @property
    def size(self):
        return {"height": self._height, "width": self._width}

    @property
    def islands(self):
        def numerate(num: int) -> str:
            if num < 0:
                raise ValueError(f'Value: {num} is invalid, num cannot be less than zero! ')
            match num:
                case 1:
                    res = 'st'
                case 2:
                    res = 'nd'
                case 3:
                    res = 'rd'
                case _:
                    res = 'th'
            return f'{num}{res}'

        blacks = '\n'.join(f'{numerate(i + 1)} {_}' for i, _ in enumerate(self._black_islands))
        whites = '\n'.join(f'{numerate(i + 1)} {_}' for i, _ in enumerate(self._white_islands))
        return f'black islands:\n{blacks}\nwhite islands:\n{whites}'

    def parse_pos(self, pos: str) -> tuple[int, int]:
        """parses the position from str to tuple of ints"""
        return self._height - int(re.findall(r'\d+', pos)[0]), Go.alphas.index(re.findall(r'[A-Z]+', pos)[0])

    def get_position(self, pos: str) -> str:
        """gets status of a particular position on the board (x, o, or .)"""
        y, x = self.parse_pos(pos)
        return self._board[y][x]

    def validate(self, y: int, x: int) -> bool:
        """validates position"""
        return 0 <= y < self._height and 0 <= x < self._width

    def check_islands(self):
        """finds all the islands after rollback..."""
        # memoization of visited cells:
        visited = [[False for _ in range(self._width)] for _ in range(self._height)]
        stones_: set[tuple[int, int]]
        neighs_: set[tuple[int, int]]

        # clearing core pars:
        self._black_islands = []
        self._white_islands = []

        def dfs(y_: int, x_: int) -> int:
            if self.validate(y_, x_):
                if self._board[y_][x_] == symb_ and not visited[y_][x_]:
                    # appending a stone:
                    stones_.add((y_, x_))
                    # visiting:
                    visited[y_][x_] = True
                    # further steps:
                    area = 0
                    for dy, dx in Island.dydx:
                        area += dfs(y_ + dy, x_ + dx)
                    return area + 1
                else:
                    # appending an empty neigh:
                    neighs_.add((y_, x_))
                    return 0
            return 0

        # counter for the new islands:
        icounter = 0
        for y in range(self._height):
            for x in range(self._width):
                symb_ = self._board[y][x]
                if not visited[y][x] and symb_ != Go.EMPTY:
                    stones_ = set()
                    neighs_ = set()
                    # here dfs starts:
                    dfs(y, x)
                    # island creating:
                    island_ = Island(self._board, self._hash, None, symb_ == self.BLACK)
                    # island updating:
                    island_.update(stones_, neighs_)
                    # island appending to the Islands list:
                    (self._black_islands if symb_ == self.BLACK else self._white_islands).append(island_)
                    # islands counter incrementation:
                    icounter += 1
        # print(f'{icounter} new islands have been found and appending to the list...')

    def create_island(self, stone: tuple[int, int]) -> 'Island':
        """creates an island with player's stone at (y, x)"""
        island = Island(self._board, self._hash, stone, self.black)
        island.append(self._black_islands, self._white_islands)
        return island

    def move(self, *positions) -> None:
        for pos_ in positions:
            self.move_(pos_)

    def move_(self, pos: str) -> None:
        """player makes a move"""
        flag = False
        stone = (y, x) = self.parse_pos(pos)
        # print(f'move: {pos}, turn: {self._turn + 1}')
        # print(f'Now {self.turn}s is moving... trying to locate a {self.turn} stone at {y, x} position!')
        if self.validate(y, x):
            # checks if the cell has already been occupied by this or the another player...
            if self._board[y][x] == self.stone:
                raise ValueError(f'the cell has already been occupied by yourself: {self.stone}')
            elif self._board[y][x] == self.EMPTY:
                # here we place a stone:
                self._board[y][x] = self.stone
                allies, aliens = [], []
                for black_island in self._black_islands:
                    if stone in black_island.neighs:
                        (allies if self.black else aliens).append(black_island)
                for white_island in self._white_islands:
                    if stone in white_island.neighs:
                        (aliens if self.black else allies).append(white_island)
                for alien in aliens:
                    if alien.liberties == 0:
                        # opponent stone-group's capturing:
                        alien.remove(self._black_islands, self._white_islands)
                        # print(f'{Go.STONE_PAIRS[self.stone]} group of {alien.size} stones has just been captured!')
                        for y_, x_ in alien.stones:
                            # board altering:
                            self._board[y_][x_] = Go.EMPTY
                        # print(f'all the captured stones have been removed!')
                if allies:
                    # print(f'unifying {self.turn} islands: ')
                    sum_ = reduce(lambda a, b: a + b, allies)
                    if not sum_.add_stone(stone):
                        flag = True
                    else:
                        for ally in allies:
                            ally.remove(self._black_islands, self._white_islands, need_to_hash=False)
                        sum_.append(self._black_islands, self._white_islands)
                else:
                    # print(f'a new Island has just been created')
                    island = self.create_island(stone)
                    if not island.liberties:
                        flag = True
            else:
                raise ValueError(f'the cell has already been occupied by your opponent: {Go.STONE_PAIRS[self.stone]}')
        else:
            raise ValueError(f'the position {y, x} is out of bounds')
        # turns counter's increasing:
        self._turn += 1
        # checks ko rule:
        if not self._hash.check_ko_rule(self._turn):
            self.rollback(1)
            raise ValueError(f'ko rule violation! the current board state repeats the previously one...'
                             f'rolling back to the previous state...')
        if flag:
            self.rollback(1)
            raise ValueError(
                f'self-capturing is strictly prohibited!.. violation detected at the cell: {y, x}')
        # showing the current board's state:
        # print(f'{self}')
        # print(self.islands)
        # self._hash.show_hashes()

    def pass_turn(self):
        """current player passes his turn"""
        # print(f'{self.turn}s pass their turn')
        self._turn += 1
        self._hash.order(self._turn)

    def reset(self):
        """Resets the board, clears all the stones from it and sets the turn to black"""
        self._board = [[Go.EMPTY for _ in range(self._width)] for _ in range(self._height)]
        self._turn = 0
        self._black_islands: list[Island] = []
        self._white_islands: list[Island] = []
        self._handicaps_used = False
        self._hash.reset()
        # print(f'The board has been reset to default state...')

    def handicap_stones(self, q: int):
        """places some handicap stones in the correct order, works only for 9x9, 13x13 and 19x19 boards"""
        if not self._handicaps_used and self._turn == 0:
            if self._height == self._width and self._height in Go.HANDICAPS.keys():
                if 0 <= q <= (m := Go.HANDICAPS[self._height][0]):
                    for i in range(q):
                        y_, x_ = Go.HANDICAPS[self._height][1][i]
                        self._board[y_][x_] = Go.BLACK
                        self._hash.dhash((y_, x_), black=True, add=True)
                    self._handicaps_used = True
                else:
                    raise ValueError(
                        f'invalid handicap stones quantity, it must be larger than {0} and less or equal to {m}...')
            else:
                raise ValueError(f"invalid board size, board's height and width should be equal to 9, 13 or 19...")
        else:
            raise ValueError(f'handicap stones have been already used...')
        # print(f'{self}')

    def rollback(self, turns_back: int):
        """rollbacks a set amount of turns on the go board"""
        # print(f'rolling back by {turns_back} turns...')
        if turns_back < 0 or turns_back > self._turn:
            raise ValueError(f'turns_back cannot be less than {0} or larger than the turns made: {self._turn}...')
        else:
            self._turn -= turns_back
            # print(f'turn after rollback: {self._turn}')
            # rolling back the board state by 'turns_back' turns back:
            self._board = self._hash.get_board(self._turn)
            # core pars updating:
            self.check_islands()
            # memo updating and hash class change:
            self._hash.rollback(self._turn, turns_back)
            # print(f'the board after rollback:\n{self}')


class Island:
    """represents a set of linked stones of the same colour on the Go-board"""
    dydx = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, board: list[list[str]], hash_: Go.Hash, stone: tuple[int, int] = None, black: bool = True):
        # outer link:
        self._board = board  # <<-- the link to the Go game board from Go class...
        self._hash = hash_
        # True means black while False means white...
        self._player = black
        # core pars:
        self._stones: set[tuple[int, int]] = {stone} if stone is not None else set()
        self._neighs: set[tuple[int, int]] = set()
        # initializing the first neighs:
        if stone is not None:
            self.get_neighs(stone)
        # altering the board and hash:
        if stone is not None and self.liberties:
            self._board[stone[0]][stone[1]] = self.symb
            self._hash.dhash(stone, black, add=True)

    @property
    def liberties(self):
        """gets the degree of liberty of the island"""
        # TODO: can be easily optimized by implementing a simple for-cycle
        #  with break condition after finding the first empty neigh...
        return sum(1 for (y_, x_) in self._neighs if self._board[y_][x_] == Go.EMPTY)

    @property
    def symb(self):
        return Go.BLACK if self._player else Go.WHITE

    @property
    def captured(self):
        """checks if the island can be captured"""
        return self.liberties == 0

    @property
    def stones(self):
        return self._stones

    @property
    def neighs(self):
        return self._neighs

    @neighs.setter
    def neighs(self, neighs):
        self._neighs = neighs

    @property
    def size(self):
        return len(self._stones)

    def __str__(self) -> str:
        return f"{'black' if self._player else 'white'} island:\nliberties: {self.liberties}\n" \
               f"stones: {self._stones}\nneighs: {self._neighs}"

    def __add__(self, other: 'Island') -> 'Island':  # stone: tuple[int, int], islands: list['Island']):
        """appends the other Island to the self one"""
        if self._player != other._player:
            raise ValueError(f"cannot add two islands with different stones' colours!..\n"
                             f"self: {self._player} != {other._player}")
        else:
            # creating a new Island:
            sum_ = Island(self._board, self._hash, None, self._player)
            # merging Islands' stones and neighs:
            sum_._stones = self._stones | other._stones
            sum_._neighs = self._neighs | other._neighs
            # returning sum of two Islands:
            return sum_

    def check_pos(self, y, x) -> bool:
        """checks the validity of the (y, x) position for the board"""
        return 0 <= y < len(self._board) and 0 <= x < len(self._board[0])

    def check_neighs(self, stone: tuple[int, int]) -> bool:
        """checks if the stone can be added to this Island"""
        return True if stone in self._neighs else False

    def check_stone(self, stone: tuple[int, int]) -> bool:
        """check if the stone can be removed from this Island"""
        return True if stone in self._stones else False

    def get_neighs(self, stone: tuple[int, int]) -> None:
        """adds all the valid neighbouring cells (horizontally and vertically connected only)
        to the Island's neighs set"""
        # print(f'getting neighs for a stone: {stone}')
        for dy, dx in Island.dydx:
            neigh_ = (y_ := stone[0] + dy, x_ := stone[1] + dx)
            if self.check_pos(y_, x_):
                if self._board[y_][x_] != self.symb:
                    self._neighs.add(neigh_)

    def add_stone(self, stone: tuple[int, int]) -> bool:
        """adds a stone to the Island"""
        # TODO: is it needed to check the stone inside of this method beforehand?..
        # at first, this stone should be removed from neighs (liberties decreases by 1):
        self._neighs.remove(stone)
        # secondly, it must be added to stones:
        self._stones.add(stone)
        # thirdly, we have to find all the new neighs for the stone:
        self.get_neighs(stone)
        # check if now liberties are equal to zero (# then remove the Island from the list if so):
        if self.liberties == 0:
            return False
        # finally we can alter the board:
        self._board[stone[0]][stone[1]] = self.symb
        self._hash.dhash(stone, self._player, add=True)
        return True

    def remove(self, black_islands: list['Island'], white_islands: list['Island'], need_to_hash: bool = True):
        """removes the island from the islands list"""
        (black_islands if self._player else white_islands).remove(self)
        if need_to_hash:
            for stone_ in self._stones:
                self._hash.dhash(stone_, self._player, add=False)

    def append(self, black_islands: list['Island'], white_islands: list['Island']):
        """appends the island to the islands list"""
        (black_islands if self._player else white_islands).append(self)

    def update(self, stones: set[tuple[int, int]], neighs: set[tuple[int, int]]):
        if self._stones or self._neighs:
            raise ValueError(f'the island cannot be updated because it is not an empty one...'
                             f'it contains {self.size} stones and {self.liberties} neighs')
        self._stones |= stones
        self._neighs |= neighs



