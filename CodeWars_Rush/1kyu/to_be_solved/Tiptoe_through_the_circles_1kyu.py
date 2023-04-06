import math
from typing import NamedTuple
import heapq as hq

import numpy as np


adjacency_matrix = None


class Point(NamedTuple):  # 36 366 98 989
    x: float
    y: float


class Circle(NamedTuple):
    ctr: Point
    r: float


# Returns length of the shortest route from a to b, avoiding the interiors of the circles in c
def shortest_path_length(a: Point, b: Point, c: list[Circle]) -> float | None:
    # adjacency matrix initialization:
    adjacency_matrix: dict[tuple[Vertex, Vertex], float] = dict()  # <<-- memoization for edges lengths
    # if start or end point lies in at least one of the circles given:
    if not validate(a, b, c):
        return None
    # removing the repeating circles from the list:
    circles = set(c)
    start_vertex, end_vertex = ..., ...
    # here we build a graph representing the circles-obstacles for further pathfinding:
    graph = build_graph(a, b, list(circles))
    # pathfinding using Dijkstra algorithm:
    vertexes_to_be_visited = [start_vertex]  # <<-- starting point...
    hq.heapify(vertexes_to_be_visited)
    # the core of Dijkstra algo:
    while vertexes_to_be_visited:
        # current vertex
        vertex_ = hq.heappop(vertexes_to_be_visited)
        if vertex_ == end_vertex:
            break
        for neigh in vertex_.neighs:
            if neigh.g > vertex_.g + neigh.edge(vertex_):
                neigh.g = vertex_.g + neigh.edge(vertex_)
                hq.heappush(vertexes_to_be_visited, neigh)
    # path restoration:
    # start point of path restoration (here we begin from the end node of the shortest path found):
    vertex = end_vertex
    shortest_path = []
    # path restoring (here we get the reversed path):
    while vertex.previously_visited_vertex:
        shortest_path.append(vertex)
        vertex = vertex.previously_visited_node
    shortest_path.append(start_vertex)
    # returns the result:
    return shortest_path


def intersect(p1: Point, p2: Point, circle: Circle) -> bool:
    """checks the intersection of the segment and the circle"""
    if coeffs := get_coeffs(p1, p2):
        # constants for the straight line equation:
        a, b, c = coeffs
        # if some end segment points lies into the circle:
        if in_(p1, circle) or in_(p2, circle):
            return True
        # distance:
        if abs(a * circle.ctr.x + b * circle.ctr.y + c) / math.hypot(a, b) < circle.r:
            # checks if the point of the projection of the center of the circle on straight line p1p2 lies into the segment p1p2:
            a_, b_ = b, -a  # <<-- orthogonal straight line to p1p2, let it be named as "orto"
            ...
            # circle's center belongs to orto straight line, consequently:
            c_ = a * circle.ctr.y - b * circle.ctr.x
            # aux par:
            h = a ** 2 + b ** 2
            # now let us define the coordinates of projection point:
            x_, y_ = (-b * c_ - a * c) / h, (a * c_ - b * c) / h
            p_ = Point(x_, y_)
            # the above condition itself:
            if distance(p_, p1) + distance(p_, p2) == distance(p1, p2):
                return True
    else:
        raise ValueError(f'p1: {p1} and p2: {p2} are the same, method: {intersect}!')
    return False


def distance(p1: Point, p2: Point):
    # euclidian distance:
    return math.hypot(p2.y - p1.y, p2.x - p1.x)


def circle_intersect(circle1: Circle, circle2: Circle) -> bool:
    return circle1.r + circle2.r > math.hypot(circle2.ctr.y - circle1.ctr.y, circle2.ctr.x - circle1.ctr.x)


def get_valid_edges(c1: Circle | Point, c2: Circle, circles: list[Circle]) -> list[tuple['Vertex', 'Vertex']]:
    """defines all valid edges for 2 circles as list of tuples: (2 linked Vertices)"""
    # WitchDoctor's code (uses intersect()...):

    # check for obstacles (one for)...

    # Value error if c1 in c2 or c2 in c1...
    if isinstance(c1, Circle):
        # obstacles check:
        for circle in circles:
            if circle not in [c1, c2]:
                # let c1 be the larger circle:
                c1_, c2_ = (c1, c2) if c1.r > c2.r else (c2, c1)
                # getting all 4 or 2 pair of points:
                # 1. 2 outer tangent edges:
                angle_c1c2_ox = ...
                if not circle_intersect(c1, c2):
                    # 2. 2 crossing edges
                    ...


                # if intersect(...)


