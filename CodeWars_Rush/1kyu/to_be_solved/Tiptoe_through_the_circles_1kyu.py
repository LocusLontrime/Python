import functools
import math
import time
from enum import Enum
from typing import NamedTuple
import heapq as hq
import numpy as np
from collections import defaultdict

ERR = 10 ** -8
NO_PATH = -1.0

building_graph_time_ms: int
building_circle_links_time_ms: int
validating_edges_time_ms: int
getting_valid_edges_time_ms: int
merry_counter: int
validating_edge_counter: int
getting_valid_edge_counter: int
inner_counter: int


class Point(NamedTuple):  # 36 366 98 989
    x: float
    y: float


class Circle(NamedTuple):
    ctr: Point
    r: float


# Returns length of the shortest route from a to b, avoiding the interiors of the circles in c
def shortest_path_length(a: Point, b: Point, c: list[Circle]) -> float:
    global building_graph_time_ms, validating_edge_counter, getting_valid_edge_counter,\
        inner_counter, validating_edges_time_ms, getting_valid_edges_time_ms
    validating_edge_counter = 0
    getting_valid_edge_counter = 0
    inner_counter = 0
    validating_edges_time_ms = 0
    getting_valid_edges_time_ms = 0
    # if start or end point lies in at least one of the circles given:
    if not validate_ab(a, b, c):
        print(f'a or b point is locked')
        return NO_PATH
    print(f'validated...')
    # removing the repeating circles from the list:
    circles = set(c)
    print(f'doubles removed...')
    # if some circles lie in some others:
    circles = [c for c in circles if all([not _in(c, c_) for c_ in circles - {c}])]
    print(f'inner circles deleted...')
    # here we build a graph representing the circles-obstacles for further pathfinding,
    # v_hashes needed in order not to create new Vertexes if they have already been built:
    building_graph_start = time.time_ns()
    v_hashes = build_graph(a, b, list(circles))
    building_graph_time_ms = (time.time_ns() - building_graph_start) // 10 ** 6
    print(f'v_hashes: ')
    for i, (k, v) in enumerate(v_hashes.items()):
        print(f'{i}. hash: {k}, vertex: {v}')
    if (start_hash := hash(Vertex(Circle(a, 0), 0))) not in v_hashes.keys() or (
            end_hash := hash(Vertex(Circle(b, 0), 0))) not in v_hashes.keys():
        return NO_PATH
    start_vertex, end_vertex = v_hashes[start_hash], v_hashes[end_hash]  # weird !!!
    print(f'start_vertex, end_vertex: {start_vertex, end_vertex}')
    print(f"start_vertex's neighs: {start_vertex.neighs}")
    print(f"end_vertex's neighs: {end_vertex.neighs}")
    # pathfinding using Dijkstra algorithm:
    vertexes_to_be_visited = [start_vertex]  # <<-- starting point...
    start_vertex.g = 0  # here we are situated at the very beginning of the path!
    hq.heapify(vertexes_to_be_visited)  # -->> priority heap will be convenient for us.
    # the core of Dijkstra algo:
    counter = 0
    while vertexes_to_be_visited:
        # current vertex
        vertex_ = hq.heappop(vertexes_to_be_visited)
        print(f'{counter}. current vertex: {vertex_}')
        if vertex_ == end_vertex:
            # the shortest path been found:
            break
        neighs = vertex_.neighs
        # print(f'neighs: {neighs}')
        for neigh in neighs:
            # avoiding circulating through the vertices that belong to the same circle:
            if neigh.circle != vertex_.circle or (
                    neigh.circle == vertex_.circle and vertex_.previously_visited_vertex.circle != vertex_.circle):
                # just a dp condition:
                if neigh.g > vertex_.g + neigh.edge(vertex_):
                    neigh.g = vertex_.g + neigh.edge(vertex_)
                    # path memoization:
                    neigh.previously_visited_vertex = vertex_
                    hq.heappush(vertexes_to_be_visited, neigh)
        counter += 1
    # path restoration:
    # the start point of path restoration process (here we begin from the end node of the shortest path found):
    vertex = end_vertex
    shortest_path = []
    # path restoring (here we get the reversed path):
    while vertex.previously_visited_vertex:
        shortest_path.append(vertex)
        vertex = vertex.previously_visited_vertex
    shortest_path.append(start_vertex)
    # shortest path visualizing:
    print(f'SHORTEST PATH VISUALIZATION: ')
    for i, vertex in enumerate(reversed(shortest_path)):
        print(f'{i}. {vertex}')
    # check end_vertex.g:
    if end_vertex.g == np.Infinity:
        # there is no path!
        print(f'THERE IS NO PATH!!!')
        return NO_PATH
    # returns the result:
    return end_vertex.g if end_vertex.g != np.Infinity else None


