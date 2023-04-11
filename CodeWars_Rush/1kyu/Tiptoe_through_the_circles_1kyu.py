# accepted on codewars.com
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
circle_pairs_counter: int


class Point(NamedTuple):  # 36 366 98 989
    x: float
    y: float


class Circle(NamedTuple):
    ctr: Point
    r: float


def shortest_path_length(a: Point, b: Point, c: list[Circle]) -> float:
    """returns length of the shortest route from a to b,
    avoiding the interiors of the circles in c"""
    global circle_pairs_counter
    circle_pairs_counter = 0
    print(f'a: {a}')
    print(f'b: {b}')
    print(f'circles: {c}')
    # if start or end point lies in at least one of the circles given:
    if not validate_ab(a, b, c):
        print(f'a or b point is locked')
        return NO_PATH
    # removing the repeating circles from the list:
    circles = set(c)
    # if some circles lie in some others:
    circles = [c for c in circles if all([not _in(c, c_) for c_ in circles - {c}])]
    # here we build a graph representing the circles-obstacles for further pathfinding,
    # v_hashes needed in order not to create new Vertexes if they have already been built:
    v_hashes = build_graph(a, b, list(circles))
    print(f'v_hashes: ')
    for i, (k, v) in enumerate(v_hashes.items()):
        print(f'{i}. hash: {k}, vertex: {v}, neighs: {len(v.neighs)}')
    if (start_hash := hash(Vertex(Circle(a, 0), 0))) not in v_hashes.keys() or (
            end_hash := hash(Vertex(Circle(b, 0), 0))) not in v_hashes.keys():
        print(f'start or end point has no neighs')
        return NO_PATH
    start_vertex, end_vertex = v_hashes[start_hash], v_hashes[end_hash]  # weird !!!
    # pathfinding using Dijkstra algorithm:
    vertexes_to_be_visited = [start_vertex]  # <<-- starting point...
    start_vertex.g = 0  # here we are situated at the very beginning of the path!
    hq.heapify(vertexes_to_be_visited)  # -->> priority heap will be convenient for us.
    # the core of Dijkstra algo:
    counter = 0
    print(f'dijkstra steps: ')
    while vertexes_to_be_visited:
        # current vertex
        vertex_ = hq.heappop(vertexes_to_be_visited)
        print(f'{counter}. current vertex: {vertex_}')
        if vertex_ == end_vertex:
            # the shortest path been found:
            break
        neighs = vertex_.neighs
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
    for i, vertex in enumerate(sp := shortest_path[::-1]):
        if vertex == start_vertex:
            s = 'START'
        elif vertex == end_vertex:
            s = 'END'
        else:
            s = 'ARC' if vertex.circle == sp[i - 1].circle else 'BRIDGE'
        print(f'{i}. {s}: {vertex}')
    # check end_vertex.g:
    if end_vertex.g == np.Infinity:
        # there is no path!
        print(f'end_vertex.g = np.Infinity. THERE IS NO PATH!!!')
        return NO_PATH
    # returns the result:
    return end_vertex.g


def intersect(p1: Point, p2: Point, circle: Circle) -> bool:
    """checks the intersection of the segment and the circle"""
    if p1 != p2:
        # constants for the straight line equation:
        a, b, c = get_coeffs(p1, p2)
        # distance from the circle's center to the straight line containing the segment:
        if abs(a * circle.ctr.x + b * circle.ctr.y + c) / math.hypot(a, b) < circle.r:  # TODO: What if == ???
            # if some end segment points lies into the circle:
            if in_(p1, circle) or in_(p2, circle):
                return True
            # checks if the point of the projection of the center of the circle on straight line p1p2 lies into the segment p1p2...
            # orthogonal straight line to p1p2, let it be named as "orto",
            # circle's center belongs to the orto straight line, consequently:
            c_ = a * circle.ctr.y - b * circle.ctr.x
            # aux par:
            h = a ** 2 + b ** 2
            # now let us define the coordinates of projection point:
            x_, y_ = (-b * c_ - a * c) / h, (a * c_ - b * c) / h
            # the above condition itself:
            if math.hypot(p1.x - x_, p1.y - y_) + math.hypot(p2.x - x_, p2.y - y_) - math.hypot(-b, a) < ERR:
                return True
    else:
        raise ValueError(f'p1: {p1} and p2: {p2} cannot be the same, method: {intersect}!')
    return False


def circle_intersect(circle1: Circle, circle2: Circle) -> bool:
    """checks if two circles have non-zero area of intersection"""
    return circle1.r + circle2.r > math.hypot(circle2.ctr.y - circle1.ctr.y, circle2.ctr.x - circle1.ctr.x)


