# accepted on codewars.com
from abc import ABC, abstractmethod
from enum import Enum


def plants_and_zombies(lawn: list[str], zombies: list[list[int]]) -> int | None:  # LL 36 366 98 989
    # your code goes here. you can do it!
    grid = Grid(lawn, zombies)
    grid.start_game()
    return grid.result


class Grid:
    """main class for game board representation"""

    def __init__(self, lawn: list[str], zombies: list[list[int]]) -> None:
        # in pars:
        self._lawn = lawn
        self._zombies_spawn = dict()
        for zombie in zombies:
            if (k := zombie[0]) in self._zombies_spawn.keys():
                self._zombies_spawn[k].append((zombie[1], zombie[2]))
            else:
                self._zombies_spawn[k] = [(zombie[1], zombie[2])]
        print(f'zombies_spawn: {self._zombies_spawn}')
        # grid sizes:
        self._j_max, self._i_max = len(lawn), len(lawn[0])
        print(f'j_max, i_max: {self._j_max, self._i_max}')
        # the game grid:
        self._grid = None
        # current turn:
        self._turn = 0
        # living plants list:
        self._shooters = []
        self._super_shooters = []
        # existing zombies list:
        self._zombies = []
        # the final result of the game:
        self._result = None

    def is_valid(self, j, i):
        return 0 <= j < self._j_max and 0 <= i < self._i_max

    @property
    def result(self) -> int | None:
        return self._result

    @property
    def grid(self):
        return self._grid

    @property
    def j_max(self):
        return self._j_max

    @property
    def i_max(self):
        return self._i_max

    @property
    def zombies(self):
        return self._zombies

    @property
    def shooters(self):
        return self._shooters

    @property
    def super_shooters(self):
        return self._super_shooters

    def start_game(self) -> None:
        # initialization of a grid:
        self.initialize_grid()
        # showing the starting state:
        print()
        print(f'{self}')
        print()
        # the main game cycle:
        while self._turn <= max(self._zombies_spawn.keys()) or self.zombies:
            print(f'turn: {self._turn}')
            if self.make_turn():
                # defining the result:
                self._result = self._turn + 1
                break

    def initialize_grid(self) -> None:
        # grid initialization:
        self._grid = [[None for _ in range(self._i_max)] for _ in range(self._j_max)]
        # here we are initializing the plants on the grid:
        for i in range(self._i_max - 1, -1, -1):
            for j in range(self._j_max):
                ch = self._lawn[j][i]
                if ch == 'S':
                    self._grid[j][i] = SuperShooter(j, i)
                    self._super_shooters.append(self._grid[j][i])
                elif ch.isdigit():
                    d = int(ch)
                    self._grid[j][i] = Shooter(j, i, d)
                    self._shooters.append(self._grid[j][i])

    def make_turn(self) -> bool:
        # existing zombies movement:
        for zombie in self._zombies:
            if zombie.move(self):
                return True
        # new zombies initialization:
        print(f'\nnew zombies: ')
        if self._turn <= max(self._zombies_spawn.keys()):
            if self._turn in self._zombies_spawn.keys():
                for row, hp in self._zombies_spawn[self._turn]:
                    print(f'row, hp: {row, hp}')
                    self._grid[row][self._i_max - 1] = Zombie(row, self._i_max - 1, hp)
                    # adding zombies to the list:
                    self._zombies.append(self._grid[row][self._i_max - 1])
        print()
        print(f'{self}')
        print()
        # now the different kinds of plants are shooting:
        for shooter in self._shooters:  # <<-- at first all the common shooters shoot:
            shooter.shoot(self)
        for super_shooter in self._super_shooters:  # <<-- then the super shooters make their turn:
            super_shooter.shoot(self)
        # turns incrementer:
        self._turn += 1
        print()
        print(f'{self}')
        print()
        return False

    def __str__(self):
        return '\n'.join(
            [''.join([str(cell) if (cell := self._grid[j][i]) is not None else ' ' for i in range(self._i_max)]) for j
             in range(self._j_max)])

    def __repr__(self):
        return str(self)


class Direction(Enum):
    TOP_RIGHT = (1, 1)
    RIGHT = (0, 1)
    BOTTOM_RIGHT = (-1, 1)