def intersect(p1: Point, p2: Point, circle: Circle) -> bool:
    """checks the intersection of the segment and the circle"""
    if p1 != p2:
        # if some end segment points lies into the circle:
        if in_(p1, circle) or in_(p2, circle):
            return True
        # constants for the straight line equation:
        a, b, c = get_coeffs(p1, p2)
        # print(f'a, b, c: {a, b, c}')
        # distance from the circle's center to the straight line containing the segment:
        if abs(a * circle.ctr.x + b * circle.ctr.y + c) / math.hypot(a, b) < circle.r:
            # checks if the point of the projection of the center of the circle on straight line p1p2 lies into the segment p1p2...
            # orthogonal straight line to p1p2, let it be named as "orto",
            # circle's center belongs to the orto straight line, consequently:
            c_ = a * circle.ctr.y - b * circle.ctr.x
            # aux par:
            h = a ** 2 + b ** 2
            # now let us define the coordinates of projection point:
            x_, y_ = (-b * c_ - a * c) / h, (a * c_ - b * c) / h
            p_ = Point(x_, y_)
            # the above condition itself:
            d1, d2, d = distance(p_, p1), distance(p_, p2), distance(p1, p2)
            if d1 + d2 - d < ERR:
                return True
    else:
        raise ValueError(f'p1: {p1} and p2: {p2} cannot be the same, method: {intersect}!')
    return False


def distance(p1: Point | Circle, p2: Point | Circle):
    """calculates an euclidian distance between 2 points: p1 and p2 or between 2 circles"""
    # euclidian distance:
    if isinstance(p1, Point) and isinstance(p2, Point):
        res = math.hypot(p2.y - p1.y, p2.x - p1.x)
    elif isinstance(p1, Circle) and isinstance(p2, Circle):
        res = math.hypot(p2.ctr.y - p1.ctr.y, p2.ctr.x - p1.ctr.x)
    else:
        raise ValueError(f'method {distance} works only for Point, Point or Circle, Circle as p1, p2...')
    return res


def circle_intersect(circle1: Circle, circle2: Circle) -> bool:
    """checks if two circles have non-zero area of intersection"""
    return circle1.r + circle2.r > math.hypot(circle2.ctr.y - circle1.ctr.y, circle2.ctr.x - circle1.ctr.x)


def get_valid_edges(c1_: Circle, c2_: Circle, circles: list[Circle]) -> list[tuple['Vertex', 'Vertex']]:
    """defines all valid edges for 2 circles as list of tuples: (2 linked Vertices)"""
    global getting_valid_edge_counter, validating_edges_time_ms
    getting_valid_edge_counter += 1
    # possible linked vertices:
    poss_vertices = []
    # Value error if c1 in c2 or c2 in c1...
    if c1_.r != 0 or c2_.r != 0:
        # let c1 be the larger circle:
        c1, c2 = (c1_, c2_) if c1_.r > c2_.r else (c2_, c1_)
        # getting all 4 or 2 pair of points:
        # 1. 2 outer tangent edges:
        c1c2_len = distance(c1, c2)
        angle_c1c2_ox = angle_of_intersection(c2, c1)
        angle_c2c1_ox = (math.pi + angle_c1c2_ox) % (2 * math.pi)
        _inner_angle = math.acos((c1.r - c2.r) / c1c2_len)
        _angle1 = _angle2 = (angle_c1c2_ox + _inner_angle) % (2 * math.pi)
        angle1_ = angle2_ = (angle_c1c2_ox - _inner_angle) % (2 * math.pi)
        poss_vertices.append((Vertex(c1, _angle1), Vertex(c2, (_angle2 if c2.r != 0 else 0))))
        poss_vertices.append((Vertex(c1, angle1_), Vertex(c2, (angle2_ if c2.r != 0 else 0))))
        if not circle_intersect(c1, c2) and 0 not in [c1.r, c2.r]:
            inner_angle_ = math.acos((c1.r + c2.r) / c1c2_len)
            # 2. 2 crossing edges
            _angle1, _angle2 = (angle_c1c2_ox + inner_angle_) % (2 * math.pi), (
                    angle_c2c1_ox + inner_angle_) % (2 * math.pi)
            angle1_, angle2_ = (2 * math.pi + angle_c1c2_ox - inner_angle_) % (2 * math.pi), (
                    2 * math.pi + angle_c2c1_ox - inner_angle_) % (2 * math.pi)
            poss_vertices.append((Vertex(c1, _angle1), Vertex(c2, _angle2)))
            poss_vertices.append((Vertex(c1, angle1_), Vertex(c2, angle2_)))
    else:
        # 0. if c1 - Point, c2 - Point or c1 and c2 - point:
        poss_vertices.append((Vertex(c1_, 0), Vertex(c2_, 0)))
    # obstacles check:
    validating_edges_start = time.time_ns()
    vertices = [(v1, v2) for v1, v2 in poss_vertices if v1.validate_edge(v2, circles)]
    validating_edges_time_ms += (time.time_ns() - validating_edges_start) // 10 ** 6
    # returns res:
    return vertices


