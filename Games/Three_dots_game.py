# accepted on codewars.com
import heapq as hq
import time
import math
import numpy as np
# graphics:
import arcade

# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050
TILE_SIZE = 86


class ThreeDotsGame(arcade.Window):
    def __init__(self, width: int, height: int, game_map):
        super().__init__(width, height)
        # choosing the main background colour:
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        # initialization of important fields:
        self.grid, dots, goals = self.make_grid_from_blueprint(game_map)
        self.dots, self.goals = Triplet(list(dots[i] for i in range(len(dots)))), Triplet(
            list(goals[i] for i in range(len(goals))))
        self.Y, self.X = len(self.grid), len(self.grid[0])
        self.permission_of_movement = True

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
                                  TILE_SIZE * self.Y - self.dots.dots[0][0] * TILE_SIZE - TILE_SIZE // 2 + 10, 36,
                                  arcade.color.RED)
        arcade.draw_circle_filled(self.dots.dots[1][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                  TILE_SIZE * self.Y - self.dots.dots[1][0] * TILE_SIZE - TILE_SIZE // 2 + 10, 36,
                                  arcade.color.GREEN)
        arcade.draw_circle_filled(self.dots.dots[2][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                  TILE_SIZE * self.Y - self.dots.dots[2][0] * TILE_SIZE - TILE_SIZE // 2 + 10, 36,
                                  arcade.color.BRONZE_YELLOW)
        # goals:
        arcade.draw_rectangle_outline(self.goals.dots[0][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                      TILE_SIZE * self.Y - self.goals.dots[0][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                      TILE_SIZE, TILE_SIZE, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(self.goals.dots[1][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                      TILE_SIZE * self.Y - self.goals.dots[1][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                      TILE_SIZE, TILE_SIZE, arcade.color.GREEN, 5)
        arcade.draw_rectangle_outline(self.goals.dots[2][1] * TILE_SIZE + TILE_SIZE // 2 + 10,
                                      TILE_SIZE * self.Y - self.goals.dots[2][0] * TILE_SIZE - TILE_SIZE // 2 + 10,
                                      TILE_SIZE, TILE_SIZE, arcade.color.BRONZE_YELLOW, 5)
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
                case arcade.key.ESCAPE:
                    arcade.finish_render()
                    self.close()
            # case of winning the game:
            if self.dots.check(self):
                arcade.draw_text('YOU WON!!!', 1920 // 2, 800)
                self.permission_of_movement = False


class Triplet:
    # movement constants:
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    NAMES = ['R', 'D', 'L', 'U']  # ['→', '↓', '←', '↑']

    def __init__(self, dots: list[tuple[int, int], ...]):
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

    def move(self, game: 'ThreeDotsGame', move: tuple[int, int]) -> None:
        new_dots = list(self.move_dot(self.dots[i], game, move) for i in range(len(self.dots)))
        collision_counter = 0
        for new_dot in new_dots:
            if new_dot in self.dots: collision_counter += 1
        if collision_counter < len(self.dots):
            for j in range(len(self.dots) - 1):
                for i in range(j + 1, len(self.dots)):
                    if new_dots[j] == new_dots[i]:
                        new_dots[j], new_dots[i] = self.dots[j], self.dots[i]
            self.dots = new_dots[:]

    @staticmethod
    def move_dot(dot: tuple[int, int], game: 'ThreeDotsGame', move: tuple[int, int]) -> tuple[int, int]:
        ny, nx = dot[0] + move[0], dot[1] + move[1]
        if 0 <= ny < game.Y and 0 <= nx < game.X:
            if game.grid[ny][nx][2]:
                return ny, nx
        return dot

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


def main():
    game = ThreeDotsGame(SCREEN_WIDTH, SCREEN_HEIGHT, game_map_y[0])
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

# Finishing rendering and showing the result:
arcade.finish_render()
# Until the user press 'Esc' button the window will be opened:
arcade.run()
