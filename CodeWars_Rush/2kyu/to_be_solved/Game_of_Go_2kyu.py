import re
from functools import reduce


class Go:
    """represents a playable game of Go for two players"""
    alphas = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
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
        self._board = [[Go.EMPTY for _ in range(self._width)] for _ in range(self._height)]
        self._turn = 0
        # previous board's states:
        self._states = set()
        self._states.add(self._board)
        # memoization:
        # TODO: to think about implementation and further optimization of a rollback system...
        self._memo: dict[int, list[list[str]]] = dict()
        # handicap stones used:
        self._handicaps_used = False
        # core:
        self._black_islands: list[Island] = []
        self._white_islands: list[Island] = []

    def __str__(self) -> str:
        return '\n'.join([' '.join(row) for row in self._board])

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

        def dfs(y_: int, x_: int) -> int:
            if self._board[y_][x_] == symb_:
                # appending a stone:
                stones_.add((y_, x_))
                # visiting:
                visited[y][x] = True
                # further steps:
                area = 0
                for dy, dx in Island.dydx:
                    area += dfs(y_ + dy, x_ + dx)
                return area + 1
            else:
                # appending an empty neigh:
                neighs_.add((y_, x_))
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
                    island_ = Island(self._board, None, symb_ == self.BLACK)
                    # island updating:
                    island_.update(stones_, neighs_)
                    # island appending to the Islands list:
                    (self._black_islands if symb_ == self.BLACK else self._white_islands).append(island_)
                    # islands counter incrementation:
                    icounter += 1
        print(f'{icounter} new islands have been found and appending to the list...')

    def create_island(self, stone: tuple[int, int]) -> 'Island':
        """creates an island with player's stone at (y, x)"""
        island = Island(self._board, stone, self.black)
        island.append(self._black_islands, self._white_islands)
        return island

    def move(self, pos: str) -> None:
        """player makes a move"""
        stone = (y, x) = self.parse_pos(pos)
        print(f'Now {self.turn}s is moving... trying to locate a {self.turn} stone at {y, x} position!')
        if self.validate(y, x):
            # checks if the cell has already been occupied by this or the another player...
            if self._board[y][x] == self.stone:
                raise ValueError(f'the cell has already been occupied by yourself: {self.stone}')
            elif self._board[y][x] == self.EMPTY:
                # here we place a stone:
                allies, aliens = [], []
                for black_island in self._black_islands:
                    if stone in black_island.neighs:
                        (allies if self.black else aliens).append(black_island)
                for white_island in self._white_islands:
                    if stone in white_island.neighs:
                        (aliens if self.black else allies).append(white_island)
                for alien in aliens:
                    alien.neighs -= stone
                    if not alien.liberties():
                        # opponent stone-group's capturing:
                        alien.remove(self._black_islands, self._white_islands)
                        print(f'{Go.STONE_PAIRS[self.stone]} group of {alien.size} stones has just been captured!')
                if allies:
                    sum_ = reduce(lambda a, b: a + b, allies)
                    for ally in allies:
                        ally.remove(self._black_islands, self._white_islands)
                    sum_.append(self._black_islands, self._white_islands)
                    sum_.add_stone(stone, self._black_islands, self._white_islands)
                else:
                    print(f'a new Island has just been created')
                    island = self.create_island(stone)
                    if not island.liberties:
                        # self-capturing prohibition's violation:
                        raise ValueError(
                            f'self-capturing is strictly prohibited!.. violation detected at the cell: {y, x}')
            else:
                raise ValueError(f'the cell has already been occupied by your opponent: {Go.STONE_PAIRS[self.stone]}')
        else:
            raise ValueError(f'the position {y, x} is out of bounds')
        # turns counter's increasing:
        self._turn += 1

    def pass_turn(self):
        """current player passes his turn"""
        print(f'{self.turn}s pass their turn')
        self._turn += 1

    def check_ko_rule(self) -> bool:
        """checks the enforcement of the following KO rule:
        player cannot recreate the same board as the board after one of the previous moves"""
        print(f'ATTEMPT OF SUICIDE DETECTED for {self.turn}s!!! Rolling back to the save state...')
        # TODO: does this rule have the unlimited depth?
        if self._board in self._states:
            return False
        else:
            return True

    def reset(self):
        """Resets the board, clears all the stones from it and sets the turn to black"""
        self._board = [[Go.EMPTY for _ in range(self._width)] for _ in range(self._height)]
        self._turn = 0
        ...
        print(f'The board has been reset to default state...')

    def handicap_stones(self, q: int):
        """places some handicap stones in the correct order, works only for 9x9, 13x13 and 19x19 boards"""
        if not self._handicaps_used:
            if self._height == self._width and self._height in Go.HANDICAPS.keys():
                if 0 <= q <= (m := Go.HANDICAPS[self._height][0]):
                    ...
                else:
                    raise ValueError(
                        f'invalid handicap stones quantity, it must be larger than {0} and less or equal to {m}...')
            else:
                raise ValueError(f"invalid board size, board's height and width should be equal to 9, 13 or 19...")
        else:
            raise ValueError(f'handicap stones have been already used...')

    def rollback(self, turns_back: int):
        """rollbacks a set amount of turns on the go board"""
        if turns_back < 0 or turns_back > self._turn:
            raise ValueError(f'turns_back cannot be less than {0} or larger than the turns made: {self._turn}...')
        self._turn -= turns_back
        # rolling back the board state by 'turns_back' turns back:
        self._board = self._memo[self._turn]
        # core pars updating:
        ...