def build_edges_circle(vertices: list['Vertex'], separators: list[float]):
    # builds all the links for all the vertices that belong to the same circle:
    # TODO: optimization!..
    # print(f'building edges for a circle...')
    # print(f'there are {len(vertices)} different vertices located on the circle...')
    links_counter = 0
    if vertices:
        len_ = len(vertices)
        for j in range(len_):
            if vertices[j].circle.r:
                for i in range(j + 1, len_):
                    if vertices[j].rot_dir != vertices[i].rot_dir:
                        min_angle_v, max_angle_v = sorted([vertices[j], vertices[i]], key=lambda x: x.angle)
                        flag = True
                        for obstacle in separators:
                            if min_angle_v.rot_dir == RotDir.ANTI_CLOCKWISE:
                                # anti-clockwise:
                                if min_angle_v.angle <= obstacle <= max_angle_v.angle:
                                    # print(f'AN OBSTACLE ARISEN!!!')
                                    flag = False
                                    break
                            else:
                                # clockwise:
                                if 0 <= obstacle <= min_angle_v.angle or max_angle_v.angle <= obstacle <= 2 * math.pi:
                                    # print(f'AN OBSTACLE ARISEN!!!')
                                    flag = False
                                    break
                        if flag:
                            # print(f'CONNECTING {min_angle_v} and {max_angle_v} vertices!!!')
                            links_counter += 1
                            vertices[j].connect(vertices[i])
                            vertices[i].connect(vertices[j])
    # print(f'{links_counter} new link-pairs built!')


