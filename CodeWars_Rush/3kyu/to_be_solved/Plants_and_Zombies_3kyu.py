from abc import ABC


def plants_and_zombies(lawn, zombies):
    # your code goes here. you can do it!
    ...


class Grid:
    """main class for game board representation"""
    def __init__(self, lawn, zombies):
        self._lawn = lawn
        self._zombies = zombies
        self._grid = None

    def initialize_grid(self):
        ...

    def make_turn(self):
        ...

    ...


class Cell:
    """needed for representing a cell of a grid"""
    ...


class Plant(ABC):
    """abstract plant"""
    ...


class Shooter(Plant):
    """numbered shooter"""
    ...


class SuperShooter(Plant):
    """s-shooter"""
    ...


class Zombie:
    """an enemy's class"""
    ...


class Bullet:
    """a usual bullet that plants can use in order to eliminate the approaching zombies waves"""
    ...