def get_valid_edges(c1_: Circle, c2_: Circle, circles: list[Circle]) -> list[tuple['Vertex', 'Vertex']]:
    """defines all valid edges for 2 circles as list of tuples: (2 linked Vertices)"""
    global circle_pairs_counter
    # possible linked vertices:
    poss_vertices = []
    # Value error if c1 in c2 or c2 in c1...
    if c1_.r != 0 or c2_.r != 0:
        # let c1 be the larger circle:
        c1, c2 = (c1_, c2_) if c1_.r > c2_.r else (c2_, c1_)
        # getting all 4 or 2 pair of points:
        # 1. 2 outer tangent edges:
        c1c2_len = math.hypot(c1.ctr.x - c2.ctr.x, c1.ctr.y - c2.ctr.y)
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
    print(f'{circle_pairs_counter}. for circles: {c1_, c2_} {len(poss_vertices)} possible vertices been found')
    vertices = [(v1, v2) for v1, v2 in poss_vertices if v1.validate_edge(v2, circles)]
    print(f'{len(vertices)} vertices remained after validation')
    circle_pairs_counter += 1
    # returns res:
    return vertices


def build_edges_circle(vertices: set['Vertex'], separators: set[float]):
    """builds all the links for all the vertices that belong to the same circle,
    taking into account the presence of circle-obstacles, called separators
    :param vertices: vertices of the same circle C
    :param separators: directing angles of intersected circles C and O (obstacle)"""
    vertices_ = list(vertices)
    if vertices_:
        for j in range(len_ := len(vertices_)):
            if vertices_[j].circle.r:
                for i in range(j + 1, len_):
                    if vertices_[j].rot_dir != vertices_[i].rot_dir:
                        min_angle_v, max_angle_v = sorted([vertices_[j], vertices_[i]], key=lambda x: x.angle)
                        flag = True
                        for obstacle in separators:
                            if min_angle_v.rot_dir == RotDir.ANTI_CLOCKWISE:
                                # anti-clockwise:
                                if min_angle_v.angle <= obstacle <= max_angle_v.angle:
                                    flag = False
                                    break
                            else:
                                # clockwise:
                                if 0 <= obstacle <= min_angle_v.angle or max_angle_v.angle <= obstacle <= 2 * math.pi:
                                    flag = False
                                    break
                        if flag:
                            vertices_[j].connect(vertices_[i])
                            vertices_[i].connect(vertices_[j])


def build_graph(a: Point, b: Point, circles: list[Circle]) -> dict:
    """builds graph: creates vertices and edges between them,
    then validates all the possible edges found,
    here edge is the tuple of two connected vertices: tuple[v1, v2]"""
    # appending a and b points to the list of circles as A and B circles:
    A, B = Circle(a, 0), Circle(b, 0)
    circles_ = circles + [A, B]
    v_hashes = dict()
    # getting possible neighbours for all circles:
    len_ = len(circles_)
    # aux dicts of vertices and separators for all the circles:
    circle_vertices = defaultdict(set[Vertex])  # : dict[Circle, list['Vertex']] = dict()
    separators = defaultdict(set[float])  # : dict[Circle, list[float]] = dict()
    for j in range(len_):
        # initializing neighs for all the vertexes:
        # busting of all possible neighs for current circle:
        for i in range(j + 1, len_):
            if circle_intersect(cj := circles_[j], ci := circles_[i]):
                separators[cj].add(angle_of_intersection(circles_[i], circles_[j]))
                separators[ci].add(angle_of_intersection(circles_[j], circles_[i]))
            valid_edges = get_valid_edges(circles_[j], circles_[i], circles_)
            for v1, v2 in valid_edges:
                # hashing:
                v1_hash, v2_hash = hash(v1), hash(v2)
                # extracting vertices from the memory:
                v1 = v_hashes.setdefault(v1_hash, v1)
                v2 = v_hashes.setdefault(v2_hash, v2)
                # building link:
                v1.connect(v2)
                v2.connect(v1)
                # defining the rotation's direction for v1 and v2 around the relative circles:
                v1.get_rot_dir(v2)
                v2.get_rot_dir(v1)
                # building vertices[circle] dict:
                circle_vertices[v1.circle].add(v1)
                circle_vertices[v2.circle].add(v2)
    # showing circle_vertices dict:
    print(f'circle_vertices: \n')
    for i, (k, v) in enumerate(circle_vertices.items()):
        print(f'{i}th circle: {k} has {len(v)} vertices')
        print(f'vertices: {v}\n')
    # getting all circle connections:
    for c in circles_:
        verts, seps = circle_vertices[c] if c in circle_vertices.keys() else {}, separators[
            c] if c in separators.keys() else {}
        build_edges_circle(verts, seps)
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
        if in_(a, circle) or in_(b, circle):
            return False
    return True