def build_graph(a: Point, b: Point, circles: list[Circle]) -> dict:
    """builds graph: creates vertices and edges between them"""
    # appending a and b points to the list of circles as A and B circles:
    global building_circle_links_time_ms, merry_counter, getting_valid_edges_time_ms
    merry_counter = 0
    A, B = Circle(a, 0), Circle(b, 0)
    circles_ = circles + [A, B]
    v_hashes = dict()
    # TODO: If a or b point belongs to some edge?..
    # getting possible neighbours for all circles:
    len_ = len(circles_)
    # aux dicts of vertices and separators for all the circles:
    circle_vertices: dict[Circle, list['Vertex']] = dict()
    separators: dict[Circle, list[float]] = dict()
    for j in range(len_):
        # print(f'cj: {circles_[j]}')
        # initializing neighs for all the vertexes:
        # busting of all possible neighs for current circle:
        for i in range(j + 1, len_):
            # print(f'ci: {circles_[i]}')
            if circle_intersect(circles_[j], circles_[i]):
                if (c1 := circles_[j]) in separators.keys():
                    separators[c1].append(angle_of_intersection(circles_[i], circles_[j]))
                else:
                    separators[c1] = [angle_of_intersection(circles_[i], circles_[j])]
                if (c2 := circles_[i]) in separators.keys():
                    separators[c2].append(angle_of_intersection(circles_[j], circles_[i]))
                else:
                    separators[c2] = [angle_of_intersection(circles_[j], circles_[i])]
            getting_valid_edges_start = time.time_ns()
            valid_edges = get_valid_edges(circles_[j], circles_[i], circles_)
            getting_valid_edges_time_ms += (time.time_ns() - getting_valid_edges_start) // 10 ** 6
            for v1, v2 in valid_edges:
                merry_counter += 1
                # print(f'v1, v2: {v1, v2}')
                v1_hash, v2_hash = hash(v1), hash(v2)
                # extracting vertices from the memory:
                if v1_hash in v_hashes.keys():
                    v1 = v_hashes[v1_hash]
                else:
                    v_hashes[v1_hash] = v1
                if v2_hash in v_hashes.keys():
                    v2 = v_hashes[v2_hash]
                else:
                    v_hashes[v2_hash] = v2
                # building link:
                v1.connect(v2)
                v2.connect(v1)
                v1.get_rot_dir(v2)
                v2.get_rot_dir(v1)
                # building vertices[circle] dict:
                if (c1 := v1.circle) in circle_vertices.keys():
                    circle_vertices[c1].append(v1)
                else:
                    circle_vertices[c1] = [v1]
                if (c2 := v2.circle) in circle_vertices.keys():
                    circle_vertices[c2].append(v2)
                else:
                    circle_vertices[c2] = [v2]
    # getting all circle connections:
    # print(f'BUILDING CIRCLE LINKS: ')
    building_circle_links_start = time.time_ns()
    for c in circles_:
        verts, seps = circle_vertices[c] if c in circle_vertices.keys() else [], separators[
            c] if c in separators.keys() else []
        # print(f'verts: {verts}')
        # print(f'seps: {[angle * 180 / math.pi for angle in seps]}')
        build_edges_circle(verts, seps)
    building_circle_links_time_ms = (time.time_ns() - building_circle_links_start) // 10 ** 6
    return v_hashes


def in_(obj: Point, circle: Circle) -> bool:
    """checks if the point lies in the circle ( 'circle' )"""
    return math.hypot(circle.ctr.y - obj.y, circle.ctr.x - obj.x) < circle.r


def _in(c1: Circle, c2: Circle):
    """checks if the circle: c1 lies in the circle: c2"""
    return math.hypot(c2.ctr.y - c1.ctr.y, c2.ctr.x - c1.ctr.x) < c2.r - c1.r


def validate_ab(a: Point, b: Point, circles: list[Circle]) -> bool:
    """checks if a or b point lies in some circle from the list"""
    for circle in circles:
        if in_(a, circle):
            # print(f'Point {a} lies in circle {circle}')
            return False
        elif in_(b, circle):
            # print(f'Point {b} lies in circle {circle}')
            return False
    return True


@functools.lru_cache
def get_coeffs(p1: Point, p2: Point) -> tuple[float, float, float]:
    """defines the coefficients a, b, c for the straight line describing by the equation: ax + by + c = 0
    and passing through 2 different points: p1 and p2"""
    if p1 != p2:
        # constants for the straight line equation:
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = p1.y * p2.x - p2.y * p1.x
        return a, b, c
    else:
        raise ValueError(f'method: {get_coeffs}, p1: {p1} = p2: {p2}')


def arc(a1: float, a2: float, circle: Circle, flag: bool = True) -> float:
    """calculates the length of the arc from angle a1 to a2 for the circle given"""
    da = abs(a2 - a1)
    return da * circle.r if flag else (2 * math.pi - da) * circle.r


