import heapq as hq
import time
import math
import numpy as np
# graphics:
import arcade

# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050
TILE_SIZE: int


class Astar(arcade.Window):  # 36 366 98 989 LL
    def __init__(self, width: int, height: int, vertical_tiles=25, line_width=3):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        # scaling:
        self.scale = 0
        self.scale_names = {0: 5, 1: 10, 2: 15, 3: 22, 4: 33, 5: 45, 6: 66, 7: 90, 8: 110, 9: 165}
        # data and info:
        self.line_width = line_width
        self.tiles_q = vertical_tiles
        self.Y, self.X = SCREEN_HEIGHT - 26, SCREEN_WIDTH - 250
        self.tile_size, self.hor_tiles_q = self.get_pars()
        self.iterations = 0
        self.nodes_visited = set()
        self.path_length = 0
        self.time_elapsed_ms = 0
        # grid of nodes:
        self.grid = [[Node(j, i, 1) for i in range(self.hor_tiles_q)] for j in range(self.tiles_q)]
        # interactions:
        self.building_walls_flag = False
        self.mode = 0  # 0 for building the walls when 1 for erasing them afterwards, 2 for a start node choosing and 3 for an end one...
        self.mode_names = {0: 'BUILDING/ERASING', 1: 'START & END NODES CHOOSING'}
        self.build_or_erase = True  # True for building and False for erasing
        self.heuristic = 0
        self.heuristic_names = {0: 'MANHATTAN', 1: 'EUCLIDIAN', 2: 'MAX_DELTA', 3: 'DIJKSTRA'}
        self.tiebreaker = None
        self.tiebreaker_names = {0: 'VECTOR_CROSS', 1: 'COORDINATES'}
        # a_star important pars:
        self.start_node = None
        self.end_node = None
        self.greedy_flag = False  # is algorithm greedy?

    def get_pars(self):
        self.Y, self.X = SCREEN_HEIGHT - 60, SCREEN_WIDTH - 250
        self.tiles_q = self.scale_names[self.scale]
        self.line_width = int(math.sqrt(max(self.scale_names.values()) / self.tiles_q))
        tile_size = self.Y // self.tiles_q
        hor_tiles_q = self.X // tile_size
        self.Y, self.X = self.tiles_q * tile_size, hor_tiles_q * tile_size
        return tile_size, hor_tiles_q

    def get_hor_tiles(self, i):
        return (SCREEN_WIDTH - 250) // ((SCREEN_HEIGHT - 30) // self.scale_names[i])

    @staticmethod
    def get_ms(start, finish):
        return (finish - start) // 10 ** 6

    def setup(self):
        # game set up is located below:
        # sprites and etc...
        ...

    def draw_grid_lines(self):
        for j in range(self.tiles_q + 1):
            arcade.draw_line(5, 5 + self.tile_size * j, 5 + self.X, 5 + self.tile_size * j, arcade.color.BLACK,
                             self.line_width)

        for i in range(self.hor_tiles_q + 1):
            arcade.draw_line(5 + self.tile_size * i, 5, 5 + self.tile_size * i, 5 + self.Y, arcade.color.BLACK,
                             self.line_width)

    def on_draw(self):
        # renders this screen:
        arcade.start_render()
        # image's code:
        # grid:
        self.draw_grid_lines()
        # blocks:
        for y in range(self.tiles_q):
            for x in range(self.hor_tiles_q):
                if self.grid[y][x].colour:
                    arcade.draw_rectangle_filled(5 + self.tile_size * x + self.tile_size / 2,
                                                 5 + self.tile_size * y + self.tile_size / 2,
                                                 self.tile_size - 2 * self.line_width - (
                                                     1 if self.line_width % 2 != 0 else 0),
                                                 self.tile_size - 2 * self.line_width - (
                                                     1 if self.line_width % 2 != 0 else 0), self.grid[y][x].colour)
        # HINTS:
        arcade.draw_text(f'Mode: {self.mode_names[self.mode]}', 25, SCREEN_HEIGHT - 35, arcade.color.BLACK, bold=True)
        arcade.draw_text(
            f'A* iters: {self.iterations}, path length: {self.path_length}, nodes visited: {len(self.nodes_visited)}, time elapsed: {self.time_elapsed_ms}',
            365, SCREEN_HEIGHT - 35, arcade.color.BROWN, bold=True)
        # SET-UPS:
        arcade.draw_text(f'Heuristics: ', SCREEN_WIDTH - 235, SCREEN_HEIGHT - 70, arcade.color.BLACK, bold=True)
        for i in range(len(self.heuristic_names)):
            arcade.draw_rectangle_outline(SCREEN_WIDTH - 225, SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * i, 18, 18,
                                          arcade.color.BLACK, 2)
            arcade.draw_text(f'{self.heuristic_names[i]}', SCREEN_WIDTH - 225 + (18 + 2 * 2),
                             SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * i - 6, arcade.color.BLACK, bold=True)

        arcade.draw_rectangle_filled(SCREEN_WIDTH - 225, SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * self.heuristic, 14,
                                     14,
                                     arcade.color.BLACK)

        arcade.draw_text(f'Tiebreakers: ', SCREEN_WIDTH - 235, SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * 3 - 18 * 3,
                         arcade.color.BLACK, bold=True)
        for i in range(len(self.tiebreaker_names)):
            arcade.draw_rectangle_outline(SCREEN_WIDTH - 225,
                                          SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * (3 + i) - 18 * 3 - 30, 18,
                                          18, arcade.color.BLACK, 2)
            arcade.draw_text(self.tiebreaker_names[i], SCREEN_WIDTH - 225 + (18 + 2 * 2),
                             SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * (3 + i) - 18 * 3 - 30 - 6, arcade.color.BLACK,
                             bold=True)

        if self.tiebreaker is not None:
            arcade.draw_rectangle_filled(SCREEN_WIDTH - 225,
                                         SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * (3 + self.tiebreaker) - 18 * 3 - 30,
                                         14,
                                         14, arcade.color.BLACK)

        arcade.draw_text('Is greedy: ', SCREEN_WIDTH - 235,
                         SCREEN_HEIGHT - 130 - (18 + 2 * 2 + 18) * 4 - 2 * 18 * 3,
                         arcade.color.BLACK, bold=True)
        arcade.draw_rectangle_outline(SCREEN_WIDTH - 225,
                                      SCREEN_HEIGHT - 130 - (18 + 2 * 2 + 18) * 4 - 2 * 18 * 3 - 30, 18, 18,
                                      arcade.color.BLACK, 2)
        arcade.draw_text(f'GREEDY FLAG', SCREEN_WIDTH - 225 + (18 + 2 * 2),
                         SCREEN_HEIGHT - 130 - (18 + 2 * 2 + 18) * 4 - 2 * 18 * 3 - 30 - 6,
                         arcade.color.BLACK, bold=True)

        if self.greedy_flag:
            arcade.draw_rectangle_filled(SCREEN_WIDTH - 225,
                                         SCREEN_HEIGHT - 130 - (18 + 2 * 2 + 18) * 4 - 2 * 18 * 3 - 30, 14,
                                         14,
                                         arcade.color.BLACK)

        arcade.draw_text('Sizes in tiles: ', SCREEN_WIDTH - 235,
                         SCREEN_HEIGHT - 160 - (18 + 2 * 2 + 18) * 4 - 3 * 18 * 3,
                         arcade.color.BLACK, bold=True)

        for i in range(len(self.scale_names)):
            arcade.draw_rectangle_outline(SCREEN_WIDTH - 225,
                                          SCREEN_HEIGHT - 160 - (18 + 2 * 2 + 18) * (4 + i) - 3 * 18 * 3 - 30, 18, 18,
                                          arcade.color.BLACK, 2)
            arcade.draw_text(f'{self.scale_names[i]}x{self.get_hor_tiles(i)}', SCREEN_WIDTH - 225 + (18 + 2 * 2),
                             SCREEN_HEIGHT - 160 - (18 + 2 * 2 + 18) * (4 + i) - 3 * 18 * 3 - 30 - 6,
                             arcade.color.BLACK, bold=True)

        arcade.draw_rectangle_filled(SCREEN_WIDTH - 225,
                                     SCREEN_HEIGHT - 160 - (18 + 2 * 2 + 18) * (4 + self.scale) - 3 * 18 * 3 - 30, 14,
                                     14,
                                     arcade.color.BLACK)

    def rebuild_map(self):
        self.tile_size, self.hor_tiles_q = self.get_pars()
        print(f'tile size: {self.tile_size}, line width: {self.line_width}')
        # grid's renewing:
        self.grid = [[Node(j, i, 1) for i in range(self.hor_tiles_q)] for j in range(self.tiles_q)]
        # pars resetting:
        self.iterations = 0
        self.nodes_visited = set()
        self.path_length = 0
        self.time_elapsed_ms = 0
        self.start_node = None
        self.end_node = None

    def update(self, delta_time: float):
        # game logic and movement mechanics lies here:
        ...

    def erase_all_linked_nodes(self, node: 'Node'):
        node.passability = True
        node.colour = None
        for neigh in node.get_extended_neighs(self):
            if not neigh.passability:
                self.erase_all_linked_nodes(neigh)

    def clear_empty_nodes(self):
        # clearing the every empty node:
        for row in self.grid:
            for node in row:
                if node.passability and node not in [self.start_node, self.end_node]:
                    node.clear()
                else:
                    node.heur_clear()
        # clearing the nodes-relating pars of the game:
        self.nodes_visited = set()
        self.time_elapsed_ms = 0
        self.iterations = 0
        self.path_length = 0

    def clear_grid(self):
        # clearing the every node:
        for row in self.grid:
            for node in row:
                node.clear()
        # clearing the nodes-relating pars of the game:
        self.start_node, self.end_node = None, None
        self.nodes_visited = set()
        self.time_elapsed_ms = 0
        self.iterations = 0
        self.path_length = 0

    def on_key_press(self, symbol: int, modifiers: int):
        # is called when user press the symbol key:
        match symbol:
            # a_star_call:
            case arcade.key.SPACE:
                if self.start_node and self.end_node:
                    start = time.time_ns()
                    the_shortest_path = self.start_node.a_star(self.end_node, self)
                    self.path_length = len(the_shortest_path)
                    finish = time.time_ns()
                    self.time_elapsed_ms = self.get_ms(start, finish)
                    for node in the_shortest_path:
                        if node not in [self.start_node, self.end_node]:
                            node.colour = arcade.color.RED
            # grid clearing:
            case arcade.key.ENTER:
                self.clear_grid()
            # recall a_star :
            case arcade.key.BACKSPACE:
                self.clear_empty_nodes()

    def get_node(self, mouse_x, mouse_y):
        x_, y_ = mouse_x - 5, mouse_y - 5
        x, y = x_ // self.tile_size, y_ // self.tile_size
        return self.grid[y][x] if 0 <= x < self.hor_tiles_q and 0 <= y < self.tiles_q else None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.building_walls_flag:
            if self.mode == 0:
                if self.build_or_erase is not None:
                    if self.build_or_erase:
                        n = self.get_node(x, y)
                        if n:
                            n.passability = False
                            n.colour = arcade.color.BLACK
                    else:
                        n = self.get_node(x, y)
                        if n:
                            n.passability = True
                            n.colour = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # setting_up heuristic and tiebreaker:
        for i in range(len(self.heuristic_names)):
            if SCREEN_WIDTH - 225 - 9 <= x <= SCREEN_WIDTH - 225 + 9 and SCREEN_HEIGHT - 100 - (
                    18 + 2 * 2 + 18) * i - 9 <= y <= SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * i + 9:
                self.heuristic = i
                break
        for i in range(len(self.tiebreaker_names)):
            if SCREEN_WIDTH - 225 - 9 <= x <= SCREEN_WIDTH - 225 + 9 and SCREEN_HEIGHT - 100 - (
                    18 + 2 * 2 + 18) * (3 + i) - 18 * 3 - 30 - 9 <= y <= SCREEN_HEIGHT - 100 - (
                    18 + 2 * 2 + 18) * (3 + i) - 18 * 3 - 30 + 9:
                self.tiebreaker = None if self.tiebreaker == i else i
                break
        for i in range(len(self.scale_names)):
            if SCREEN_WIDTH - 225 - 9 <= x <= SCREEN_WIDTH - 225 + 9 and SCREEN_HEIGHT - 160 - (
                    18 + 2 * 2 + 18) * (4 + i) - 3 * 18 * 3 - 30 - 9 <= y <= SCREEN_HEIGHT - 160 - (
                    18 + 2 * 2 + 18) * (4 + i) - 3 * 18 * 3 - 30 + 9:
                self.scale = i
                self.rebuild_map()
        if SCREEN_WIDTH - 225 - 9 <= x <= SCREEN_WIDTH - 225 + 9 and SCREEN_HEIGHT - 130 - (
                18 + 2 * 2 + 18) * 4 - 2 * 18 * 3 - 30 - 9 <= y <= SCREEN_HEIGHT - 130 - (
                18 + 2 * 2 + 18) * 4 - 2 * 18 * 3 - 30 + 9:
            self.greedy_flag = not self.greedy_flag
        if self.mode == 0:
            self.building_walls_flag = True
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.build_or_erase = True
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                self.build_or_erase = False
            elif button == arcade.MOUSE_BUTTON_MIDDLE:
                self.build_or_erase = None
                n = self.get_node(x, y)
                if n:
                    self.erase_all_linked_nodes(n)
        elif self.mode == 1:
            if button == arcade.MOUSE_BUTTON_LEFT:
                sn = self.get_node(x, y)
                if sn:
                    if self.start_node: self.start_node.colour = None
                    sn.colour = arcade.color.GREEN
                    self.start_node = sn
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                en = self.get_node(x, y)
                if en:
                    if self.end_node: self.end_node.colour = None
                    en.colour = arcade.color.BLUE
                    self.end_node = en

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.mode = (self.mode + 1) % len(self.mode_names)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.building_walls_flag = False


