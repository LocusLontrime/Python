from enum import Enum

import arcade

# math:
import math

# abstract classes:
from abc import ABC, abstractmethod

# logging
import logging
from logging import config

# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050

# Moore's neighbourhood:
moore_walk = tuple((j, i) for j in range(-1, 2) for i in range(-1, 2) if j | i)

# debugging:
is_debug = False


class GraphLastarT(arcade.Window):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        # cursor change:
        self.CURSOR_HAND = 'hand'
        # choosing the main background colour:
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        # graph:
        self.graph = Graph()

    def setup(self):
        self.create_graph_sample()
        # initializing the graph nodes' sprites:
        for node_ in self.graph.nodes.values():
            node_.get_solid_colour_sprite(self.graph)

    def create_graph_sample(self):
        # graph nodes:
        self.graph.add_node(300, 300, 1)
        self.graph.add_node(500, 300, 2)
        self.graph.add_node(300, 500, 3)
        self.graph.add_node(900, 700, 4)
        self.graph.add_node(600, 850, 5)

        self.graph.add_node(1550, 650, 6)

        # links:
        self.graph.nodes[1].append_link(self.graph.nodes[2])
        self.graph.nodes[2].append_link(self.graph.nodes[3])
        self.graph.nodes[1].append_link(self.graph.nodes[3])
        self.graph.nodes[3].append_link(self.graph.nodes[1])
        self.graph.nodes[3].append_link(self.graph.nodes[4])
        self.graph.nodes[4].append_link(self.graph.nodes[5])
        self.graph.nodes[3].append_link(self.graph.nodes[6])
        self.graph.nodes[5].append_link(self.graph.nodes[6])

        # removing:

        self.graph.nodes[3].remove_link(self.graph.nodes[4])

        self.graph.erase_node(self.graph.nodes[3])

        arcade.text_pillow.Sprite

    def on_draw(self):
        # renders this screen:
        arcade.start_render()
        # graph drawing:
        self.graph.node_sprite_list.draw()
        for node_ in self.graph.nodes.values():
            for _, link in node_.links.items():
                link.draw()

    def update(self, delta_time: float):
        ...

    def on_key_press(self, symbol: int, modifiers: int):
        ...

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        ...

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        ...


class Connected(ABC):  # Connected
    """interface for connection between two elements (class exemplars)"""

    def __init__(self):
        # object to be managed:
        self.log = logging.getLogger('Connected')
        self._obj = None

    # connects elements (one-way link):
    @abstractmethod
    def connect(self, obj):
        self.log.info('Connected')  # WITH WHAT???
        self._obj = obj


class FuncConnected(ABC):
    """interface for connection between an element (class exemplar)
    and some method(s) of another one"""

    def __init__(self):
        # function/functions connected:
        self._func = None

    # connects elements and methods:
    # TODO: get smart!!! Must process two or more functions...
    def connect_to_func(self, *func):
        log = logging.getLogger('FuncConnected')
        try:
            log.info(f'Connected to func {func.__name__}')
        except AttributeError:
            log.info(f'Connected to func {func}')
        self._func = func


