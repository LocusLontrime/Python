from typing import NamedTuple


class Point(NamedTuple):  # 36 366 98 989
    x: float
    y: float


class Circle(NamedTuple):
    ctr: Point
    r: float


# Returns length of the shortest route from a to b, avoiding the interiors of the circles in c
def shortest_path_length(a: Point, b: Point, c: list[Circle]) -> float:

    return 0

