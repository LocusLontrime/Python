# acc
import math
from collections import defaultdict as d


class Blobservation:
    def __init__(self, h: int, w: int = None):
        # initial pars:
        self.h = h
        self.w = h if w is None else w
        # core pars:
        self.blobs: dict[tuple[int, int], Blob] = dict()
        self.turn = 0
        # aux pars:
        self.smallest_blob = None

    def populate(self, population: list[dict[str, int]]) -> None:
        # validation:
        for new_blob_dict in population:
            if 'x' not in new_blob_dict.keys() or 'y' not in new_blob_dict.keys() or 'size' not in new_blob_dict.keys():
                raise Exception(f'No x, y or size par in one of dicts...')
            if (isinstance(new_blob_dict['x'], bool) or isinstance(new_blob_dict['y'], bool) or isinstance(
                    new_blob_dict['size'], bool) or
                new_blob_dict['x'] < 0 or new_blob_dict['x'] >= self.h or new_blob_dict['y'] < 0 or new_blob_dict[
                    'y'] >= self.w) or new_blob_dict['size'] < 0:
                raise Exception(f'Invalid data types...')

        for new_blob_dict in population:
            y, x = new_blob_dict['x'], new_blob_dict['y']
            new_blob = Blob(y, x, new_blob_dict['size'])
            if (y, x) in self.blobs.keys():
                self.blobs[(y, x)].consume(new_blob)
            else:
                self.blobs[(y, x)] = new_blob

    def move(self, moves: int = 1) -> None:
        print(f'{moves = }')
        # validation:
        if isinstance(moves, bool) or moves <= 0:
            raise Exception(f'Invalid moves...')

        for i in range(moves):
            # print(f'{i}th move: ')
            if len(self.blobs) == 1:
                return
            moves_list: d[tuple[int, int], list] = d(list)
            for blob in self.blobs.values():
                if blob.size != min(b.size for b in self.blobs.values()):
                    # print(f'moving the blob: {blob}')
                    y_, x_ = blob.compute_move(self.blobs)
                    # print(f'->{y_, x_ = }')
                    moves_list[y_, x_].append(blob)
                else:
                    moves_list[blob.y, blob.x].append(blob)
            # print(f'{moves_list = }')
            # new blobs dict building:
            self.blobs = {(y_, x_): Blob(y_, x_, sum(blob.size for blob in moves_list[y_, x_])) for y_, x_ in
                          moves_list.keys()}

    def print_state(self) -> list[list[int]]:
        blobs = [[blob.y, blob.x, blob.size] for blob in self.blobs.values()]
        blobs.sort(key=lambda blob: (blob[0], blob[1]))
        return blobs


class Blob:
    def __init__(self, y: int, x: int, size: int):
        self.y = y
        self.x = x
        self.size = size

    def compute_move(self, blobs: dict[tuple[int, int], 'Blob']) -> tuple[int, int]:
        prey = self.find_prey(blobs)
        dy, dx = self.choose_dir(prey)
        return self.y + dy, self.x + dx

    def consume(self, other: 'Blob'):
        """consuming and fusing lies here..."""
        self.size += other.size

    def find_prey(self, blobs: dict[tuple[int, int], 'Blob']) -> 'Blob':
        def angle_key(blob):
            """sorts blobs clockwise..."""
            k = math.atan2(blob.x - self.x, -(blob.y - self.y))
            return 180 * (2 * math.pi + k if k < 0 else k) / math.pi

        # let us find the nearest blob excluding the blob itself:
        # targetable blobs (their sizes < self.size):
        targets = [blob for blob in blobs.values() if (blob != self and blob.size < self.size)]
        best_distance_blob = min(targets, key=lambda blob: max(abs(self.y - blob.y), abs(self.x - blob.x)))
        # searching for all the best blobs-preys in terms of distance::
        best_distance = max(abs(self.y - best_distance_blob.y), abs(self.x - best_distance_blob.x))
        # print(f'...{best_distance = }')
        possible_preys = [blob for blob in targets if max(abs(self.y - blob.y), abs(self.x - blob.x)) == best_distance]
        # print(f'...1{possible_preys = }')
        # now let us separate the biggest ones:
        best_size_blob = max(possible_preys, key=lambda blob: blob.size)
        best_size = best_size_blob.size
        # print(f'...{best_size = }')
        possible_preys = [blob for blob in possible_preys if blob.size == best_size]
        # print(f'...2{possible_preys = }')
        # if we have more than one blob -> we should choose the on that lies nearest to 12 o'clock in clockwise rotation...
        best_angle_blob = min(possible_preys, key=angle_key)
        best_angle = angle_key(best_angle_blob)
        # print(f'...{best_angle = }')
        possible_preys = [blob for blob in possible_preys if angle_key(blob) == best_angle]
        # print(f'...3{possible_preys = }')
        # return the best prey -> it must be the one...
        return possible_preys.pop()

    def choose_dir(self, prey: 'Blob') -> tuple[int, int]:
        """choose the one cell from the moor neighbourhood..."""
        dy, dx = prey.y - self.y, prey.x - self.x
        return (-1 if dy < 0 else 1) if dy != 0 else 0, (-1 if dx < 0 else 1) if dx != 0 else 0

    # just for testing:
    def __str__(self):
        return f'{self.y, self.x}[{self.size}]'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x and self.size == other.size


