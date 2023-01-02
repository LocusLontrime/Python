def three_dots(game_map):  # 36 366 98 989 LL
    pass


class Triplet:
    # movement constants:
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    NAMES = ['→', '↓', '←', '↑']

    def __init__(self, game_map):
        self.grid, self.dots, self.goals = self.make_grid_from_blueprint(game_map)
        print(f'DOTS: {self.dots}')
        print(f'GOALS: {self.goals}')
        self.Y, self.X = len(self.grid), len(self.grid[0])
        self.stop_flag = False
        self.solution = None
        self.backtracking_iters = 0

    def solve(self):
        self.backtracking('', set())
        # print(f'THE WAY: {self.solution}')
        return self.solution

    def show_triplet(self):
        for row in self.grid:
            for cell in row:
                if cell in self.dots.values():
                    if cell == self.dots[0]:
                        print(f'R', end='')
                    elif cell == self.dots[1]:
                        print(f'G', end='')
                    else:
                        print(f'Y', end='')
                elif cell in self.goals.values():
                    if cell == self.goals[0]:
                        print(f'r', end='')
                    elif cell == self.goals[1]:
                        print(f'g', end='')
                    else:
                        print(f'y', end='')
                elif cell.passability:
                    print(f' ', end='')
                else:
                    print(f'*', end='')
            print()
        print()

    def get_next_moves(self):
        # all 4 moves:
        new_triplets = []
        for ind, move in enumerate(self.MOVES):
            # try to move every dot:
            new_dots = {}
            for key in self.dots.keys():
                new_dot = self.dots[key].move(self, move)
                new_dots[key] = new_dot
            new_triplets.append((new_dots, self.NAMES[ind]))
        return new_triplets

    def check(self) -> bool:
        for key in self.dots.keys():
            if self.dots[key] != self.goals[key]:
                return False
        return True

    def __str__(self):
        return str(self.dots.values())

    def __repr__(self):
        return str(self) + ' '

    def __hash__(self) -> int:
        # print(f'dict: {self.dots}')
        t = tuple(self.dots[key] for key in self.dots.keys())
        # print(f'hashable: {t}')
        return hash(t)

    def backtracking(self, steps: str, visited_states: set[int]):
        if not self.stop_flag and len(visited_states) < 32:
            self.backtracking_iters += 1
            if self.backtracking_iters % 10000 == 0:
                print(f'{self.backtracking_iters}-th iteration of backtracking: ')
                print(f'TRIPLET STATE: {self}')
                self.show_triplet()
            # base case of finding solution:
            if self.check():
                print(f'SOLUTION FOUND!!!')
                self.stop_flag = True
                self.solution = steps
                return
            # looking for next possible moves:
            new_triplets = self.get_next_moves()
            # print(f'new triplets: {len(new_triplets)}')
            current_dots = self.dots.copy()
            new_triplets = sorted(new_triplets, key=lambda x: sum([x[0][key].manhattan_distance(self.goals[key]) for key in x[0].keys()]))
            for new_triplet, move in new_triplets:
                # new step:
                self.dots = new_triplet
                # recurrent_relation:
                h = hash(self)
                # print(f'hash: {h}')
                if h not in visited_states:
                    self.backtracking(steps + move, visited_states | {h})
                # backtracking:
                self.dots = current_dots

    @staticmethod
    def make_grid_from_blueprint(game_map: str):
        grid = []
        start_dots, end_dots = {}, {}
        for y, row in enumerate(game_map.split('\n')[1:-1]):
            grid.append([])
            for x, s in enumerate(row[1:-1]):
                if s in (l := ['R', 'G', 'Y']):
                    cell = Cell(y, x)
                    start_dots[l.index(s)] = cell
                elif s in (l := ['r', 'g', 'y']):
                    cell = Cell(y, x)
                    end_dots[l.index(s)] = cell
                elif s == '*':
                    cell = Cell(y, x, False)
                else:
                    # space ' ' case:
                    cell = Cell(y, x)
                grid[y].append(cell)
        return grid, start_dots, end_dots


class Cell:
    def __init__(self, y, x, passability=True):
        self.y, self.x = y, x
        self.passability = passability

    def move(self, triplet: 'Triplet', move: tuple[int, int]) -> 'Cell' or None:
        new_y, new_x = self.y + move[0], self.x + move[1]
        if 0 <= new_y < triplet.Y and 0 <= new_x < triplet.X:
            if (nc := triplet.grid[new_y][new_x]).passability and nc not in triplet.dots:
                return nc
        return self

    def manhattan_distance(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def __eq__(self, other):
        # print(f'SELF: {self}')
        # print(f'OTHER: {other}')
        # print(f'SELF == OTHER: {(self.y, self.x) == (other.y, other.x)}')
        return (self.y, self.x) == (other.y, other.x)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.y, self.x))

    def __str__(self):
        return str((self.y, self.x))

    def __repr__(self):
        return str(self)

    def a_star_variation(self):
        pass


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

print(f'game map: ')
for string in field:
    print(f'{string}')
Triplet(field[0]).solve()

hash(())

print(f'{None and 98}')