class Node:
    # horizontal and vertical up and down moves:
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if dy * dx == 0 and (dy, dx) != (0, 0)]
    extended_walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]
    IS_GREEDY = False

    def __init__(self, y, x, val, passability=True):
        self.y, self.x = y, x
        self.val = val
        self.passability = passability
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one
        # cost and heuristic vars:
        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        self.tiebreaker = None
        # f = h + g or total cost of the current Node is not needed here
        # visual options:
        self.colour = None
        # heur dict:
        self.heuristics = {0: self.manhattan_distance, 1: self.euclidian_distance, 2: self.max_delta,
                           3: self.no_heuristic}
        self.tiebreakers = {0: self.vector_cross_product_deviation, 1: self.coordinates_pair}

    def __eq__(self, other):
        if type(self) != type(other): return False
        return (self.y, self.x) == (other.y, other.x)

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other: 'Node'):
        if self.IS_GREEDY: return (self.h, self.tiebreaker) < (other.h, other.tiebreaker)
        else: return (self.g + self.h, self.tiebreaker) < (other.g + other.h, other.tiebreaker)

    def __hash__(self):
        return hash((self.y, self.x))

    def clear(self):
        self.heur_clear()
        self.passability = True
        self.colour = None

    def heur_clear(self):
        self.g = np.Infinity
        self.h = 0
        self.tiebreaker = None
        self.previously_visited_node = None

    @staticmethod
    def manhattan_distance(node1, node2: 'Node'):
        return abs(node1.y - node2.y) + abs(node1.x - node2.x)

    @staticmethod
    def euclidian_distance(node1, node2: 'Node'):
        return math.sqrt((node1.y - node2.y) ** 2 + (node1.x - node2.x) ** 2)

    @staticmethod
    def max_delta(node1, node2: 'Node'):
        return max(abs(node1.y - node2.y), abs(node1.x - node2.x))

    @staticmethod
    def no_heuristic(node1, node2: 'Node'):
        return 0

    # self * other, tiebreaker:
    @staticmethod
    def vector_cross_product_deviation(start, end, neigh):
        v1 = neigh.y - start.y, neigh.x - start.x
        v2 = end.y - neigh.y, end.x - neigh.x
        return abs(v1[0] * v2[1] - v1[1] * v2[0])

    @staticmethod
    def coordinates_pair(start, end, neigh):
        return neigh.y, neigh.x

    def get_neighs(self, game: 'Astar') -> list['Node']:
        for dy, dx in self.walk:
            ny, nx = self.y + dy, self.x + dx
            if 0 <= ny < game.tiles_q and 0 <= nx < game.hor_tiles_q:
                if game.grid[ny][nx].passability:
                    yield game.grid[ny][nx]

    def get_extended_neighs(self, game: 'Astar') -> list['Node']:
        for dy, dx in self.extended_walk:
            ny, nx = self.y + dy, self.x + dx
            if 0 <= ny < game.tiles_q and 0 <= nx < game.hor_tiles_q:
                yield game.grid[ny][nx]

    def a_star(self, other: 'Node', game: 'Astar'):
        Node.IS_GREEDY = game.greedy_flag
        print(f'greedy_flag: {game.greedy_flag}')
        nodes_to_be_visited = [self]
        self.g = 0
        hq.heapify(nodes_to_be_visited)
        # the main cycle:
        while nodes_to_be_visited:
            game.iterations += 1
            curr_node = hq.heappop(nodes_to_be_visited)
            game.nodes_visited.add(curr_node)
            if curr_node not in [self, other]:
                curr_node.colour = arcade.color.ROSE_QUARTZ
            # base case of finding the shortest path:
            if curr_node == other: break
            # next step:
            for neigh in curr_node.get_neighs(game):
                if neigh.g > curr_node.g + neigh.val:
                    neigh.g = curr_node.g + neigh.val
                    neigh.h = neigh.heuristics[game.heuristic](neigh, other)
                    if game.tiebreaker is not None: neigh.tiebreaker = self.tiebreakers[game.tiebreaker](self, other,
                                                                                                         neigh)
                    neigh.previously_visited_node = curr_node
                    hq.heappush(nodes_to_be_visited, neigh)
        # start point of path restoration (here we begin from the end node of the shortest path found):
        node = other
        shortest_path = []
        # path restoring (here we get the reversed path):
        while node.previously_visited_node:
            shortest_path.append(node)
            node = node.previously_visited_node
        shortest_path.append(self)
        # returns the result:
        return shortest_path


