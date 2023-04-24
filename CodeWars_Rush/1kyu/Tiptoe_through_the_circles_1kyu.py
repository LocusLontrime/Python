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
trinity_counter: int


class Point(NamedTuple):  # 36 366 98 989
    x: float
    y: float


class Circle(NamedTuple):
    ctr: Point
    r: float


def shortest_path_length(a: Point, b: Point, c: list[Circle], flag=False) -> float:
    """returns length of the shortest route from a to b,
    avoiding the interiors of the circles in c"""
    global circle_pairs_counter, trinity_counter
    circle_pairs_counter = 0
    trinity_counter = 0
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
    circles = [c for c in circles if all([not in_(c, c_) for c_ in circles - {c}])]
    # here we build a graph representing the circles-obstacles for further pathfinding,
    # v_hashes needed in order not to create new Vertexes if they have already been built:
    v_hashes = build_graph(a, b, circles, flag)
    print(f'{len(v_hashes)} v_hashes found: ')
    if flag:
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
    print(f'dijkstra has made: ')
    while vertexes_to_be_visited:
        # current vertex
        vertex_ = hq.heappop(vertexes_to_be_visited)
        if flag:
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
    print(f'{counter + 1} steps...')
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


class TipToe:
    def __init__(self, start_point: Point, end_point: Point, circles: list[Circle]):
        self._start = start_point
        self._end = end_point
        self._circles = circles

    ...


def intersect(p1: Point, p2: Point, circle: Circle, flag: bool = False) -> bool:
    """checks the intersection of the segment and the circle"""
    if p1 != p2:
        # constants for the straight line equation:
        a, b, c = get_coeffs(p1, p2, flag)
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


def get_valid_edges(c1_: Circle, c2_: Circle, circles: list[Circle], flag: bool = False) -> list[
    tuple['Vertex', 'Vertex']]:
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
    if flag:
        print(f'{circle_pairs_counter}. for circles: {c1_, c2_} {len(poss_vertices)} possible vertices been found')
    vertices = [(v1, v2) for v1, v2 in poss_vertices if v1.validate_edge(v2, circles, flag)]
    if flag:
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


def build_graph(a: Point, b: Point, circles: list[Circle], flag=False) -> dict:
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
            valid_edges = get_valid_edges(circles_[j], circles_[i], circles_, flag)
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
    if flag:
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


def in_(obj: Point | Circle, circle: Circle) -> bool:
    """checks if the point or Circle lies in the circle ( 'circle' )"""
    if isinstance(obj, Point):
        return math.hypot(circle.ctr.y - obj.y, circle.ctr.x - obj.x) < circle.r
    elif isinstance(obj, Circle):
        return math.hypot(circle.ctr.y - obj.ctr.y, circle.ctr.x - obj.ctr.x) < circle.r - obj.r


def validate_ab(a: Point, b: Point, circles: list[Circle]) -> bool:
    """checks if a or b point lies in some circle from the list"""
    for circle in circles:
        if in_(a, circle) or in_(b, circle):
            return False
    return True


@functools.lru_cache
def get_coeffs(p1: Point, p2: Point, flag: bool = False) -> tuple[float, float, float]:
    """defines the coefficients a, b, c for the straight line,
    describing by the equation: ax + by + c = 0
    and passing through 2 different points: p1 and p2"""
    global trinity_counter
    if p1 != p2:
        # constants for the straight line equation:
        a, b, c = p2.y - p1.y, p1.x - p2.x, p1.y * p2.x - p2.y * p1.x
        if flag:
            print(f'{trinity_counter}. a, b, c: {a, b, c}')
        trinity_counter += 1
        return a, b, c
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

    def validate_edge(self, other: 'Vertex', circles: list[Circle], flag: bool = False):
        """validates the edge between 2 vertices, forbidding any intersections with outer circles"""
        if self != other:
            for circle in circles:
                if circle not in {self.circle, other.circle}:
                    if intersect(Point(self.x, self.y), Point(other.x, other.y), circle, flag):
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