@functools.lru_cache
def get_coeffs(p1: Point, p2: Point) -> tuple[float, float, float]:
    """defines the coefficients a, b, c for the straight line,
    describing by the equation: ax + by + c = 0
    and passing through 2 different points: p1 and p2"""
    if p1 != p2:
        # constants for the straight line equation:
        return p2.y - p1.y, p1.x - p2.x, p1.y * p2.x - p2.y * p1.x
    else:
        raise ValueError(f'method: {get_coeffs}, p1: {p1} cannot be equal to p2: {p2}')


def arc(a1: float, a2: float, circle: Circle, flag: bool = True) -> float:
    """calculates the length of the arc from angle a1 to a2 for the circle given"""
    da = abs(a2 - a1)
    return da * circle.r if flag else (2 * math.pi - da) * circle.r


def scalar_product(x1: float, y1: float, x2: float, y2: float):
    """calculates the scalar product of two vectors: v1(x1, y1) and v2(x2, y2)"""
    return x1 * x2 + y1 * y2


def cross_product_val(x1: float, y1: float, x2: float, y2: float):
    """returns the scalar value of vector cross product for two vectors: v1(x1, y1) and v2(x2, y2)"""
    return x1 * y2 - x2 * y1


def angle_of_intersection(outer_obj: Circle | Point, circle: Circle):
    """defines the angle between vector(circle, outer_obj) and abscissa axis"""
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
    with some concrete value of the angle with abscissa axis and
    rotation direction around the circle..."""

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
        """returns the length of the edge from the Vertex: v1 to the Vertex: v2"""
        if self.circle == other.circle:
            # the vertices lie on the same circle:
            v1, v2 = sorted([self, other], key=lambda x: x.angle)
            # the rotation's direction also has an impact on result:
            res = arc(self.angle, other.angle, self.circle, v1.rot_dir == RotDir.ANTI_CLOCKWISE)
        else:
            # the vertices lie on the different circles,
            # it is just an euclidian distance between v1 and v2 points:
            x1, y1, x2, y2 = self.x, self.y, other.x, other.y
            res = math.hypot(x2 - x1, y2 - y1)
        return res

    def connect(self, other: 'Vertex'):
        """add only one oriented link: self -->> other!!!"""
        if self != other:
            if other not in self.neighs:
                self.neighs.add(other)

    def get_rot_dir(self, twin: 'Vertex'):
        """defines the rotation's direction of the vertex"""
        l_vector = twin.x - self.x, twin.y - self.y
        r_vector = self.x - self.circle.ctr.x, self.y - self.circle.ctr.y
        self._rot_dir = RotDir.CLOCKWISE if cross_product_val(*l_vector, *r_vector) < 0 else RotDir.ANTI_CLOCKWISE

    def validate_edge(self, other: 'Vertex', circles: list[Circle]):
        """validates the edge between 2 vertices, forbidding any intersections with outer circles"""
        if self != other:
            for circle in circles:
                if circle not in {self.circle, other.circle}:
                    if intersect(Point(self.x, self.y), Point(other.x, other.y), circle):
                        return False
            return True
        else:
            raise ValueError(f'method {self.validate_edge} works only for 2 different vertices...')

    def __eq__(self, other):
        # return (self.circle, self.angle) == (other.circle, other.angle)
        return (self.circle, self.angle, self.rot_dir) == (other.circle, other.angle, other.rot_dir)

    def __ne__(self, other):
        # return (self.circle, self.angle) != (other.circle, other.angle)
        return (self.circle, self.angle, self.rot_dir) != (other.circle, other.angle, other.rot_dir)

    def __lt__(self, other):
        # necessary for priority queue:
        return self.g < other.g

    def __str__(self):
        return f'({self.circle}, {self.angle * 180 / math.pi}, {self.rot_dir})[{self.g}]'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        # necessary for hashing:
        return hash((self.circle, self.angle))


class RotDir(Enum):
    CLOCKWISE = 0
    ANTI_CLOCKWISE = 1  # LL 36 366 98 989