def main():
    # line_width par should be even number for correct grid&nodes representation:
    game = Astar(SCREEN_WIDTH, SCREEN_HEIGHT, 28, 2)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

# v0.1 base Node class created
# v0.2 base Astar(arcade.Window) class created
# v0.3 grid lines drawing added
# v0.4 grid of nodes (self.grid) for Astar class, consisting of Nodes objects created, some fields added for both classes,
# drawing of walls (not passable nodes), start and end nodes added
# v0.5 on_mouse_press() and on_mouse_release methods() overwritten
# v0.6 on_mouse_motion() method overwritten
# v0.7 on_mouse_scroll() method overwritten, now it is possible to draw walls while mouse button pressed,
# switch drawing modes and erase walls, choose start and end node (4 modes are available for now)
# v0.8 on_key_press() method overwritten, clear() method for Node class implemented for resetting the temporal fields to its defaults,
# clear() method for Astar class added to clear all the game field (every Node), now by pressing the 'ENTER' key user can clear all the map
# v0.9 info displaying added (current mode, a_star related information)
# v1.0 a_star now is called by pressing the 'SPACE' key, the shortest way is shown on the grid
# v1.1 visited_nodes are now displayed after a_star call, info extended, hash() dunder method added for class Node
# v1.2 tiebreaker (vector cross product absolute deviation) added
# v1.3 erase separate drawing mode merged with build mode, now there is one build/erase draw mode for building walls by pressing the left mouse button
# and erasing them by pressing the right one
# v1.4 fixed a bug, when some heuristic related temporal pars have not been cleared after a_star had been called
# v1.5 now it is possible to reset all heuristic related pars for the every node on the grid but leave all the walls
# and start and end nodes at their positions by pressing the 'BACKSPACE' key, clear method for Astar class divided into two methods:
# clear_empty_nodes() for partial clearing and clear_grid() for entire clearing
# v1.6 3 auxiliary heuristics added
# v1.7 user interface for heuristic  and tiebreaker choosing added
# v1.8 fixed a bug when start and end nodes have been removed after heuristic had been chosen
# v1.9 start node choosing and end node choosing drawing modes merged into one start & end nodes choosing drawing mode,
# start node is chosen by pressing the left mouse button when end node is chosen by pressing the right one
# v1.10 coordinate pairs tiebreaker added
# v1.11 fixed bug when cross vector product deviation heuristic causes no impact on a_star
# v1.12 interface for scale choosing added
# v1.13 fixed bug when node's filled rectangle has been located not in the center of related grid cell, scaling improved
# v1.14 erase_all_linked_nodes() method added to erase all coherent wall-regions by pressing the middle mouse button on the any cell of them
# v1.15 greedy interaction added, greedy_case's of a_star logic implemented, now it is possible to find some non-shortest ways fast
# v1.16 fixed bug when the time elapsed ms have not been reset after pressing keys such as 'BACKSPACE' and 'ENTER'
# v1.17 fixed bug when greedy flag has had no impact on a_star, fixed closely related to this clearing bug when if there has been at least one
# important node (start or end) unselected clearing process has been finished with error
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# TODO: implement a step-up a_star visualization with some interaction... (high, hard)
# TODO: add some other tiebreakers (medium, easy) +-
# TODO: upgrade the visual part (medium, medium) -+
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