a__x = Point(x=1, y=1)
b__x = Point(x=5, y=5)
c__x = [Circle(ctr=Point(x=0, y=0), r=0.22536087676417083), Circle(ctr=Point(x=0, y=1), r=0.31572697742376477),
        Circle(ctr=Point(x=0, y=2), r=0.34621551611926404), Circle(ctr=Point(x=0, y=3), r=0.5213144983397796),
        Circle(ctr=Point(x=0, y=4), r=0.5118164314655587), Circle(ctr=Point(x=0, y=5), r=0.24980794640723614),
        Circle(ctr=Point(x=0, y=6), r=0.5152214519446715), Circle(ctr=Point(x=0, y=7), r=0.522460746509023),
        Circle(ctr=Point(x=1, y=0), r=0.55523882440757), Circle(ctr=Point(x=1, y=2), r=0.6768058778950944),
        Circle(ctr=Point(x=1, y=3), r=0.22686033414211124), Circle(ctr=Point(x=1, y=4), r=0.40346503250766547),
        Circle(ctr=Point(x=1, y=5), r=0.6050873699365183), Circle(ctr=Point(x=1, y=6), r=0.44699280748609455),
        Circle(ctr=Point(x=1, y=7), r=0.571783722541295), Circle(ctr=Point(x=2, y=0), r=0.623612377163954),
        Circle(ctr=Point(x=2, y=1), r=0.47327484309207646), Circle(ctr=Point(x=2, y=2), r=0.4116287773707881),
        Circle(ctr=Point(x=2, y=3), r=0.6735617255559191), Circle(ctr=Point(x=2, y=4), r=0.4685481223510578),
        Circle(ctr=Point(x=2, y=5), r=0.5217285147635266), Circle(ctr=Point(x=2, y=6), r=0.30998576211277395),
        Circle(ctr=Point(x=2, y=7), r=0.5198963790899143), Circle(ctr=Point(x=3, y=0), r=0.5368135755183175),
        Circle(ctr=Point(x=3, y=1), r=0.5974121243460103), Circle(ctr=Point(x=3, y=2), r=0.5061762819299475),
        Circle(ctr=Point(x=3, y=3), r=0.4053584629436955), Circle(ctr=Point(x=3, y=4), r=0.6964988417224959),
        Circle(ctr=Point(x=3, y=5), r=0.28043378989677875), Circle(ctr=Point(x=3, y=6), r=0.503911703475751),
        Circle(ctr=Point(x=3, y=7), r=0.1262727547204122), Circle(ctr=Point(x=4, y=0), r=0.5151378431590273),
        Circle(ctr=Point(x=4, y=1), r=0.36086485579144206), Circle(ctr=Point(x=4, y=2), r=0.4173152281204238),
        Circle(ctr=Point(x=4, y=3), r=0.3183767212321982), Circle(ctr=Point(x=4, y=4), r=0.6159705261932685),
        Circle(ctr=Point(x=4, y=5), r=0.20989467788022012), Circle(ctr=Point(x=4, y=6), r=0.6259145677322522),
        Circle(ctr=Point(x=4, y=7), r=0.6778776474064215), Circle(ctr=Point(x=5, y=0), r=0.5636972558917478),
        Circle(ctr=Point(x=5, y=1), r=0.5609463461441919), Circle(ctr=Point(x=5, y=2), r=0.391939307958819),
        Circle(ctr=Point(x=5, y=3), r=0.456533202691935), Circle(ctr=Point(x=5, y=4), r=0.43285039805341513),
        Circle(ctr=Point(x=5, y=6), r=0.666378344851546), Circle(ctr=Point(x=5, y=7), r=0.5680479590082541),
        Circle(ctr=Point(x=6, y=0), r=0.4713804449653253), Circle(ctr=Point(x=6, y=1), r=0.4619080887408927),
        Circle(ctr=Point(x=6, y=2), r=0.24539715021383016), Circle(ctr=Point(x=6, y=3), r=0.3736096939304843),
        Circle(ctr=Point(x=6, y=4), r=0.6197382619371637), Circle(ctr=Point(x=6, y=5), r=0.24627519131172448),
        Circle(ctr=Point(x=6, y=6), r=0.5888057655422017), Circle(ctr=Point(x=6, y=7), r=0.5676657743984833),
        Circle(ctr=Point(x=7, y=0), r=0.540108250058256), Circle(ctr=Point(x=7, y=1), r=0.5732564409496262),
        Circle(ctr=Point(x=7, y=2), r=0.5362131939036772), Circle(ctr=Point(x=7, y=3), r=0.5966956639895216),
        Circle(ctr=Point(x=7, y=4), r=0.7095990309258923), Circle(ctr=Point(x=7, y=5), r=0.6521467766957357),
        Circle(ctr=Point(x=7, y=6), r=0.29132984827738256), Circle(ctr=Point(x=7, y=7), r=0.5453128289664164)]

# ...