# blob_ = Blob(98, 989, 98989)

# too smart atan...
print(f'{180 * math.atan2(1, 0) / math.pi}')
print(f'{180 * math.atan2(0, 1) / math.pi}')
print(f'{180 * math.atan2(-1, 0) / math.pi}')
print(f'{180 * math.atan2(0, -1) / math.pi}')
print(f'{180 * math.atan2(3, -3) / math.pi}')
print(f'{180 * math.atan2(-3, 3) / math.pi}')

generation0 = [
    {'x': 0, 'y': 4, 'size': 3},
    {'x': 0, 'y': 7, 'size': 5},
    {'x': 2, 'y': 0, 'size': 2},
    {'x': 3, 'y': 7, 'size': 2},
    {'x': 4, 'y': 3, 'size': 4},
    {'x': 5, 'y': 6, 'size': 2},
    {'x': 6, 'y': 7, 'size': 1},
    {'x': 7, 'y': 0, 'size': 3},
    {'x': 7, 'y': 2, 'size': 1}
]

generation1 = [
    {'x': 3, 'y': 6, 'size': 3},
    {'x': 8, 'y': 0, 'size': 2},
    {'x': 5, 'y': 3, 'size': 6},
    {'x': 1, 'y': 1, 'size': 1},
    {'x': 2, 'y': 6, 'size': 2},
    {'x': 1, 'y': 5, 'size': 4},
    {'x': 7, 'y': 7, 'size': 1},
    {'x': 9, 'y': 6, 'size': 3},
    {'x': 8, 'y': 3, 'size': 4},
    {'x': 5, 'y': 6, 'size': 3},
    {'x': 0, 'y': 6, 'size': 1},
    {'x': 3, 'y': 2, 'size': 5}
]

gen = [{'x': False, 'y': 19, 'size': 17}, {'x': 6, 'y': 20, 'size': 3}, {'x': 17, 'y': 1, 'size': 11},
       {'x': 3, 'y': 7, 'size': 8}, {'x': 8, 'y': 5, 'size': 3}, {'x': 2, 'y': 0, 'size': 6},
       {'x': 0, 'y': 16, 'size': 12}, {'x': 8, 'y': 1, 'size': 17}, {'x': 9, 'y': 9, 'size': 7},
       {'x': 18, 'y': 12, 'size': 13}, {'x': 16, 'y': 13, 'size': 16}, {'x': 14, 'y': 4, 'size': 17},
       {'x': 20, 'y': 4, 'size': 16}, {'x': 4, 'y': 3, 'size': 9}, {'x': 16, 'y': 6, 'size': 12},
       {'x': 4, 'y': 12, 'size': 1}, {'x': 11, 'y': 13, 'size': 18}, {'x': 10, 'y': 9, 'size': 11},
       {'x': 15, 'y': 12, 'size': 14}, {'x': 14, 'y': 20, 'size': 2}, {'x': 10, 'y': 19, 'size': 7},
       {'x': 8, 'y': 11, 'size': 10}]

# blobs_ = Blobservation(8)
# blobs_.populate(generation0)
# blobs_.move()
# res = blobs_.print_state()
# print(f'{res = }')
# blobs_.move()
# res = blobs_.print_state()
# print(f'{res = }')
# blobs_.move(1000)
# res = blobs_.print_state()
# print(f'{res = }')

blobs_ = Blobservation(10, 8)

blobs_.populate(generation1)
# blobs_.populate(gen)
blobs_.move()
res = blobs_.print_state()
print(f'{res = }')
