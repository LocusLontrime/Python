# accepted on codewars.com (5-7 seconds, can be optimized a bit)
import heapq as hq
import time
import math
import numpy as np


def three_dots(game_map):  # 36 366 98 989 LL
    return ThreeDotsGame(game_map).solve()


class ThreeDotsGame:
    BOLD = "\033[1m"
    RED = "\033[31m{}"
    GREEN = "\033[32m{}"
    YELLOW = "\033[33m{}"
    END = "\033[0m"

    def __init__(self, game_map):
        self.grid, in_dots, goals = self.make_grid_from_blueprint(game_map)
        self.in_dots, self.goals = tuple(in_dots[i] for i in range(3)), tuple(goals[i] for i in range(3))
        print(f'INITIALS: {self.in_dots}')
        print(f'GOALS: {self.goals}')
        self.Y, self.X = len(self.grid), len(self.grid[0])
        self.a_star_iters = 0

    def solve(self):
        return self.a_star_var()

    # from INITIALS -->> GOALS:
    def a_star_var(self):
        initials = Triplet(self.in_dots)
        triplets_state_dict = {self.in_dots: initials}
        triplets_state_dict: dict[tuple[tuple[int, int], ...], 'Triplet']  # checking...
        triplets_to_be_visited = [initials]
        initials.g = 0
        hq.heapify(triplets_to_be_visited)
        goals = Triplet(self.goals)
        triplets_state_dict[self.goals] = goals
        # core of a-star variation:
        while triplets_to_be_visited:
            self.a_star_iters += 1
            curr_triplet = hq.heappop(triplets_to_be_visited)
            # print(f'iter: {self.a_star_iters}, curr_triplet: {curr_triplet}')
            # self.show_triplet(curr_triplet)
            if curr_triplet == goals:
                print(f'SOLUTION BEEN FOUND!')
                break
            # next step of a-star:
            for new_coords, move in curr_triplet.get_next_moves(self):
                # kind of memoization:
                if new_coords not in triplets_state_dict.keys():
                    # print(f'new_coords: {new_coords}')
                    # print(f'move: {move}')
                    triplets_state_dict[new_coords] = Triplet(new_coords)
                new_triplet = triplets_state_dict[new_coords]
                # dynamic programming and length minimization:
                if new_triplet.g > curr_triplet.g + 1:
                    new_triplet.g = curr_triplet.g + 1
                    new_triplet.h = new_triplet.manhattan_heuristic(goals)
                    new_triplet.aux_h = new_triplet.aux(goals)
                    new_triplet.previously_visited_state = curr_triplet
                    new_triplet.direction = move
                    hq.heappush(triplets_to_be_visited, new_triplet)
        # the first cell for path-restoring (from the end):
        triplet = goals
        triplets, the_way = [], ''
        # path restoring (here we get the reversed path):
        while triplet.previously_visited_state:
            triplets.append(triplet)
            the_way += triplet.direction
            triplet = triplet.previously_visited_state
        # info:
        print(f'dict length: {len(triplets_state_dict)}')
        print(f'A* iterations: {self.a_star_iters}')
        print(f'Showing the road: ')
        triplets = triplets[::-1]
        print()
        for i, triplet in enumerate(triplets):
            print(f'{i}th step: ')
            self.show_triplet(triplet)
            # time.sleep(0.5)
        # returning the reversed shortest path:
        return the_way[::-1]

    def show_triplet(self, triplet: 'Triplet'):
        print(f'{self.get_border(self.X)}')
        for row in self.grid:
            print(f'|', end='')
            for cell in row:
                c = cell[:2]
                if c in triplet.dots:
                    if c == triplet.dots[0]:
                        self.colour_print('R', self.RED)
                    elif c == triplet.dots[1]:
                        self.colour_print('G', self.GREEN)
                    else:
                        self.colour_print('Y', self.YELLOW)
                elif c in self.goals:
                    if c == self.goals[0]:
                        self.colour_print('r', self.RED)
                    elif c == self.goals[1]:
                        self.colour_print('g', self.GREEN)
                    else:
                        self.colour_print('y', self.YELLOW)
                elif cell[2]:
                    print(f' ', end='')
                else:
                    print(f'*', end='')
            print(f'|')
        print(f'{self.get_border(self.X)}')
        print()

    @staticmethod
    def get_border(length):
        return f"+{'-' * length}+"

    def colour_print(self, char, colour):
        print(f"{(self.BOLD + colour + self.END).format(char)}", end='')

    @staticmethod
    def make_grid_from_blueprint(game_map: str):
        grid = []
        start_dots, end_dots = {}, {}
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