def build_graph(a: Point, b: Point, circles: list[Circle]) -> list['Vertex']:

    # getting possible neighbours for all circles:
    for circle in circles:
        # initializing neighs for all the vertexes:
        # busting of all possible neighs for current circle:
        for possible_neigh in circles:
            # neigh cannot be the same circle:
            if possible_neigh != circle:
                # busting all possible obstacles (intersections with other circles):
                for possible_obstacle in circles:
                    if possible_obstacle not in [circle, possible_neigh]:
                        # TODO: angle check: angle_to >= angle_from!!!
                        if ...:
                            break
                else:
                    continue

    return ...


def in_(obj: Point | Circle, circle: Circle):
    if isinstance(obj, Point):
        res = math.hypot(circle.ctr.y - obj.y, circle.ctr.x - obj.x) < circle.r
    elif isinstance(obj, Circle):
        res = math.hypot(circle.ctr.y - obj.ctr.y, circle.ctr.x - obj.ctr.x) < circle.r - obj.r
    else:
        raise ValueError(f'method {in_} works only for Point or Circle as obj and Circle as circle...')
    return res


def validate(a: Point, b: Point, circles: list[Circle]) -> bool:
    for circle in circles:
        if in_(a, circle):
            print(f'Point {a} lies in circle {circle}')
            return False
        elif in_(b, circle):
            print(f'Point {b} lies in circle {circle}')
            return False
    return True


def get_coeffs(p1: Point, p2: Point) -> tuple[float, float, float] | None:
    if p1 != p2:
        # constants for the straight line equation:
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = p1.y * p2.x - p2.y * p1.x
        return a, b, c
    print(f'method: {get_coeffs}, p1: {p1} = p2: {p2}')
    return None


def arc(a1: float, a2: float, circle: Circle) -> float:
    """calculates the length of the arc from angle a1 to a2 for the circle given"""
    return abs(a2 - a1) * circle.r


def scalar_product(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


def angle_of_intersection(outer_obj: Circle | Point, circle: Circle):
    _a, _b = 0, 1  # abscissa axis
    if isinstance(outer_obj, Circle):
        a_, b_, _ = get_coeffs(outer_obj.ctr, circle.ctr)
    elif isinstance(outer_obj, Point):
        a_, b_, _ = get_coeffs(outer_obj, circle.ctr)
    else:
        raise ValueError(f'method {angle_of_intersection} works only for Point or Circle as outer_obj and Circle as circle...')
    sc = scalar_product(_a, _b, a_, b_)
    # lengths of v1 and v2:
    l1, l2 = math.hypot(_a, _b), math.hypot(a_, b_)
    # angle:
    angle = math.acos(sc / (l1 * l2))
    # result:
    return angle if a_ >= 0 and b_ >= 0 else 2 * math.pi - angle


class Vertex:
    """Vertex cannot be just a circle, it is a point on the border of the circle
    with some concrete value of the angle with abscissa axis..."""
    def __init__(self, circle: Circle, angle: float):
        # basic attrs:
        self.circle = circle
        self.angle = angle
        # algo logic pars:
        self.g = np.Infinity  # aggregated cost of moving from start to the current Node,
        # Infinity chosen for convenience and algorithm's logic
        self.previously_visited_vertex = None  # -->> for building the shortest path of Nodes from the starting point to the ending one
        # neighs:
        self.neighs: set[Vertex] = set()

    @property
    def xy(self):
        return self.circle.ctr.x + self.circle.r * math.cos(self.angle), self.circle.ctr.y + self.circle.r * math.sin(self.angle)

    def edge(self, other: 'Vertex'):
        if self.circle == other.circle:
            res = arc(self.angle, other.angle, self.circle)
        else:
            (x1, y1), (x2, y2) = self.xy, other.xy
            res = math.hypot(x2 - x1, y2 - y1)
        return res

    def get_neighs(self, vertexes: list['Vertex']):
        ...

    def __eq__(self, other):
        return self.circle, self.angle == other.circle, other.angle

    def __ne__(self, other):
        return self.circle, self.angle != other.circle, other.angle

    def __lt__(self, other):
        # necessary for priority queue:
        return self.g < other.g

    def __str__(self):
        return f'({self.circle}, {self.angle})[{self.g}]'

    def __repr__(self):
        return str(self)