class DrawLib:
    @staticmethod
    def create_line_arrow(node: 'GridNode', deltas: tuple[int, int] = (-1, 0),
                          grid: 'Grid' = None):
        """creates a guiding triangle-arrow in order to visualize the path and visited nodes more comprehensively,
        by default the arrow to be drawn is left sided"""
        cx, cy = 5 + node.x * grid.tile_size + grid.tile_size / 2, 5 + node.y * grid.tile_size + grid.tile_size / 2
        h = 2 * grid.tile_size // 3
        _h, h_, dh = h / 6, h / 3, h / 2  # for 90 degrees triangle
        shape = arcade.create_triangles_filled_with_colors(
            (
                (cx + deltas[0] * h_, cy + deltas[1] * h_),
                (cx - (deltas[0] * _h + deltas[1] * dh), cy - (deltas[0] * dh + deltas[1] * _h)),
                (cx - (deltas[0] * _h - deltas[1] * dh), cy - (-deltas[0] * dh + deltas[1] * _h))
            ),
            (
                arcade.color.BLACK,
                arcade.color.BLACK,
                arcade.color.BLACK
            )
        )
        return shape

    # helpful auxiliary methods:
    @staticmethod
    def is_point_in_square(cx, cy, size, x, y):
        """checks if the point given located in the square with the center in (cx, cy) and side that equals size"""
        return cx - size / 2 <= x <= cx + size / 2 and cy - size / 2 <= y <= cy + size / 2

    @staticmethod
    def is_point_in_circle(cx, cy, r, x, y):
        """checks if the point given located in the circle with the center in (cx, cy) and radius that equals r"""
        return (cx - x) ** 2 + (cy - y) ** 2 <= r ** 2

    @staticmethod
    def is_point_in_ellipse(cx, cy, rx, ry, x, y):
        """checks if the point given located in the ellipse with the center in (cx, cy) and radius 1 and 2: rx and ry"""
        return ry * 2 * (cx - x) ** 2 + rx ** 2 * (cy - y) ** 2 <= (rx * ry) ** 2

    @staticmethod
    def draw_icon_lock():
        """draws a lock for an icon"""
        ...


class Drawable(ABC):
    """interface for drawable element"""

    # logging.config.fileConfig('log.conf', disable_existing_loggers=True)

    # on initialization (loads presets):
    @abstractmethod
    def setup(self):
        ...

    # on every frame:
    @abstractmethod
    def update(self):
        ...

    # renders the element:
    @abstractmethod
    def draw(self):
        ...


class Structure(ABC):
    """parental class for different kinds of structures like graph, grid and so on"""

    def __init__(self):
        # a node chosen for info displaying
        self._node_chosen = None
        # modes:
        self._mode = 0  # 98 for building the walls and erasing them afterwards for the every structure, the modes remained can vary...
        self._mode_names = None

    @abstractmethod
    def get_neighs(self, node: 'Node', forbidden_node_types: list['NodeType']) -> list['Node']:
        # TODO: exclude .get_neighs(...) method from Node class and implement it in all Structures
        ...

    @abstractmethod
    def initialize_guiding_arrows(self):
        ...

    @abstractmethod
    def get_pars(self):
        ...

    @abstractmethod
    def node(self, num: int) -> 'Node':
        ...

    @abstractmethod
    def get_node(self, mouse_x, mouse_y):
        ...

    # getters/setters...

    # some methods:
    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def can_start(self):
        ...

    @abstractmethod
    def clear_redo_memo(self):
        ...

    # make a node the chosen one:
    @abstractmethod
    def choose_node(self, node: 'Node'):
        """chooses a node for info display"""
        self._node_chosen = node

    @abstractmethod
    def setup(self):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def scroll(self):
        self._mode = (self._mode + 1) % len(self._mode_names)

    @abstractmethod
    def draw(self):
        ...

    # something, rotating the guiding arrows if such ones exist
    ...

    # something, removing the guiding arrows from the SpriteList
    ...


