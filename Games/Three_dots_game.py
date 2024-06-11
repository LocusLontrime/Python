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


class ThreeDotsGame(arcade.Window):
    def __init__(self, width: int, height: int, game_map):
        global TILE_SIZE
        super().__init__(width, height)
        self.CURSOR_HAND = 'hand'
        # choosing the main background colour:
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        # initialization of important fields:
        self.grid, dots, goals = self.make_grid_from_blueprint(game_map)
        self.dots, self.goals = Triplet(tuple(dots[i] for i in range(len(dots)))), Triplet(
            tuple(goals[i] for i in range(len(goals))))
        self.Y, self.X = len(self.grid), len(self.grid[0])
        self.permission_of_movement = True
        self.tile_size = min((SCREEN_WIDTH - 30) / self.X, (SCREEN_HEIGHT - 25) / self.Y)
        TILE_SIZE = self.tile_size
        self.STEPS = 0
        self.HINT = ''
        self.a_star_iters = 0
        self.a_star_time_ms = 0

    @staticmethod
    def make_grid_from_blueprint(game_map: str):
        grid, start_dots, end_dots = [], {}, {}
        for y, row in enumerate(game_map.split('\n')[1:-1]):
            grid.append([])
            for x, s in enumerate(row[1:-1]):
                if s in (l := ['R', 'G', 'Y']):
                    cell = y, x, True
                    start_dots[l.index(s)] = cell[:2]
                elif s in (l := ['r', 'g', 'y']):
                    cell = y, x, True
                    end_dots[l.index(s)] = cell[:2]
                elif s == '*':
                    cell = y, x, False
                else:
                    cell = y, x, True
                grid[y].append(cell)
        return grid, start_dots, end_dots

    # from INITIALS -->> GOALS:
    def a_star_var(self):
        self.a_star_iters = 0
        triplets_state_dict = {self.dots.dots: self.dots}
        triplets_state_dict: dict[tuple[tuple[int, int], ...], 'Triplet']  # checking...
        triplets_to_be_visited = [self.dots]
        self.goals.clear()
        self.dots.g = 0  # nullifying of g-cost for a starting point
        hq.heapify(triplets_to_be_visited)
        triplets_state_dict[self.goals.dots] = self.goals
        # core of a-star variation:
        while triplets_to_be_visited:
            self.a_star_iters += 1
            curr_triplet = hq.heappop(triplets_to_be_visited)
            if curr_triplet == self.goals:
                print(f'SOLUTION BEEN FOUND!')
                break
            # next step of a-star:
            for new_coords, move in [(curr_triplet.move(self, m, False), Triplet.NAMES[i]) for i, m in
                                     enumerate(Triplet.MOVES)]:
                # kind of memoization:
                if new_coords not in triplets_state_dict.keys():
                    triplets_state_dict[new_coords] = Triplet(new_coords)
                new_triplet = triplets_state_dict[new_coords]
                # dynamic programming and length minimization:
                if new_triplet.g > curr_triplet.g + 1:
                    new_triplet.g = curr_triplet.g + 1
                    new_triplet.h = new_triplet.manhattan_heuristic(self.goals)
                    new_triplet.aux_h = new_triplet.aux(self.goals)
                    new_triplet.previously_visited_state = curr_triplet
                    new_triplet.direction = move
                    hq.heappush(triplets_to_be_visited, new_triplet)
        # the first cell for path-restoring (from the end):
        triplet = self.goals
        triplets, the_way = [], ''
        # path restoring (here we get the reversed path):
        while triplet.previously_visited_state:
            triplets.append(triplet)
            the_way += triplet.direction
            triplet = triplet.previously_visited_state
        # info:
        print(f'dict length: {len(triplets_state_dict)}')
        print(f'A* iterations: {self.a_star_iters}')
        triplets = triplets[::-1]
        # returning the reversed shortest path:
        return the_way[::-1]

    def get_hint(self):
        start = time.time_ns()
        self.HINT = self.a_star_var()
        finish = time.time_ns()
        self.a_star_time_ms = self.get_ms(start, finish)

    @staticmethod
    def get_ms(start, finish):
        return (finish - start) // 10 ** 6

    def setup(self):
        # game set up is located below:
        # sprites and etc...
        ...

    def on_draw(self):
        # renders this screen:
        arcade.start_render()
        # image's code:
        # border:
        arcade.draw_rectangle_outline(TILE_SIZE * self.X // 2 + 10, TILE_SIZE * self.Y // 2 + 10, TILE_SIZE * self.X,
                                      TILE_SIZE * self.Y, arcade.color.BLACK, 5)
        # cells:
        for j, row in enumerate(self.grid):
            for i, cell in enumerate(row):
                if cell[2]:
                    ...
                else:
                    arcade.draw_rectangle_filled(i * TILE_SIZE + TILE_SIZE // 2 + 10,
                                                 TILE_SIZE * self.Y - j * TILE_SIZE - TILE_SIZE // 2 + 10, TILE_SIZE,
                                                 TILE_SIZE, arcade.color.BLACK)
                    arcade.draw_rectangle_outline(i * TILE_SIZE + TILE_SIZE // 2 + 10,
                                                  TILE_SIZE * self.Y - j * TILE_SIZE - TILE_SIZE // 2 + 10, TILE_SIZE,
                                                  TILE_SIZE, arcade.color.DARK_GRAY, 5)
        # dots:
        arcade.draw_circle_filled(self.dots.dots[0][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                  TILE_SIZE * self.Y - self.dots.dots[0][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                  7 / 16 * TILE_SIZE,
                                  arcade.color.RED)
        arcade.draw_circle_filled(self.dots.dots[1][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                  TILE_SIZE * self.Y - self.dots.dots[1][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                  7 / 16 * TILE_SIZE,
                                  arcade.color.GREEN)
        arcade.draw_circle_filled(self.dots.dots[2][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                  TILE_SIZE * self.Y - self.dots.dots[2][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                  7 / 16 * TILE_SIZE,
                                  arcade.color.BRONZE_YELLOW)
        # goals:
        arcade.draw_rectangle_outline(self.goals.dots[0][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                      TILE_SIZE * self.Y - self.goals.dots[0][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                      TILE_SIZE - 5, TILE_SIZE - 5, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(self.goals.dots[1][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                      TILE_SIZE * self.Y - self.goals.dots[1][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                      TILE_SIZE - 5, TILE_SIZE - 5, arcade.color.GREEN, 5)
        arcade.draw_rectangle_outline(self.goals.dots[2][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                      TILE_SIZE * self.Y - self.goals.dots[2][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                      TILE_SIZE - 5, TILE_SIZE - 5, arcade.color.BRONZE_YELLOW, 5)

        arcade.draw_text(f'STEPS: {self.STEPS}', 25, SCREEN_HEIGHT - 15, arcade.color.BLACK, bold=True)
        arcade.draw_text(
            f'HINT ({Triplet.ALGOS_NAMES[Triplet.ALGO]}): {self.HINT}, A* iters: {self.a_star_iters}, time elapsed: {self.a_star_time_ms} ms',
            125, SCREEN_HEIGHT - 15,
            arcade.color.BLUE, bold=True)
        ...

    def update(self, delta_time: float):
        # game logic and movement mechanics lies here:
        ...

    def on_key_press(self, symbol: int, modifiers: int):
        # is called when user press the symbol key:
        if self.permission_of_movement:
            match symbol:
                case arcade.key.UP:
                    self.dots.move(self, (-1, 0))
                case arcade.key.RIGHT:
                    self.dots.move(self, (0, 1))
                case arcade.key.DOWN:
                    self.dots.move(self, (1, 0))
                case arcade.key.LEFT:
                    self.dots.move(self, (0, -1))
                case arcade.key.SPACE:
                    self.get_hint()
                case arcade.key.ENTER:
                    Triplet.ALGO = (Triplet.ALGO + 1) % len(Triplet.ALGOS)
                case arcade.key.ESCAPE:
                    arcade.finish_render()
                    self.close()
            # case of winning the game:
            if self.dots.check(self):
                self.permission_of_movement = False


class Triplet:
    # movement constants:
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    NAMES = ['R', 'D', 'L', 'U']  # ['→', '↓', '←', '↑']
    ALGOS = [0, 1, 2]
    ALGOS_NAMES = ['A*', 'Greedy', 'Dijkstra']
    ALGO = 0

    def __init__(self, dots: tuple[tuple[int, int], ...]):
        self.dots = dots
        # a star vars:
        self.g = np.Infinity
        self.h = 0
        self.aux_h = 0
        # path-restoring vars:
        self.previously_visited_state = None
        self.direction = None

    def __eq__(self, other: 'Triplet'):
        for i, cell in enumerate(self.dots):
            if cell != other.dots[i]: return False
        return True

    # just a manhattan distance between two dots of a Triplet:
    @staticmethod
    def manhattan_distance(cell1: tuple[int, int], cell2: tuple[int, int]):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

    # it must be implemented for working with priority queues/heaps:
    def __lt__(self, other):
        match self.ALGO:
            case 0: return self.g + self.h + self.aux_h < other.g + other.h + other.aux_h  # -->> for optimal solution
            case 1: return self.h + self.aux_h < other.h + other.aux_h  # -->> for faster one (in general, not in every case)...
            case 2: return self.g < other.g  # Dijkstra case, ver slow

    # clearing all the necessary a_star fields of the Triplet in order to make a_star_var() method work correctly when called sequentially:
    def clear(self):
        self.g = np.Infinity
        self.h = 0
        self.aux_h = 0

    # max manhattan distance between relative dots of current state and goal state:
    def manhattan_heuristic(self, other: 'Triplet') -> int:
        return max(self.manhattan_distance(self.dots[i], other.dots[i]) for i in range(len(self.dots)))

    # aux heuristic -->> current and goal states coherence's difference:
    def aux(self, other: 'Triplet') -> int:
        return sum(abs(self.manhattan_distance(self.dots[j], self.dots[i]) - other.manhattan_distance(other.dots[j],
                                                                                                      other.dots[i]))
                   for j in range(len(self.dots) - 1) for i in range(j + 1, len(self.dots)))

    # moves the current triplet in the direction chosen:
    def move(self, game: 'ThreeDotsGame', move: tuple[int, int], flag=True) -> None or tuple[tuple[int, int]]:
        new_dots = list(self.move_dot(self.dots[i], game, move) for i in range(len(self.dots)))
        collision_counter = 0
        for new_dot in new_dots:
            if new_dot in self.dots: collision_counter += 1
        if collision_counter < len(self.dots):
            for j in range(len(self.dots) - 1):
                for i in range(j + 1, len(self.dots)):
                    if new_dots[j] == new_dots[i]:
                        new_dots[j], new_dots[i] = self.dots[j], self.dots[i]
            if flag:
                self.dots = tuple(new_dots[:])
                game.STEPS += 1
                return
        return tuple(new_dots)

    # finds the new coordinates of the point after moving it in the direction chosen:
    @staticmethod
    def move_dot(dot: tuple[int, int], game: 'ThreeDotsGame', move: tuple[int, int]) -> tuple[int, int]:
        ny, nx = dot[0] + move[0], dot[1] + move[1]
        if 0 <= ny < game.Y and 0 <= nx < game.X:
            if game.grid[ny][nx][2]:
                return ny, nx
        return dot

    # checks if the current Triplet state is the goal one:
    def check(self, game: 'ThreeDotsGame'):
        return self == game.goals


game_map_x = [
    "+---------------+\n"
    + "|*              |\n"
    + "|   y r  ***    |\n"
    + "|     g*****    |\n"
    + "|      **       |\n"
    + "|  ***        R |\n"
    + "|  ******       |\n"
    + "|     ***    YG |\n"
    + "+---------------+"
]

game_map_y = [
    "+------------+\n"
    + "|R           |+\n"
    + "|G    **     |+\n"
    + "|Y    **     |+\n"
    + "|            |+\n"
    + "|     **    r|+\n"
    + "|     **    g|+\n"
    + "|           y|+\n"
    + "+------------+"
]

# a_star smart check from LarryAtGU on codewars.com:
game_map_z = [
    "+--+\n"
    + "|R |\n"
    + "| r|\n"
    + "|**|\n"
    + "|Gg|\n"
    + "|Yy|\n"
    + "+--+"
]


def main():
    game = ThreeDotsGame(SCREEN_WIDTH, SCREEN_HEIGHT, game_map_z[0])
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