a__xy = Point(x=1, y=1)
b__xy = Point(x=5, y=5)
c__xy = [Circle(ctr=Point(x=0, y=0), r=0.3733836166535602), Circle(ctr=Point(x=0, y=1), r=0.7646571021257514),
         Circle(ctr=Point(x=0, y=2), r=0.37625935979706626), Circle(ctr=Point(x=0, y=3), r=0.46151910213661984),
         Circle(ctr=Point(x=0, y=4), r=0.49633754706788186), Circle(ctr=Point(x=0, y=5), r=0.3924247965496766),
         Circle(ctr=Point(x=0, y=6), r=0.6465832422643291), Circle(ctr=Point(x=0, y=7), r=0.7355589298669372),
         Circle(ctr=Point(x=1, y=0), r=0.2556949529041494), Circle(ctr=Point(x=1, y=2), r=0.43340103319944806),
         Circle(ctr=Point(x=1, y=3), r=0.16363142176405582), Circle(ctr=Point(x=1, y=4), r=0.36872687720007097),
         Circle(ctr=Point(x=1, y=5), r=0.4654180178631844), Circle(ctr=Point(x=1, y=6), r=0.7160705898422999),
         Circle(ctr=Point(x=1, y=7), r=0.3603082984813049), Circle(ctr=Point(x=2, y=0), r=0.23005439464389651),
         Circle(ctr=Point(x=2, y=1), r=0.5210477234553427), Circle(ctr=Point(x=2, y=2), r=0.5137340003548325),
         Circle(ctr=Point(x=2, y=3), r=0.28561070378126985), Circle(ctr=Point(x=2, y=4), r=0.5427584194859758),
         Circle(ctr=Point(x=2, y=5), r=0.44646162416440927), Circle(ctr=Point(x=2, y=6), r=0.5873580569370819),
         Circle(ctr=Point(x=2, y=7), r=0.5072925438051062), Circle(ctr=Point(x=3, y=0), r=0.6543755554632266),
         Circle(ctr=Point(x=3, y=1), r=0.32641189534982995), Circle(ctr=Point(x=3, y=2), r=0.1738723820347528),
         Circle(ctr=Point(x=3, y=3), r=0.4427842675433667), Circle(ctr=Point(x=3, y=4), r=0.5237682156468356),
         Circle(ctr=Point(x=3, y=5), r=0.560401627944492), Circle(ctr=Point(x=3, y=6), r=0.5712770753708286),
         Circle(ctr=Point(x=3, y=7), r=0.4805720039034642), Circle(ctr=Point(x=4, y=0), r=0.6669233716491119),
         Circle(ctr=Point(x=4, y=1), r=0.5157106855297812), Circle(ctr=Point(x=4, y=2), r=0.5514950057560287),
         Circle(ctr=Point(x=4, y=3), r=0.33233196317322716), Circle(ctr=Point(x=4, y=4), r=0.8083744257600238),
         Circle(ctr=Point(x=4, y=5), r=0.3333187589810605), Circle(ctr=Point(x=4, y=6), r=0.7664630215297396),
         Circle(ctr=Point(x=4, y=7), r=0.32948012254500303), Circle(ctr=Point(x=5, y=0), r=0.720832835624389),
         Circle(ctr=Point(x=5, y=1), r=0.38146775936107147), Circle(ctr=Point(x=5, y=2), r=0.6902580605317346),
         Circle(ctr=Point(x=5, y=3), r=0.43938439937473345), Circle(ctr=Point(x=5, y=4), r=0.7060807031153361),
         Circle(ctr=Point(x=5, y=6), r=0.5329481712575107), Circle(ctr=Point(x=5, y=7), r=0.2679594922303426),
         Circle(ctr=Point(x=6, y=0), r=0.2701717944605807), Circle(ctr=Point(x=6, y=1), r=0.6040820497521656),
         Circle(ctr=Point(x=6, y=2), r=0.370754937522257), Circle(ctr=Point(x=6, y=3), r=0.25923713989749153),
         Circle(ctr=Point(x=6, y=4), r=0.26010998861553186), Circle(ctr=Point(x=6, y=5), r=0.6605004936242216),
         Circle(ctr=Point(x=6, y=6), r=0.47369012732331167), Circle(ctr=Point(x=6, y=7), r=0.2473842261471942),
         Circle(ctr=Point(x=7, y=0), r=0.36160998572254843), Circle(ctr=Point(x=7, y=1), r=0.4487130029786687),
         Circle(ctr=Point(x=7, y=2), r=0.7419241735684938), Circle(ctr=Point(x=7, y=3), r=0.2437247934395541),
         Circle(ctr=Point(x=7, y=4), r=0.4293908535832631), Circle(ctr=Point(x=7, y=5), r=0.5398185771497245),
         Circle(ctr=Point(x=7, y=6), r=0.4960298569587059), Circle(ctr=Point(x=7, y=7), r=0.6997170076760052)]

# ...