class Link(Drawable):
    """Represents an edge, connecting two nodes, in a Graph; can be ONLY directed.
    Undirected connection can be expressed with two directed links"""

    ANGLE = 15  # in degrees

    def __init__(self, node1: 'GraphNode', node2: 'GraphNode', val: int | float = None):
        # nodes:
        self.to_ = node2
        self.from_ = node1
        self.val = None
        self.link_length_init(val)
        # segment line:
        # self.link_shape = arcade.create_line(node1.x, node1.y, node2.x, node2.y, arcade.color.BLACK, line_width=2)
        # directional arrow:
        # self.link_arrow_shape = None  # node1->node2 arrow and visa versa
        # colour:
        self.colour = None

    # link's length initialization:
    def link_length_init(self, val: int):
        # value (the length of the link)
        # if the lengths of the nodes' links are equal to euclidian distances between these 2 nodes...
        self.val = GraphNode.euclidian_distance(self.to_, self.from_)

    # def link_init(self, node1: 'GraphNode', node2: 'GraphNode'):
    #     # type of node initialization:
    #     if node1 in node2.links:
    #         self.type = LinkType.UNDIRECTED
    #     else:
    #         self.type = LinkType.DIRECTED
    #     # links' drawing section:
    #     # in the draw section now...

    # def move(self, ): DEPRECATED, now links' coords are strictly affected by nodes' coords
    #     ...

    def locate_directional_arrow(self):
        ...

    def setup(self):
        pass

    def update(self):
        pass

    def draw(self):
        # draws per every frame the link in accordance with 'from' and 'to' nodes' coords ->
        angle_rad = Link.ANGLE * math.pi / 180
        distance = math.hypot(abs(self.from_.y - self.to_.y), abs(self.from_.x - self.to_.x))
        ys, xs = Link.sep_seg(self.from_.y, self.from_.x, self.to_.y, self.to_.x, Graph.NODE_RADIUS, distance - Graph.NODE_RADIUS)
        ye, xe = Link.sep_seg(self.from_.y, self.from_.x, self.to_.y, self.to_.x, distance - Graph.NODE_RADIUS, Graph.NODE_RADIUS)
        # the link itself:
        Link.draw_arrow_line(ys, xs, ye, xe)

    @staticmethod
    def draw_arrow_line(ys: int | float, xs: int | float, ye: int | float, xe: int | float, arrow_side_length=5 * 2, arrow_angle=30, line_w=2):
        rad_angle = arrow_angle * math.pi / 180
        distance = math.hypot(abs(ye - ys), abs(xe - xs))
        y0_, x0_ = Link.sep_seg(ye, xe, ys, xs, arrow_side_length, distance - arrow_side_length)
        arcade.draw_line(xs, ys, xe, ye, arcade.color.BLACK, line_w)  # 1???
        arcade.draw_line(xe, ye, *Link.rotate(y0_, x0_, rad_angle, ye, xe), arcade.color.BLACK, line_w)
        arcade.draw_line(xe, ye, *Link.rotate(y0_, x0_, -rad_angle, ye, xe), arcade.color.BLACK, line_w)

    @staticmethod
    def rotate(y: int | float, x: int | float, rad_angle: int | float, y0: int | float, x0: int | float) -> tuple[int | float, int | float]:
        """rotates (y, x) point relative to the coordinate system with the center in (y0, x0),
        positive angle is for anti-clockwise rotation direction"""
        y_rel, x_rel = y - y0, x - x0
        return x0 + math.cos(rad_angle) * x_rel - math.sin(rad_angle) * y_rel, y0 + math.sin(rad_angle) * x_rel + math.cos(rad_angle) * y_rel

    @staticmethod
    def sep_seg(ys: int | float, xs: int | float, ye: int | float, xe: int | float, p: int | float, q: int | float) -> \
    tuple[int | float, int | float]:
        return (p * ye + q * ys) / (p + q), (p * xe + q * xs) / (p + q)