def scalar_product(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


def cross_product_val(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1


def angle_of_intersection(outer_obj: Circle | Point, circle: Circle):
    # TODO: check!
    _x, _y = 0, 1  # abscissa axis
    if isinstance(outer_obj, Circle):
        x_, y_ = outer_obj.ctr.x - circle.ctr.x, outer_obj.ctr.y - circle.ctr.y
    elif isinstance(outer_obj, Point):
        x_, y_ = outer_obj.x - circle.ctr.x, outer_obj.y - circle.ctr.y
    else:
        raise ValueError(
            f'method {angle_of_intersection} works only for Point or Circle as outer_obj and Circle as circle...')
    sc = scalar_product(_x, _y, y_, x_)
    # lengths of v1 and v2:
    l1, l2 = math.hypot(y_, x_), math.hypot(_x, _y)
    # angle:
    angle = math.acos(sc / (l1 * l2))
    # result:
    return angle if y_ >= 0 else 2 * math.pi - angle


class Vertex:
    """Vertex cannot be just a circle, it is a point on the border of the circle
    with some concrete value of the angle with abscissa axis..."""

    def __init__(self, circle: Circle, angle: float):
        # basic attrs:
        self.circle = circle
        self.angle = angle
        self._rot_dir = None
        self.x, self.y = self.circle.ctr.x + self.circle.r * math.cos(
            self.angle), self.circle.ctr.y + self.circle.r * math.sin(self.angle)
        # algo logic pars:
        self.g = np.Infinity  # aggregated cost of moving from start to the current Node,
        # Infinity chosen for convenience and algorithm's logic
        self.previously_visited_vertex = None  # -->> for building the shortest path of Nodes from the starting point to the ending one
        # neighs:
        self.neighs: set[Vertex] = set()

    @property
    def rot_dir(self):
        return self._rot_dir

    def edge(self, other: 'Vertex'):
        if self.circle == other.circle:
            # TODO: FIX!!!
            v1, v2 = sorted([self, other], key=lambda x: x.angle)
            res = arc(self.angle, other.angle, self.circle, v1.rot_dir == RotDir.ANTI_CLOCKWISE)
        else:
            x1, y1, x2, y2 = self.x, self.y, other.x, other.y
            res = math.hypot(x2 - x1, y2 - y1)
        return res

    def connect(self, other: 'Vertex'):
        """add only one oriented link: self -->> other!!!"""
        if self != other:
            if other not in self.neighs:
                # print(f'appending neighbouring vertex: {other} for the vertex: {self}')
                self.neighs.add(other)

    def get_rot_dir(self, twin: 'Vertex'):
        l_vector = twin.x - self.x, twin.y - self.y
        r_vector = self.x - self.circle.ctr.x, self.y - self.circle.ctr.y
        self._rot_dir = RotDir.CLOCKWISE if cross_product_val(*l_vector, *r_vector) < 0 else RotDir.ANTI_CLOCKWISE

    def validate_edge(self, other: 'Vertex', circles: list[Circle]):
        global validating_edge_counter, inner_counter
        validating_edge_counter += 1
        # print(f'validating an edge: {self} --> {other}')
        # print(f'circles: {circles}')
        if self != other:
            for circle in circles:
                inner_counter += 1
                if circle not in {self.circle, other.circle}:
                    if intersect(Point(self.x, self.y), Point(other.x, other.y), circle):
                        # print(f'NON-VALID')
                        return False
            # print(f'VALID')
            return True
        else:
            raise ValueError(f'method {self.validate_edge} works only for 2 different vertices...')

    def __eq__(self, other):
        return (self.circle, self.angle) == (other.circle, other.angle)

    def __ne__(self, other):
        return (self.circle, self.angle) != (other.circle, other.angle)

    def __lt__(self, other):
        # necessary for priority queue:
        return self.g < other.g

    def __str__(self):
        return f'({self.circle}, {self.angle * 180 / math.pi}, {self.rot_dir})[{self.g}]'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.circle, self.angle))


class RotDir(Enum):
    CLOCKWISE = 0
    ANTI_CLOCKWISE = 1


# tests:
# a__, b__ = Point(-3, 1), Point(4.25, 0)
# c__ = [Circle(Point(0, 0), 2.5), Circle(Point(1.5, 2), 0.5), Circle(Point(3.5, 1), 1), Circle(Point(3.5, -1.7), 1.2)]

# a__, b__ = Point(0, 1), Point(0, -1)
# c__ = [Circle(Point(0, 0), 0.8), Circle(Point(3.8, 0), 3.2), Circle(Point(-3.5, 0), 3), Circle(Point(-7, 0), 1)]

# a__, b__ = Point(3, 0), Point(0, 4)
# c__ = [Circle(Point(0, 0), 1)]

# a__, b__ = Point(0, 0), Point(20, 20)
# c__ = [Circle(Point(4, 0), 3), Circle(Point(-4, 0), 3), Circle(Point(0, 4), 3), Circle(Point(0, -4), 3)]

