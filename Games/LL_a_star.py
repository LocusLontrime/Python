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


class Astar(arcade.Window):
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
        self.time_elapsed_ms = 0
        self.grid = [[Node(j, i, 1) for i in range(self.hor_tiles_q)] for j in range(self.tiles_q)]
        # interactions:
        self.building_walls_flag = False
        self.mode = 0  # 0 for building the walls when 1 for erasing them afterwards, 2 for a start node choosing and 3 for a end one...
        self.mode_names = {0: 'BUILDING', 1: 'ERASING', 2: 'START NODE CHOOSING', 3: 'END NODE CHOOSING'}
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
            f'A* iters: {self.iterations}, nodes visited: {len(self.nodes_visited)}, time elapsed: {self.time_elapsed_ms}',
            295, SCREEN_HEIGHT - 25, arcade.color.BROWN, bold=True)

    def update(self, delta_time: float):
        # game logic and movement mechanics lies here:
        ...

    def clear_nodes(self):
        # clearing the every node:
        for row in self.grid:
            for node in row:
                node.clear()
        # clearing the nodes-relating pars of the game:
        self.start_node, self.end_node = None, None

    def on_key_press(self, symbol: int, modifiers: int):
        # is called when user press the symbol key:
        match symbol:
            # a_star_call:
            case arcade.key.SPACE:
                if self.start_node and self.end_node:
                    start = time.time_ns()
                    the_shortest_path = self.start_node.a_star(self.end_node, self)
                    finish = time.time_ns()
                    self.time_elapsed_ms = self.get_ms(start, finish)
                    for node in the_shortest_path:
                        if node not in [self.start_node, self.end_node]:
                            node.colour = arcade.color.RED
            # grid clearing:
            case arcade.key.ENTER:
                self.clear_nodes()
            # heuristic change:

    def get_node(self, mouse_x, mouse_y):
        x_, y_ = mouse_x - 5, mouse_y - 5
        x, y = x_ // self.tile_size, y_ // self.tile_size
        return self.grid[y][x] if 0 <= x < self.hor_tiles_q and 0 <= y < self.tiles_q else None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.building_walls_flag:
            if self.mode == 0:
                n = self.get_node(x, y)
                if n:
                    n.passability = False
                    n.colour = arcade.color.BLACK
            elif self.mode == 1:
                n = self.get_node(x, y)
                if n:
                    n.passability = True
                    n.colour = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.building_walls_flag = True
        if self.mode == 2:
            if self.start_node: self.start_node.colour = None
            sn = self.get_node(x, y)
            sn.colour = arcade.color.GREEN
            self.start_node = sn
        if self.mode == 3:
            if self.end_node: self.end_node.colour = None
            en = self.get_node(x, y)
            en.colour = arcade.color.BLUE
            self.end_node = en

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.mode = (self.mode + 1) % 4

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
        # f = h + g or total cost of the current Node is not needed here
        # visual options:
        self.colour = None

    def __eq__(self, other: 'Node'):
        return (self.y, self.x) == (other.y, other.x)

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other: 'Node'):
        return self.g + self.h < other.g + other.h  # the right sigh is "<" for __lt__() method

    def __hash__(self):
        return hash((self.y, self.x))

    def clear(self):
        self.g = np.Infinity
        self.h = 0
        self.passability = True

        self.previously_visited_node = None
        self.colour = None

    def manhattan_distance(self, other: 'Node'):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def get_neighs(self, game: 'Astar') -> list['Node']:
        for dy, dx in self.walk:
            ny, nx = self.y + dy, self.x + dx
            if 0 <= ny < game.tiles_q and 0 <= nx < game.hor_tiles_q:
                if game.grid[ny][nx].passability:
                    yield game.grid[ny][nx]

    def a_star(self, other: 'Node', game: 'Astar'):
        game.iterations = 0
        nodes_to_be_visited = [self]
        self.g = 0
        hq.heapify(nodes_to_be_visited)
        # the main cycle:
        while nodes_to_be_visited:
            game.iterations += 1
            curr_node = hq.heappop(nodes_to_be_visited)
            game.nodes_visited.add(curr_node)
            curr_node.colour = arcade.color.ROSE
            # base case of finding the shortest path:
            if curr_node == other:
                break
            # next step:
            for neigh in curr_node.get_neighs(game):
                if neigh.g > curr_node.g + neigh.val:
                    neigh.g = curr_node.g + neigh.val
                    neigh.h = neigh.manhattan_distance(other)
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