a__xyz = Point(x=1, y=1)
b__xyz = Point(x=5, y=5)
c__xyz = [Circle(ctr=Point(x=0, y=0), r=0.4252193937057501), Circle(ctr=Point(x=0, y=1), r=0.2281870185845714),
          Circle(ctr=Point(x=0, y=2), r=0.5825998618846896), Circle(ctr=Point(x=0, y=3), r=0.5750050136799926),
          Circle(ctr=Point(x=0, y=4), r=0.48668337136309064), Circle(ctr=Point(x=0, y=5), r=0.34028009269262605),
          Circle(ctr=Point(x=0, y=6), r=0.6417128796436126), Circle(ctr=Point(x=0, y=7), r=0.14173358291305488),
          Circle(ctr=Point(x=1, y=0), r=0.24912355173545048), Circle(ctr=Point(x=1, y=2), r=0.5473393243591542),
          Circle(ctr=Point(x=1, y=3), r=0.2886043908992823), Circle(ctr=Point(x=1, y=4), r=0.2778911326107542),
          Circle(ctr=Point(x=1, y=5), r=0.2415874013517103), Circle(ctr=Point(x=1, y=6), r=0.6285921137194408),
          Circle(ctr=Point(x=1, y=7), r=0.45177837572435453), Circle(ctr=Point(x=2, y=0), r=0.5790489334295118),
          Circle(ctr=Point(x=2, y=1), r=0.36530436107238906), Circle(ctr=Point(x=2, y=2), r=0.48429977489625764),
          Circle(ctr=Point(x=2, y=3), r=0.7432412802383382), Circle(ctr=Point(x=2, y=4), r=0.42954066757550996),
          Circle(ctr=Point(x=2, y=5), r=0.2240386629414084), Circle(ctr=Point(x=2, y=6), r=0.5057563150980783),
          Circle(ctr=Point(x=2, y=7), r=0.41282407918360886), Circle(ctr=Point(x=3, y=0), r=0.5968463425614242),
          Circle(ctr=Point(x=3, y=1), r=0.3217374139740567), Circle(ctr=Point(x=3, y=2), r=0.5225387255842834),
          Circle(ctr=Point(x=3, y=3), r=0.4460426482412339), Circle(ctr=Point(x=3, y=4), r=0.5641421896212826),
          Circle(ctr=Point(x=3, y=5), r=0.622252559144413), Circle(ctr=Point(x=3, y=6), r=0.4815167649508336),
          Circle(ctr=Point(x=3, y=7), r=0.4491333434503476), Circle(ctr=Point(x=4, y=0), r=0.5529864613928466),
          Circle(ctr=Point(x=4, y=1), r=0.5454327901787127), Circle(ctr=Point(x=4, y=2), r=0.3816132202520731),
          Circle(ctr=Point(x=4, y=3), r=0.3578025755691582), Circle(ctr=Point(x=4, y=4), r=0.30828249856059814),
          Circle(ctr=Point(x=4, y=5), r=0.4457141687247314), Circle(ctr=Point(x=4, y=6), r=0.6308192735349655),
          Circle(ctr=Point(x=4, y=7), r=0.4051159265937521), Circle(ctr=Point(x=5, y=0), r=0.7116006415938577),
          Circle(ctr=Point(x=5, y=1), r=0.3545268197214862), Circle(ctr=Point(x=5, y=2), r=0.46413304991521553),
          Circle(ctr=Point(x=5, y=3), r=0.57812875545184), Circle(ctr=Point(x=5, y=4), r=0.36155457397080376),
          Circle(ctr=Point(x=5, y=6), r=0.46549263944851355), Circle(ctr=Point(x=5, y=7), r=0.33621743828787803),
          Circle(ctr=Point(x=6, y=0), r=0.2843907557460949), Circle(ctr=Point(x=6, y=1), r=0.46621271303819783),
          Circle(ctr=Point(x=6, y=2), r=0.42291315330835116), Circle(ctr=Point(x=6, y=3), r=0.5267438555353943),
          Circle(ctr=Point(x=6, y=4), r=0.18725541685438332), Circle(ctr=Point(x=6, y=5), r=0.34984471670280376),
          Circle(ctr=Point(x=6, y=6), r=0.3625074671117228), Circle(ctr=Point(x=6, y=7), r=0.7902471717791125),
          Circle(ctr=Point(x=7, y=0), r=0.5343838964198483), Circle(ctr=Point(x=7, y=1), r=0.3095288716926172),
          Circle(ctr=Point(x=7, y=2), r=0.3547652894917585), Circle(ctr=Point(x=7, y=3), r=0.35156580429380174),
          Circle(ctr=Point(x=7, y=4), r=0.35634704222796426), Circle(ctr=Point(x=7, y=5), r=0.27131123068372737),
          Circle(ctr=Point(x=7, y=6), r=0.4673668911178974), Circle(ctr=Point(x=7, y=7), r=0.7024918006908409)]

# 6.313663992741751

a__q = Point(x=1, y=1)
b__q = Point(x=5, y=5)
c__q = [Circle(ctr=Point(x=0, y=0), r=0.38640867748763413), Circle(ctr=Point(x=0, y=1), r=0.20012473419774324),
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
print(f'shortest_path: {shortest_path_length(a__q, b__q, c__q, flag=True)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