# a__, b__ = Point(0, 1), Point(0, -1)
# c__ = [Circle(Point(0, 0), 0.8), Circle(Point(-3.8, 0), 3.2), Circle(Point(3.5, 0), 3.5), Circle(Point(7, 0), 1)]

# a__, b__ = Point(0, -7), Point(8, 8)
# c__ = []

# a__, b__ = Point(-3.5, 0.1), Point(3.5, 0.0)
# r = 2.01
# c__ = [Circle(Point(0, 0), 1), Circle(Point(r, 0), 1), Circle(Point(r * 0.5, r * math.sqrt(3) / 2), 1),
#        Circle(Point(-r * 0.5, r * math.sqrt(3) / 2), 1),
#        Circle(Point(-r, 0), 1), Circle(Point(r * 0.5, -r * math.sqrt(3) / 2), 1),
#        Circle(Point(-r * 0.5, -r * math.sqrt(3) / 2), 1)]

# a__, b__ = Point(0.5, 0.5), Point(2, 2)
# c__ = [Circle(Point(0, 0), 1)]

# a__, b__ = Point(2, 2), Point(0.5, 0.5)
# c__ = [Circle(Point(0, 0), 1)]

a__ = Point(x=1, y=1)
b__ = Point(x=5, y=5)
c__ = [Circle(ctr=Point(x=0, y=0), r=0.38640867748763413), Circle(ctr=Point(x=0, y=1), r=0.20012473419774324),
       Circle(ctr=Point(x=0, y=2), r=0.4910248144296929), Circle(ctr=Point(x=0, y=3), r=0.33334242256823926),
       Circle(ctr=Point(x=0, y=4), r=0.3390456042950973), Circle(ctr=Point(x=0, y=5), r=0.3665664402069524),
       Circle(ctr=Point(x=0, y=6), r=0.47572857371997085), Circle(ctr=Point(x=0, y=7), r=0.823775384039618),
       Circle(ctr=Point(x=1, y=0), r=0.605539690121077), Circle(ctr=Point(x=1, y=2), r=0.8604423254029825),
       Circle(ctr=Point(x=1, y=3), r=0.37138958300929514), Circle(ctr=Point(x=1, y=4), r=0.5601797837996855),
       Circle(ctr=Point(x=1, y=5), r=0.7542402487015352), Circle(ctr=Point(x=1, y=6), r=0.4849949301453307),
       Circle(ctr=Point(x=1, y=7), r=0.33705196499358864), Circle(ctr=Point(x=2, y=0), r=0.4161911523202434),
       Circle(ctr=Point(x=2, y=1), r=0.604188579856418), Circle(ctr=Point(x=2, y=2), r=0.27119430333841593),
       Circle(ctr=Point(x=2, y=3), r=0.6511102757183834), Circle(ctr=Point(x=2, y=4), r=0.5126366399461403),
       Circle(ctr=Point(x=2, y=5), r=0.7969563483959063), Circle(ctr=Point(x=2, y=6), r=0.6673986469628289),
       Circle(ctr=Point(x=2, y=7), r=0.5619564772350714), Circle(ctr=Point(x=3, y=0), r=0.3324886301765218),
       Circle(ctr=Point(x=3, y=1), r=0.7300074005266651), Circle(ctr=Point(x=3, y=2), r=0.6491321481065825),
       Circle(ctr=Point(x=3, y=3), r=0.4017128477571532), Circle(ctr=Point(x=3, y=4), r=0.26374804044608025),
       Circle(ctr=Point(x=3, y=5), r=0.5922080177580937), Circle(ctr=Point(x=3, y=6), r=0.35210499849636107),
       Circle(ctr=Point(x=3, y=7), r=0.2786758293164894), Circle(ctr=Point(x=4, y=0), r=0.5483823104063049),
       Circle(ctr=Point(x=4, y=1), r=0.592110608308576), Circle(ctr=Point(x=4, y=2), r=0.2816006015287712),
       Circle(ctr=Point(x=4, y=3), r=0.5140958129195496), Circle(ctr=Point(x=4, y=4), r=0.6654430777067318),
       Circle(ctr=Point(x=4, y=5), r=0.21963583601173012), Circle(ctr=Point(x=4, y=6), r=0.5013549668015912),
       Circle(ctr=Point(x=4, y=7), r=0.43891786120366305), Circle(ctr=Point(x=5, y=0), r=0.5264885412761942),
       Circle(ctr=Point(x=5, y=1), r=0.5317781867226585), Circle(ctr=Point(x=5, y=2), r=0.35505329214502124),
       Circle(ctr=Point(x=5, y=3), r=0.4161083685932681), Circle(ctr=Point(x=5, y=4), r=0.21143551210407166),
       Circle(ctr=Point(x=5, y=6), r=0.6029599722241983), Circle(ctr=Point(x=5, y=7), r=0.6235687331529334),
       Circle(ctr=Point(x=6, y=0), r=0.40419265895616263), Circle(ctr=Point(x=6, y=1), r=0.5229661515215411),
       Circle(ctr=Point(x=6, y=2), r=0.4306587716331705), Circle(ctr=Point(x=6, y=3), r=0.5710683602141217),
       Circle(ctr=Point(x=6, y=4), r=0.5276285207597539), Circle(ctr=Point(x=6, y=5), r=0.48761439698282627),
       Circle(ctr=Point(x=6, y=6), r=0.236933310306631), Circle(ctr=Point(x=6, y=7), r=0.4831113030435517),
       Circle(ctr=Point(x=7, y=0), r=0.5696406797273085), Circle(ctr=Point(x=7, y=1), r=0.6816570753464475),
       Circle(ctr=Point(x=7, y=2), r=0.35647277624811974), Circle(ctr=Point(x=7, y=3), r=0.3498640827136114),
       Circle(ctr=Point(x=7, y=4), r=0.5531412089942023), Circle(ctr=Point(x=7, y=5), r=0.7099347036564723),
       Circle(ctr=Point(x=7, y=6), r=0.6517945740139112), Circle(ctr=Point(x=7, y=7), r=0.19755813118536025)]

