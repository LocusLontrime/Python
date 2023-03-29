from abc import ABC, abstractmethod
from enum import Enum


def plants_and_zombies(lawn: list[str], zombies: list[list[int]]) -> int | None:   # LL 36 366 98 989
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
            if self._zombies_spawn.setdefault((k := zombie[0]), []):
                self._zombies_spawn[k].append(zombie[1], zombie[2])
        # grid sizes:
        self._j_max, self._i_max = len(lawn), len(lawn[0])
        # the game grid:
        self._grid = None
        # current turn:
        self._turn = 0
        # living plants list:
        self._plants = []
        # existing zombies list:
        self._zombies = []
        # flying bullets' dict:
        self._bullets = dict()
        # stop flag:
        self._flag = False
        # the final result of the game:
        self._result = None

    def is_valid(self, j, i):
        return 0 <= j < self._j_max and 0 <= i < self._i_max

    @property
    def bullets(self):
        return self._bullets

    @property
    def result(self) -> int | None:
        return self._result

    @property
    def grid(self):
        return self._grid

    def start_game(self) -> None:
        # initialization of a grid:
        self.initialize_grid()
        # the main game cycle:
        while not self._flag:
            self.make_turn()

    def initialize_grid(self) -> None:
        # grid initialization:
        self._grid = [[None for _ in range(self._i_max)] for _ in range(self._j_max)]
        # here we are initializing the plants on the grid:
        for j, row in enumerate(self._lawn):
            for i, ch in enumerate(row):
                if ch == 'S':
                    self._grid[j][i] = SuperShooter(j, i)
                elif ch.isdigit():
                    d = int(ch)
                    self._grid[j][i] = Shooter(j, i, d)

    def make_turn(self) -> None:
        # existing zombies movement:
        for zombie in self._zombies:
            zombie.move()
        # new zombies initialization:
        for row, hp in self._zombies_spawn[self._turn]:
            self._grid[row][self._i_max - 1] = Zombie(row, self._i_max - 1, hp)
        # now the plants are shooting:
        for plant in self._plants:
            # appends a list of new bullets to the general bullets list:
            plant.shoot(self._grid)
        # finally the bullets are moving:
        for key in self._bullets.keys():
            self._bullets[key].move(self)


class Direction(Enum):
    TOP_RIGHT = (1, 1)
    RIGHT = (0, 1)
    BOTTOM_RIGHT = (-1, 1)


class Bullet:
    """a usual bullet that plants can use in order to eliminate the approaching zombies waves"""

    def __init__(self, j: int, i: int, d: int, dir_: Direction):
        # coords:
        self.j = j
        self.i = i
        # damage:
        self.damage = d
        # direction:
        self._direction = dir_

    def move(self, grid: Grid):
        dj, di = self._direction.value
        j_, i_ = self.j + dj, self.i + di
        if grid.is_valid(j_, i_):
            # updating the bullet:
            self.update(j_, i_, grid)
            if isinstance((z := grid.grid[self.j][self.i]), Zombie):
                self.inflict_damage(z, grid)
        else:
            # the bullet is out of grid range -->> it is removed from dict:
            self.delete(grid)

    def update(self, j_: int, i_: int, grid: Grid):
        self.delete(grid)
        if grid.bullets.setdefault((j_, i_), []):
            grid.bullets[(j_, i_)].append(self)
        self.j, self.i = j_, i_

    def delete(self, grid: Grid):
        grid.bullets[self.j, self.i].remove(self)

    def inflict_damage(self, zombie: 'Zombie', grid: Grid):
        zombie.hp -= self.damage
        if zombie.hp <= 0:
            # zombie's eliminating:
            grid.grid[zombie.j][zombie.i] = None


class Plant(ABC):
    """abstract plant"""

    def __init__(self, j, i):
        self.j = j
        self.i = i

    @abstractmethod
    def shoot(self, grid: Grid):
        ...


class Shooter(Plant):
    """numbered shooter"""

    def __init__(self, j, i, d):
        super().__init__(j, i)
        self._damage = d

    def shoot(self, grid: Grid) -> None:
        if grid.grid.bullets.setdefault((self.j, self.i), []):
            grid.grid.bullets[self.j, self.i] = Bullet(self.j, self.i, self._damage, Direction.RIGHT)


class SuperShooter(Plant):
    """s-shooter"""

    def __init__(self, j, i):
        super().__init__(j, i)

    def shoot(self, grid: Grid) -> None:
        for dir_ in Direction:
            if grid.grid.bullets.setdefault((self.j, self.i), []):
                grid.grid.bullets[self.j, self.i] = Bullet(self.j, self.i, 1, dir_)


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

    def move(self):
        # movement itself:
        self._i -= 1
        # if zombies bumps into a bullet:
        ...
        # if zombie touches a plant he destroys it:
        ...
        # if zombie reaches the left border the game is lost:
        if self._i == 0:
            ...


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