class Graph(Structure, Drawable, FuncConnected):
    """represents a graph of nodes -->> POSTPONED"""

    NODE_RADIUS = 16

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger('Graph')
        # the graph itself:
        # TODO: it is necessary to implement good dicts for graph storing...
        self._nodes: dict[int, GraphNode] = {}  # all the information needed are kept inside the nodes...
        # self._links_dict: dict[tuple[GraphNode, GraphNode], Link] = {}  # keeps all the links between the graph's nodes, keys: pairs of nodes (left=from, right=to)
        # important nodes:
        self._start_node = None
        self._end_node = None
        # game mode:
        # self._mode = 0  # 0 for building the walls and erasing them afterwards, 1 for a start and end nodes choosing and 2 for info getting for every node
        self._mode_names = {0: 'BUILDING', 1: 'START&END', 2: 'DETAILS'}
        # the current node chosen (for getting info):
        # self._node_chosen = None
        # guide arrows ON/OFF:
        self._guide_arrows_ind = None
        # visualization:
        self._node_sprite_list = arcade.SpriteList()
        self._link_sprite_list = arcade.SpriteList()
        # algo steps visualization:
        self._path_arrows = arcade.ShapeElementList()  # <<-- for more comprehensive path visualization
        # pars:
        self._line_width = None
        self._node_radius = 8
        # memoization for undo/redo area:
        ...

    @property
    def nodes(self):
        return self._nodes

    @property
    def node_sprite_list(self):
        return self._node_sprite_list

    @node_sprite_list.setter
    def node_sprite_list(self, node_sprite_list):
        self._node_sprite_list = node_sprite_list

    def initialize_guiding_arrows(self):
        pass

    def get_pars(self):
        pass

    def node(self, num: int) -> 'GraphNode':
        return self._nodes[num]

    def get_node(self, mouse_x, mouse_y):
        for node_ in self._nodes.values():
            if DrawLib.is_point_in_circle(node_.x, node_.y, 10, mouse_x, mouse_y):
                return node_

    def can_start(self):
        """checks if start and end nodes are chosen"""
        return self._start_node is not None and self._end_node is not None

    def clear_redo_memo(self):
        pass

    def scroll(self):
        pass

    def get_neighs(self, node: 'GraphNode', forbidden_node_types: list['NodeType']) -> list['GraphNode']:
        ...

    def choose_node(self, node: 'GraphNode'):
        self._node_chosen = node

    # def move_node(self, node_: 'GraphNode', y_: float, x_: float):
    #     # moves node to the new coords, redraws all the links affected ->
    #     node_.move(y_, x_)
    #     ...

    def add_node(self, x, y, number):
        # just adds a new node without any links:
        new_node = GraphNode(y, x, number, NodeType.EMPTY)
        self._nodes[number] = new_node

    def erase_node(self, node: 'GraphNode'):  # , y, x
        # get node at first...
        #node: GraphNode = ...
        # erasing all the links (directed ones more carefully):
        neighs = [n for n in node.links.keys()]
        for neigh in neighs:
            link = node.links[neigh]
            del node.links[neigh]
        for node_ in self.nodes.values():
            if node in node_.links.keys():
                del node_.links[node]
        # erasing the node's sprite:
        # self.node_sprite_list.remove(node.sprite)
        # now deleting the node itself:
        del self._nodes[node.val]

    def clear_empty_nodes(self):
        """clear the graph from the algo's visualization"""
        ...

    def clear_graph(self):
        """entirely removes the graph"""
        ...

    def initialize(self):
        # perhaps should load/initialize some simple graph for a start...
        ...

    def get_sprites(self):
        ...

    def setup(self):
        # initialization:
        self.initialize()
        # sprites, shapes etc...
        # blocks:
        self.get_sprites()

    def update(self):
        pass

    def draw(self):
        # drawing nodes:
        ...
        # drawing links:
        ...


class Node(ABC):

    # is_greedy = False

    def __init__(self, y: int, x: int, val: int, node_type: 'NodeType'):
        # type and sprite:
        self.type = node_type
        self.sprite = None
        self.guiding_arrow_sprite = None  # for more comprehensive visualization, consist of three line shapes
        # important pars:
        self.y, self.x = y, x
        self.val = val
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one
        self.times_visited = 0
        self.times_neighbourized = 0
        # cost and heuristic vars:
        self.g = math.inf  # np.Infinity || aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        self.tiebreaker = None  # recommended for many shortest paths situations
        # f = h + g or total cost of the current Node is not needed here
        self.heuristics = {}
        self.tiebreakers = {}

    @abstractmethod
    def init_heurs_ties(self):
        ...

    # @staticmethod DEPRECATED
    # def set_greedy(greedy_ind: int):
    #     Node.is_greedy = False if greedy_ind is None else True

    @property
    def coords(self):
        """returns a tuple of node's coordinates: (x, y)"""
        return self.x, self.y

    @property
    def f(self):
        """returns overall node's estimation f"""
        return self.g + self.h

    @abstractmethod
    def smart_copy(self, attributes: list[str]):
        ...

    @abstractmethod
    def smart_restore(self, other: 'Node', attributes: list[str]):
        ...

    @abstractmethod
    def smart_core(self, other: 'Node', attributes: list[str]):
        ...

    @abstractmethod
    def get_solid_colour_sprite(self, structure: Structure):
        ...

    @abstractmethod
    def update_sprite_colour(self):
        ...

    @abstractmethod
    def __eq__(self, other):
        ...

    @abstractmethod
    def __lt__(self, other):
        ...

    @abstractmethod
    def __hash__(self):
        ...

    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def heur_clear(self):
        ...

    # TODO: ELIMINATE THESE METHODS (should be moved to Structure classes!!!)
    @abstractmethod
    def get_neighs(self, struct: Structure, forbidden_node_types: list['NodeType']) -> list['Node']:
        ...

    @abstractmethod
    def get_extended_neighs(self, struct: Structure) -> list['Node']:
        ...