class Plant(ABC):
    """abstract plant"""

    def __init__(self, j, i, d):
        self.j = j
        self.i = i
        self._damage = d

    @abstractmethod
    def shoot(self, grid: Grid):
        ...

    @staticmethod
    def inflict_damage(j: int, i: int, damage_remained: int, zombie: 'Zombie', grid: Grid):
        z_hp = zombie.hp - damage_remained
        if z_hp <= 0:
            grid.zombies.remove(zombie)
            grid.grid[j][i] = None
            return damage_remained - zombie.hp
        else:
            zombie.hp = z_hp
            return 0


class Shooter(Plant):
    """numbered shooter"""

    def __init__(self, j, i, d):
        super().__init__(j, i, d)

    def shoot(self, grid: Grid) -> None:
        damage_remained = self._damage
        for i_ in range(self.i + 1, grid.i_max):
            print(f'i_: {i_}, damage_remained: {damage_remained}')
            if isinstance((z := grid.grid[self.j][i_]), Zombie):
                if delta_d := self.inflict_damage(self.j, i_, damage_remained, z, grid):
                    print(f'LALA!!!')
                    damage_remained = delta_d
                else:
                    # the plant runs out of bullets:
                    break

    def __str__(self):
        return f'{self._damage}'

    def __repr__(self):
        return str(self)


class SuperShooter(Plant):
    """s-shooter"""

    def __init__(self, j, i):
        super().__init__(j, i, 1)

    def shoot(self, grid: Grid) -> None:
        for dir_ in Direction:
            dj, di = dir_.value
            j_, i_ = self.j, self.i
            while grid.is_valid(j_ + dj, i_ + di):
                print(f'dir_: {dir_}, damage: {self._damage}')
                j_ += dj
                i_ += di
                if isinstance((z := grid.grid[j_][i_]), Zombie):
                    self.inflict_damage(j_, i_, self._damage, z, grid)
                    # the plant runs out of bullets:
                    break

    def __str__(self):
        return f'S'

    def __repr__(self):
        return str(self)


class Zombie:
    """an enemy's class"""

    def __init__(self, j, i, hp):
        self._j = j
        self._i = i
        self._hp = hp

    @property
    def j(self):
        return self._j

    @property
    def i(self):
        return self._i

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp

    def move(self, grid: Grid) -> bool:
        # movement itself:
        grid.grid[self.j][self.i] = None
        self._i -= 1
        # if zombie touches a plant he destroys it:
        if isinstance((s := grid.grid[self._j][self._i]), Shooter):
            grid.shooters.remove(s)
        elif isinstance((ss := grid.grid[self._j][self._i]), SuperShooter):
            grid.super_shooters.remove(ss)
        # updating the grid:
        grid.grid[self._j][self._i] = self  # <<-- new position of zombie on the grid:
        # if zombie reaches the left border the game is lost:
        return True if self._i == 0 else False

    def __str__(self):
        return f'Z({self._hp})'

    def __repr__(self):
        return str(self)


lawn_ = [
    '2       ',
    '  S     ',
    '21  S   ',
    '13      ',
    '2 3     '
]

zombies_ = [  # [move num, row, hp]
    [0, 4, 28],
    [1, 1, 6],
    [2, 0, 10],
    [2, 4, 15],
    [3, 2, 16],
    [3, 3, 13]
]

lawn_x = [
    '11      ',
    ' 2S     ',
    '11S     ',
    '3       ',
    '13      '
]

zombies_x = [
    [0, 3, 16],
    [2, 2, 15],
    [2, 1, 16],
    [4, 4, 30],
    [4, 2, 12],
    [5, 0, 14],
    [7, 3, 16],
    [7, 0, 13]
]

lawn_z = [
    '1         ',
    'SS        ',
    'SSS       ',
    'SSS       ',
    'SS        ',
    '1         '
]

zombies_z = [
    [0, 2, 16],
    [1, 3, 19],
    [2, 0, 18],
    [4, 2, 21],
    [6, 3, 20],
    [7, 5, 17],
    [8, 1, 21],
    [8, 2, 11],
    [9, 0, 10],
    [11, 4, 23],
    [12, 1, 15],
    [13, 3, 22]
]

lawn_k = [
    '12        ',
    '3S        ',
    '2S        ',
    '1S        ',
    '2         ',
    '3         ']

zombies_k = [
    [0, 0, 18],
    [2, 3, 12],
    [2, 5, 25],
    [4, 2, 21],
    [6, 1, 35],
    [6, 4, 9],
    [8, 0, 22],
    [8, 1, 8],
    [8, 2, 17],
    [10, 3, 18],
    [11, 0, 15],
    [12, 4, 21]
]