class Island:
    """represents a set of linked stones of the same colour on the Go-board"""
    dydx = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, board: list[list[str]], stone: tuple[int, int] = None, black: bool = True):
        # outer link:
        self._board = board  # <<-- the link to the Go game board from Go class...
        # True means black while False means white...
        self._player = black
        # core pars:
        self._stones: set[tuple[int, int]] = {stone} if stone else {}
        self._neighs: set[tuple[int, int]] = set()
        # initializing the first neighs:
        if stone:
            self.check_neighs(stone)

    @property
    def liberties(self):
        """gets the degree of liberty of the island"""
        return len(self._neighs)

    @property
    def captured(self):
        """checks if the island can be captured"""
        return self.liberties == 0

    @property
    def neighs(self):
        return self._neighs

    @property
    def size(self):
        return len(self._stones)

    def __add__(self, other: 'Island') -> 'Island':  # stone: tuple[int, int], islands: list['Island']):
        """appends the other Island to the self one"""
        if self._player != other._player:
            raise ValueError(f"cannot add two islands with different stones' colours!..\n"
                             f"self: {self._player} != {other._player}")
        else:
            # creating a new Island:
            sum_ = Island(self._board, None, self._player)
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
        """adds all the valid and empty neighbouring cells (horizontally and vertically only) to the Island's neighs set"""
        for dy, dx in Island.dydx:
            neigh_ = (y_ := stone[0] + dy, x_ := stone[1] + dx)
            if self.check_pos(y_, x_, ):
                if self._board[y_][x_] == Go.EMPTY:
                    self._neighs.add(neigh_)

    def add_stone(self, stone: tuple[int, int], black_islands: list['Island'], white_islands: list['Island']) -> None:
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
            self.remove(black_islands, white_islands)
        # finally we can alter the board:
        self._board[stone[0]][stone[1]] = Go.BLACK if self._player else Go.WHITE

    def remove(self, black_islands: list['Island'], white_islands: list['Island']):
        """removes the island from the islands list"""
        (black_islands if self._player else white_islands).remove(self)

    def append(self, black_islands: list['Island'], white_islands: list['Island']):
        """appends the island to the islands list"""
        (black_islands if self._player else white_islands).append(self)

    def update(self, stones: set[tuple[int, int]], neighs: set[tuple[int, int]]):
        if self._stones or self._neighs:
            raise ValueError(f'the island cannot be updated because it is not an empty one...'
                             f'it contains {self.size} stones and {self.liberties} neighs')
        self._stones = stones
        self._neighs = neighs


go = Go(9)
print(f'{go}')
# TODO: implement changing the global game sets like neighs and stones...
# TODO: when is the game over?