class GraphNode(Node):
    def __init__(self, y: int, x: int, val, node_type: 'NodeType'):
        # super method call:
        super().__init__(y, x, val, node_type)
        # logger
        self.log = logging.getLogger('GraphNode')
        # graph-only pars:
        self.links: dict[GraphNode, Link] = dict()  # neighs and links simultaneously...

    def init_heurs_ties(self):
        # heurs and ties for graph?!? TODO: find all reasonable...
        self.heuristics[...] = ...
        self.tiebreaker[...] = ...

    @staticmethod
    def euclidian_distance(node1: 'GraphNode', node2: 'GraphNode'):
        return math.sqrt((node1.y - node2.y) ** 2 + (node1.x - node2.x) ** 2)

    def append_link(self, node_to: 'GraphNode'):  # node_from: 'GraphNode' is the node itself -> self.
        # checks if the link exists:
        if node_to not in self.links.keys():
            # val = self.euclidian_distance(self, node_to)  # should be initialized in GraphNode class...
            # new link:
            new_link = Link(self, node_to)
            # adding a new link:
            self.links[node_to] = new_link
        else:
            print(f'This link is already appended!!!')

    def remove_link(self, node_to: 'GraphNode'):  # node_from: 'GraphNode' is the node itself -> self.
        if node_to in self.links:
            del self.links[node_to]

    # DUNDERS:
    def __str__(self):
        ...

    def __repr__(self):
        ...

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __hash__(self):
        return self.val

    def move(self, y_: float, x_: float):
        # the node moves:
        self.y = y_
        self.x = x_
        # all the links connected are automatically being redrawn:
        # for neigh_node, link in self.links.items():
        #     ...

    # SMART COPYING SECTION:
    def smart_copy(self, attributes: list[str]):
        pass

    def smart_restore(self, other: 'GraphNode', attributes: list[str]):
        pass

    def smart_core(self, other: 'GraphNode', attributes: list[str]):
        pass

    # DRAWINGS:
    def get_solid_colour_sprite(self, graph: Graph):
        # need something spherical...
        """makes a solid colour sprite for a node"""
        self.sprite = arcade.SpriteCircle(16, arcade.color.RED)
        self.sprite.center_x, self.sprite.center_y = self.x, self.y
        graph.node_sprite_list.append(self.sprite)

    def update_sprite_colour(self):
        pass

    # CLEARING:
    def clear(self):
        pass

    def heur_clear(self):
        pass

    # TODO: ELIMINATE THESE METHODS (should be moved to Structure classes!!!)
    # NEIGHBOURIZING:
    def get_neighs(self, structure: Structure, forbidden_node_types: list['NodeType']) -> list['Node']:
        pass

    def get_extended_neighs(self, structure: Structure) -> list['Node']:
        pass


# enum for node type:
class NodeType(Enum):
    EMPTY = arcade.color.WHITE
    WALL = arcade.color.BLACK
    VISITED_NODE = arcade.color.ROSE_QUARTZ
    NEIGH = arcade.color.BLUEBERRY
    CURRENT_NODE = arcade.color.ROSE
    START_NODE = arcade.color.GREEN
    END_NODE = (75, 150, 0)
    PATH_NODE = arcade.color.RED
    TWICE_VISITED = arcade.color.BRONZE
    TWICE_NEIGHBOURIZED = arcade.color.PURPLE
    FRONT_NEIGH = arcade.color.CYAN


class InterType(Enum):
    NONE = 1
    HOVERED = 2
    PRESSED = 3


class MenuType(Enum):
    SETTINGS = 1
    BFS_DFS = 2
    A_STAR = 3
    WAVE_LEE = 4


class LinkType(Enum):
    DIRECTED = 1
    UNDIRECTED = 2


def main():
    game = GraphLastarT(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