# test:
a__ = Point(x=1, y=1)
b__ = Point(x=5, y=5)
c__ = [Circle(ctr=Point(x=0, y=0), r=0.6654126562743986), Circle(ctr=Point(x=0, y=1), r=0.31217519648965275),
       Circle(ctr=Point(x=0, y=2), r=0.6232015793694412), Circle(ctr=Point(x=0, y=3), r=0.38003328010799914),
       Circle(ctr=Point(x=0, y=4), r=0.48487671876177607), Circle(ctr=Point(x=0, y=5), r=0.6422045498675714),
       Circle(ctr=Point(x=0, y=6), r=0.306074228741586), Circle(ctr=Point(x=0, y=7), r=0.244301142076016),
       Circle(ctr=Point(x=1, y=0), r=0.39721861364401206), Circle(ctr=Point(x=1, y=2), r=0.2620762335702007),
       Circle(ctr=Point(x=1, y=3), r=0.6506634926484625), Circle(ctr=Point(x=1, y=4), r=0.38634094970503763),
       Circle(ctr=Point(x=1, y=5), r=0.5376846503912368), Circle(ctr=Point(x=1, y=6), r=0.46707003594036345),
       Circle(ctr=Point(x=1, y=7), r=0.27777549448801925), Circle(ctr=Point(x=2, y=0), r=0.26742543215397147),
       Circle(ctr=Point(x=2, y=1), r=0.34060722911043045), Circle(ctr=Point(x=2, y=2), r=0.6854798620341291),
       Circle(ctr=Point(x=2, y=3), r=0.2520758927408477), Circle(ctr=Point(x=2, y=4), r=0.35071621738802355),
       Circle(ctr=Point(x=2, y=5), r=0.21735540982431029), Circle(ctr=Point(x=2, y=6), r=0.5244830881953406),
       Circle(ctr=Point(x=2, y=7), r=0.5535225404581795), Circle(ctr=Point(x=3, y=0), r=0.3501366141007027),
       Circle(ctr=Point(x=3, y=1), r=0.5301065592945815), Circle(ctr=Point(x=3, y=2), r=0.4389881484017259),
       Circle(ctr=Point(x=3, y=3), r=0.24393578083966283), Circle(ctr=Point(x=3, y=4), r=0.41678757811694306),
       Circle(ctr=Point(x=3, y=5), r=0.32071782452623276), Circle(ctr=Point(x=3, y=6), r=0.42489097150294625),
       Circle(ctr=Point(x=3, y=7), r=0.5604458650366225), Circle(ctr=Point(x=4, y=0), r=0.34333327414568626),
       Circle(ctr=Point(x=4, y=1), r=0.5035224975864683), Circle(ctr=Point(x=4, y=2), r=0.20326002005888102),
       Circle(ctr=Point(x=4, y=3), r=0.45670445814214344), Circle(ctr=Point(x=4, y=4), r=0.5354257048968771),
       Circle(ctr=Point(x=4, y=5), r=0.0737719649436905), Circle(ctr=Point(x=4, y=6), r=0.497115380661929),
       Circle(ctr=Point(x=4, y=7), r=0.4282939857814543), Circle(ctr=Point(x=5, y=0), r=0.5566062846451303),
       Circle(ctr=Point(x=5, y=1), r=0.5332630266899393), Circle(ctr=Point(x=5, y=2), r=0.49985999457067337),
       Circle(ctr=Point(x=5, y=3), r=0.5349746485755236), Circle(ctr=Point(x=5, y=4), r=0.5705771960468453),
       Circle(ctr=Point(x=5, y=6), r=0.41217697656992264), Circle(ctr=Point(x=5, y=7), r=0.2867045059347944),
       Circle(ctr=Point(x=6, y=0), r=0.4715572526427856), Circle(ctr=Point(x=6, y=1), r=0.4451599790286849),
       Circle(ctr=Point(x=6, y=2), r=0.3998765137397195), Circle(ctr=Point(x=6, y=3), r=0.29262711139003783),
       Circle(ctr=Point(x=6, y=4), r=0.25993720619360156), Circle(ctr=Point(x=6, y=5), r=0.4573679857432452),
       Circle(ctr=Point(x=6, y=6), r=0.5804625564419119), Circle(ctr=Point(x=6, y=7), r=0.42483049238814535),
       Circle(ctr=Point(x=7, y=0), r=0.543992357837293), Circle(ctr=Point(x=7, y=1), r=0.3561338748642807),
       Circle(ctr=Point(x=7, y=2), r=0.4853869181604214), Circle(ctr=Point(x=7, y=3), r=0.5073142863485367),
       Circle(ctr=Point(x=7, y=4), r=0.44060976544398434), Circle(ctr=Point(x=7, y=5), r=0.3805088438179483),
       Circle(ctr=Point(x=7, y=6), r=0.3802780674425552), Circle(ctr=Point(x=7, y=7), r=0.5480423783318745)]

# 6.03335656791951

start = time.time_ns()
print(f'shortest_path: {shortest_path_length(a__, b__, c__)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')





