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
        # data and info:
        self.line_width = line_width
        self.tiles_q = vertical_tiles
        self.Y, self.X = SCREEN_HEIGHT - 30, SCREEN_WIDTH - 250
        self.tile_size = self.Y // self.tiles_q
        self.hor_tiles_q = self.X // self.tile_size
        self.Y, self.X = self.tiles_q * self.tile_size, self.hor_tiles_q * self.tile_size
        self.iterations = 0
        self.nodes_visited = set()
        self.path_length = 0
        self.time_elapsed_ms = 0
        self.grid = [[Node(j, i, 1) for i in range(self.hor_tiles_q)] for j in range(self.tiles_q)]
        # interactions:
        self.building_walls_flag = False
        self.mode = 0  # 0 for building the walls when 1 for erasing them afterwards, 2 for a start node choosing and 3 for a end one...
        self.mode_names = {0: 'BUILDING/ERASING', 1: 'START NODE CHOOSING', 2: 'END NODE CHOOSING'}
        self.build_or_erase = True  # True for building and False for erasing
        self.heuristic = 0
        self.heuristic_names = {0: 'MANHATTAN', 1: 'EUCLIDIAN', 2: 'MAX_DELTA', 3: 'DIJKSTRA'}
        self.tiebreaker = None
        # a_star important pars:
        self.start_node = None
        self.end_node = None

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
                                                 self.tile_size - 2 * self.line_width,
                                                 self.tile_size - 2 * self.line_width, self.grid[y][x].colour)
        # HINTS:
        arcade.draw_text(f'Mode: {self.mode_names[self.mode]}', 25, SCREEN_HEIGHT - 25, arcade.color.BLACK, bold=True)
        arcade.draw_text(
            f'A* iters: {self.iterations}, path length: {self.path_length}, nodes visited: {len(self.nodes_visited)}, time elapsed: {self.time_elapsed_ms}',
            295, SCREEN_HEIGHT - 25, arcade.color.BROWN, bold=True)
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
        arcade.draw_rectangle_outline(SCREEN_WIDTH - 225, SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * 3 - 18 * 3 - 30, 18,
                                      18, arcade.color.BLACK, 2)
        arcade.draw_text(f'VECTOR_CROSS', SCREEN_WIDTH - 225 + (18 + 2 * 2),
                         SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * 3 - 18 * 3 - 30 - 6, arcade.color.BLACK, bold=True)

        if self.tiebreaker:
            arcade.draw_rectangle_filled(SCREEN_WIDTH - 225, SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * 3 - 18 * 3 - 30, 14,
                                          14, arcade.color.BLACK)

    def update(self, delta_time: float):
        # game logic and movement mechanics lies here:
        ...

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
        if SCREEN_WIDTH - 225 - 9 <= x <= SCREEN_WIDTH - 225 + 9 and SCREEN_HEIGHT - 100 - (
                18 + 2 * 2 + 18) * 3 - 18 * 3 - 30 - 9 <= y <= SCREEN_HEIGHT - 100 - (18 + 2 * 2 + 18) * 3 - 18 * 3 - 30 + 9:
                self.tiebreaker = None if self.tiebreaker else 1
        self.building_walls_flag = True
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.build_or_erase = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.build_or_erase = False
        if self.mode == 1:
            sn = self.get_node(x, y)
            if sn:
                if self.start_node: self.start_node.colour = None
                sn.colour = arcade.color.GREEN
                self.start_node = sn
        if self.mode == 2:
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

    def __init__(self, y, x, val, passability=True):
        self.y, self.x = y, x
        self.val = val
        self.passability = passability
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one
        # cost and heuristic vars:
        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        self.cross_deviation = 0
        # f = h + g or total cost of the current Node is not needed here
        # visual options:
        self.colour = None
        # heur dict:
        self.heuristics = {0: self.manhattan_distance, 1: self.euclidian_distance, 2: self.max_delta,
                           3: self.no_heuristic}
        self.tiebreakers = {0: self.vector_cross_product_deviation}

    def __eq__(self, other: 'Node'):
        return (self.y, self.x) == (other.y, other.x)

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other: 'Node'):
        return (self.g + self.h, self.cross_deviation) < (
            other.g + other.h, other.cross_deviation)  # the right sigh is "<" for __lt__() method

    def __hash__(self):
        return hash((self.y, self.x))

    def clear(self):
        self.heur_clear()
        self.passability = True
        self.colour = None

    def heur_clear(self):
        self.g = np.Infinity
        self.h = 0
        self.cross_deviation = 0
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
    def vector_cross_product_deviation(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    def get_neighs(self, game: 'Astar') -> list['Node']:
        for dy, dx in self.walk:
            ny, nx = self.y + dy, self.x + dx
            if 0 <= ny < game.tiles_q and 0 <= nx < game.hor_tiles_q:
                if game.grid[ny][nx].passability:
                    yield game.grid[ny][nx]

    def a_star(self, other: 'Node', game: 'Astar'):
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
            if curr_node == other:
                break
            # next step:
            for neigh in curr_node.get_neighs(game):
                if neigh.g > curr_node.g + neigh.val:
                    neigh.g = curr_node.g + neigh.val
                    neigh.h = neigh.heuristics[game.heuristic](neigh, other)
                    if game.tiebreaker:
                        curr_dir = neigh.y - self.y, neigh.x - self.x
                        goal_dir = other.y - neigh.y, other.x - neigh.x
                        neigh.cross_deviation = abs(self.vector_cross_product_deviation(curr_dir, goal_dir))
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