lawn_l = [
    '12      ',
    '2S      ',
    '1S      ',
    '2S      ',
    '3       '
]

zombies_l = [
    [0, 0, 15],
    [1, 1, 18],
    [2, 2, 14],
    [3, 3, 15],
    [4, 4, 13],
    [5, 0, 12],
    [6, 1, 19],
    [7, 2, 11],
    [8, 3, 17],
    [9, 4, 18],
    [10, 0, 15],
    [11, 4, 14]
]

lawn_q = ['41SSS              ', '22   S             ', '2113S SS           ', '1S122S S           ',
          '4S S S             ', '4SSS               ', '4SSSS              ', 'S141  SS           ',
          '  S2 S             ', '61S S              ', '131S               ', '411SS              ',
          ' 4111S             ', '2SSSS              ', '1111               ', '121                ',
          '41                 ', ' 1S1S              ', ' 32S S             ', '21S                ',
          'S14  S S           ', '311  S S1          ', '1321 SS            ', '222 SS             ']

zombies_q = [[2, 0, 112], [2, 1, 70], [2, 2, 140], [2, 3, 126], [2, 4, 98], [2, 6, 112], [2, 8, 56], [2, 9, 126],
             [2, 11, 112], [2, 13, 84], [2, 14, 56], [2, 16, 70], [2, 17, 56], [2, 19, 56], [2, 20, 112], [2, 22, 126],
             [3, 7, 133], [3, 10, 88], [3, 12, 118], [3, 15, 59], [3, 23, 118], [5, 5, 108], [5, 21, 124], [8, 0, 59],
             [8, 1, 37], [8, 3, 66], [8, 4, 51], [8, 6, 59], [8, 8, 29], [8, 9, 66], [8, 11, 59], [8, 17, 29],
             [8, 18, 124], [8, 19, 29], [8, 20, 59], [8, 22, 66], [10, 5, 49], [10, 7, 68], [10, 10, 45], [10, 12, 60],
             [10, 13, 48], [10, 14, 32], [10, 15, 30], [10, 23, 60], [11, 16, 44], [11, 21, 62], [12, 2, 96],
             [14, 18, 53], [18, 1, 35], [18, 6, 56], [18, 11, 56], [18, 17, 28], [18, 19, 28], [18, 20, 56],
             [20, 0, 62], [20, 3, 71], [20, 4, 55], [20, 5, 49], [20, 7, 64], [20, 9, 71], [20, 10, 43], [20, 12, 57],
             [20, 13, 44], [20, 15, 28], [20, 22, 71], [20, 23, 57], [23, 8, 34], [23, 21, 57], [25, 2, 76],
             [25, 14, 35], [25, 16, 41], [27, 18, 50], [30, 1, 35], [30, 6, 56], [30, 11, 56], [30, 17, 28],
             [30, 19, 28], [30, 20, 56], [31, 0, 58], [31, 3, 65], [31, 5, 49], [31, 9, 65], [31, 10, 42], [31, 12, 56],
             [31, 13, 42], [31, 15, 28], [31, 22, 65], [31, 23, 56], [32, 4, 56], [32, 8, 30], [32, 21, 56],
             [34, 2, 72], [34, 7, 76], [34, 16, 37], [35, 14, 33], [36, 18, 54], [39, 17, 28], [40, 0, 56], [40, 1, 39],
             [40, 3, 63], [40, 9, 63], [40, 10, 42], [40, 11, 62], [40, 12, 56], [40, 13, 42], [40, 19, 31],
             [40, 20, 62], [40, 22, 63], [41, 8, 28], [41, 15, 31], [41, 21, 56], [41, 23, 62], [42, 2, 71],
             [42, 4, 56], [42, 5, 59], [42, 6, 74], [42, 16, 35], [43, 7, 74], [43, 14, 29], [47, 17, 28], [48, 3, 63],
             [48, 9, 63], [48, 13, 42], [48, 18, 66], [48, 19, 29], [48, 20, 58], [48, 22, 63], [49, 0, 62],
             [49, 1, 39], [49, 8, 28], [49, 10, 47], [49, 15, 29], [49, 21, 56], [49, 23, 58], [50, 6, 61],
             [50, 11, 70], [50, 12, 68], [51, 2, 77], [51, 5, 57], [51, 16, 39], [52, 4, 61], [52, 14, 31]]

print(f'res: {plants_and_zombies(lawn_q, zombies_q)}')