# 12.655151357393386

start = time.time_ns()
print(f'shortest_path: {shortest_path_length(a__, b__, c__)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
print(f'building_graph_time_ms: {building_graph_time_ms} milliseconds')
print(f'building_circle_links_time_ms: {building_circle_links_time_ms} milliseconds')
print(f'validating_edges_time_ms: {validating_edges_time_ms} milliseconds')
print(f'getting_valid_edges_time_ms: {getting_valid_edges_time_ms} milliseconds')
print(f'merry_counter: {merry_counter}')
print(f'validating_edge_counter: {validating_edge_counter}')
print(f'getting_valid_edge_counter: {getting_valid_edge_counter}')
print(f'inner_counter: {inner_counter}')

# print(f'intersect? {intersect(Point(1, 1), Point(7, 7), Circle(Point(4, 4), 1))}')
# print(f'intersect? {intersect(Point(-3, 1), Point(4.25, 0), Circle(Point(0, 0), 2.5))}')
# print(f'angle: {angle_of_intersection(Circle(Point(10, -10), 1), Circle(Point(0, 0), 2))}')
# print(f'right angle: {2 * math.pi - math.pi / 2 / 2}')

# (Circle(ctr=Point(x=0, y=0), r=2.5), 90.0)[inf] --> (Circle(ctr=Point(x=1.5, y=2), r=0.5), 90.0)[inf]
# obstacle: 53.13010235415598

# v1__ = Vertex(Circle(Point(0, 0), 2.5), math.pi / 2)
# v2__ = Vertex(Circle(Point(0, 0), 2.5), 123.80380727004292 * math.pi / 180)
# v1__.get_rot_dir(v2__)
# v2__.get_rot_dir(v1__)
# # 36 366 98 989
# build_edges_circle([v1__, v2__], [53.13010235415598 * math.pi / 180])
# print(f'edge: {v1__.edge(v2__)}')
# print(f'right val: {2.5 * (123.80380727004292 * math.pi / 180 - math.pi / 2)}')

# print(f'{RotDir.CLOCKWISE == RotDir.ANTI_CLOCKWISE}')

# print(f'valid edges: ')
# for i, edge in enumerate(get_valid_edges(Circle(Point(1.5, 2), 0.5), Circle(Point(3.5, 1), 1), [])):
#     print(f'{i}. {edge}')
# TODO: Default dict!!!
