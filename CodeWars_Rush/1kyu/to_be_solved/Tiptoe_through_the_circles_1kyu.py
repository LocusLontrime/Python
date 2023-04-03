import math
from typing import NamedTuple


class Point(NamedTuple):  # 36 366 98 989
    x: float
    y: float


class Circle(NamedTuple):
    ctr: Point
    r: float


# Returns length of the shortest route from a to b, avoiding the interiors of the circles in c
def shortest_path_length(a: Point, b: Point, c: list[Circle]) -> float:
    circles = set(c)
    graph = build_graph(a, b, list(circles))

    return 0


def intersect(p1: Point, p2: Point, circle: Circle):
    if p1 != p2:
        # constants for the straight line equation:
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = p1.y * p2.x - p2.y * p1.x
        # distance:
        if abs(a * circle.ctr.x + b * circle.ctr.y + c) / math.hypot(a, b) < circle.r:
            return True
        else:
            return False
    else:
        raise ValueError(f'p1 and p2 are the same!')


def get_reference_points(c1: Circle, c2: Circle) -> tuple[Point, Point, Point, Point]:
    # WitchDoctor's code:
    ...
    # Value error if c1 in c2 or c2 in c1...


def build_graph(a: Point, b: Point, circles: list[Circle]) -> dict[Circle, set[Circle]]:
    graph: dict[Circle, set[Circle]] = dict()
    # getting possible neighbours for all circles:
    for circle in circles:
        # busting of all possible neighs for current circle:
        for possible_neigh in circles:
            # neigh cannot be the same circle:
            if possible_neigh != circle:
                # busting all possible obstacles (intersections with other circles):
                for possible_obstacle in circles:
                    if possible_obstacle not in [possible_neigh, possible_obstacle]:
                        if ...:
                            ...
    a, b = b, a
    return ...

