def three_dots(game_map):
    pass

class Triplet:
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def __init__(self, dots: list[tuple[int, int]], game_map):
        self.grid, self.dots, self.goals = self.make_grid_from_blueprint(game_map)
        self.Y, self.X = len(self.grid), len(self.grid[0])

    def get_next_moves(self):
        # all 4 moves:
        new_triplets = []
        for move in self.MOVES:
            # try to move every dot:
            new_dots = []
            for key in self.dots.keys():
                new_dot = self.dots[key].move(self, move)
                if new_dot:
                    new_dots.append(new_dot)
                else: break
            else: new_triplets.append(new_dots)
        return new_triplets
    def check(self):
        pass

    def __str__(self):
        return str(self.dots.values())

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.dots)

    def a_star_variation(self):
        pass

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
        return None

    def __eq__(self, other):
        pass

    def __hash__(self):
        return hash((self.y, self.x))

    def __str__(self):
        return str((self.y, self.x))

    def __repr__(self):
        return str(self)

    def a_star_variation(self):
        pass


field = ["+------------+\n"
     + "|R    *******|\n"
     + "|G    *******|\n"
     + "|Y    *******|\n"
     + "|            |\n"
     + "|           r|\n"
     + "|******     g|\n"
     + "|******     y|\n"
     + "+------------+"]


print(f'game map: ')
for string in field:
    print(f'{string}')

print(f'solution: {three_dots(field)}')