class Triplet:
    # movement constants:
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    NAMES = ['R', 'D', 'L', 'U']  # ['→', '↓', '←', '↑']

    def __init__(self, dots: tuple[tuple[int, int], ...]):
        self.dots = dots
        # a star vars:
        self.g = np.Infinity
        self.h = 0
        self.aux_h = 0
        # path-restoring vars:
        self.previously_visited_state = None
        self.direction = None

    def get_next_moves(self, game: 'ThreeDotsGame'):
        # all 4 moves:
        new_triplets = []
        for ind, move in enumerate(self.MOVES):
            # try to move every dot:
            new_dots = list(self.move_cell(self.dots[i], game, move) for i in range(len(self.dots)))
            collision_counter = 0
            for new_dot in new_dots:
                if new_dot in self.dots: collision_counter += 1
            if collision_counter < len(self.dots):
                for j in range(len(self.dots) - 1):
                    for i in range(j + 1, len(self.dots)):
                        if new_dots[j] == new_dots[i]:
                            new_dots[j], new_dots[i] = self.dots[j], self.dots[i]
                new_triplets.append((tuple(new_dots), self.NAMES[ind]))
        return new_triplets

    @staticmethod
    def move_cell(cell: tuple[int, int], game: 'ThreeDotsGame', move: tuple[int, int]) -> tuple[int, int]:
        ny, nx = cell[0] + move[0], cell[1] + move[1]
        if 0 <= ny < game.Y and 0 <= nx < game.X:
            if game.grid[ny][nx][2]:
                return ny, nx
        return cell

    @staticmethod
    def manhattan_distance(cell1: tuple[int, int], cell2: tuple[int, int]):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

    def __eq__(self, other: 'Triplet'):
        for i, cell in enumerate(self.dots):
            if cell != other.dots[i]: return False
        return True

    # it must be implemented for working with priority queues/heaps:
    def __lt__(self, other):
        # return self.g + self.h + self.aux_h < other.g + other.h + other.aux_h  # -->> for optimal solution
        return self.h + self.aux_h < other.h + other.aux_h  # -->> for faster one (in general, not in every case)...

    def manhattan_heuristic(self, other: 'Triplet') -> int:
        return max(self.manhattan_distance(self.dots[i], other.dots[i]) for i in range(len(self.dots)))

    def aux(self, other: 'Triplet') -> int:
        return sum(abs(self.manhattan_distance(self.dots[j], self.dots[i]) - other.manhattan_distance(other.dots[j],
                                                                                                      other.dots[i]))
                   for j in range(len(self.dots) - 1) for i in range(j + 1, len(self.dots)))

    def __str__(self):
        return str(self.dots)

    def __repr__(self):
        return str(self) + ' '


field1 = ["+------------+\n"
          + "|R    *******|\n"
          + "|G    *******|\n"
          + "|Y    *******|\n"
          + "|            |\n"
          + "|           r|\n"
          + "|******     g|\n"
          + "|******     y|\n"
          + "+------------+"]

field2 = ["+------------+\n"
          + "|R           |\n"
          + "|G    **     |\n"
          + "|Y    **     |\n"
          + "|            |\n"
          + "|     **    r|\n"
          + "|     **    g|\n"
          + "|           y|\n"
          + "+------------+"]

field = ["+------------+\n"
          + "|R     ** ***|\n"
          + "|G     ** ***|\n"
          + "|Y           |\n"
          + "|            |\n"
          + "|            |\n"
          + "|            |\n"
          + "|           g|\n"
          + "|** ***     r|\n"
          + "|** ***     y|\n"
          + "+------------+"]

field4 = ["+------------+\n"
          + "|RGY         |\n"
          + "|            |\n"
          + "|     **     |\n"
          + "|     **     |\n"
          + "|            |\n"
          + "|         rgy|\n"
          + "+------------+"]

field5 = ["+------------+\n"
          + "|R           |\n"
          + "|G           |\n"
          + "|Y    **     |\n"
          + "|     **    r|\n"
          + "|           g|\n"
          + "|           y|\n"
          + "+------------+"]

field6 = ["+------------+\n"
          + "|R           |\n"
          + "|G    **     |\n"
          + "|Y    **     |\n"
          + "|            |\n"
          + "|     **    r|\n"
          + "|     **    g|\n"
          + "|           y|\n"
          + "+------------+"]

field7 = ["+---------------+\n"
          + "|         g     |\n"
          + "|           r   |\n"
          + "|   **      y   |\n"
          + "|   **       RY |\n"
          + "|      *****   G|\n"
          + "|***   ***      |\n"
          + "|***      **    |\n"
          + "+---------------+"]

field8 = ["+---------------+\n"
          + "| YG            |\n"
          + "|    ***  * *   |\n"
          + "|  R ***  * *r y|\n"
          + "|        **** g |\n"
          + "|          **   |\n"
          + "|        ****   |\n"
          + "|               |\n"
          + "+---------------+"]

field9 = ["+---------------+\n"
         + "|               |\n"
         + "|   * *         |\n"
         + "|** * *   r     |\n"
         + "|** * *    y    |\n"
         + "|G Y* *   g     |\n"
         + "|R  * *   ***   |\n"
         + "|         ***   |\n"
         + "+---------------+"]

print(f'game map: ')
for string in field:
    print(f'{string}')
start = time.time_ns()
print(f'Solution: {three_dots(field[0])}')
finish = time.time_ns()
print(f'Time elapsed: {(finish - start) // 10 ** 6} milliseconds')
hash(())

print(f'{None and 98}')

# cells_set = {Cell(11, 98), Cell(11, 98)}
# print(f'{cells_set}')

tu = ((1, 1), (1, 1), (98, 989))
print(f'set: {set(tu)}')
