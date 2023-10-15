import time  # accepted on codewars.com

rec_counter: int


def first_impossible(stones: list[tuple[int, int]]):  # LL 36 366 98 989
    global rec_counter
    rec_counter = 0
    # initial value of the first stones placed:
    INIT_VAL = 1
    # dictionary of possible cells for the stones placements:
    neighs = dict()
    stones_placed = {stone: INIT_VAL for stone in stones}
    # current highest val for max stone value defining:
    highest_val = 0
    highest_stone_placement: dict[tuple[int, int]]
    # deltas for the neighs seeking:
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]

    def get_neighs(_y: int, _x: int):
        for dy, dx in walk:
            y_, x_ = _y + dy, _x + dx
            if (y_, x_) not in stones_placed.keys():
                yield y_, x_

    def initialize_neighs():
        """initializes the initial placements for stones, using the 'stones' list"""
        for _y, _x in stones:
            # stones placement and memoization of stones have already been placed:
            process_stone(_y, _x, INIT_VAL)

    def process_stone(_y: int, _x: int, val: int, is_reversed: bool = False):
        """place or stone or unplace it depending on the flag 'is_reversed'"""
        for neigh in get_neighs(_y, _x):
            if neigh in neighs.keys():
                neighs[neigh] += (-val if is_reversed else val)
                if neighs[neigh] == 0:
                    neighs.pop(neigh)
            else:
                neighs[neigh] = val
        if is_reversed:
            stones_placed.pop((_y, _x))
        else:
            stones_placed[(_y, _x)] = val

    def recursive_seeker(val_: int):
        """seeks for all the game solving ways int order to define the highest value
        of the first stone that cannot be placed"""
        global rec_counter
        rec_counter += 1
        nonlocal highest_val, highest_stone_placement
        # cells, that fits the current value of stone:
        possibles = [k for k, v in neighs.items() if v == val_ and k not in stones_placed.keys()]
        # cycling through all the available for stones placement cells with the v == val_:
        for y_, x_ in possibles:
            # stone placement:
            process_stone(y_, x_, val_)
            # recurrent relation:
            recursive_seeker(val_ + 1)
            # backtracking:
            process_stone(y_, x_, val_, True)
        else:
            if highest_val < val_:
                highest_val = val_
                highest_stone_placement = stones_placed.copy()

    # at first, we initialize all data structures needed:
    initialize_neighs()
    # secondly we start recursively seeking for the highest value implacable stone on all the possible ways of solving:
    recursive_seeker(INIT_VAL + 1)
    # best placement:
    print(f'stones:\n{sorted(highest_stone_placement.items(), key=lambda x: x[1])}')
    show_stones(highest_stone_placement)
    # returns the highest value among the higher ones:
    return highest_val


def show_stones(stones_placed_: dict[tuple[int, int]]):
    # decimal based system:
    BASE = 10
    print(f'\nplacement: ')
    min_j, max_j = min(_[0] for _ in stones_placed_.keys()), max(_[0] for _ in stones_placed_.keys())
    min_i, max_i = min(_[1] for _ in stones_placed_.keys()), max(_[0] for _ in stones_placed_.keys())
    grid = [['**' for _ in range(min_i, max_i + 1)] for _ in range(min_j, max_j + 1)]
    for (j, i), v in stones_placed_.items():
        print(f'(j, i), v: {(j, i), v}')
        grid[j][i] = f'0{v}' if v < BASE else f'{v}'
    print()
    for row in grid:
        print(f'{" ".join(row)}')


stones_ = [(8, 2), (1, 0), (2, 5), (0, 7), (3, 6), (6, 8)]  # [(0, 0), (2, -2)]
# [(0, 2), (3, 0), (5, 2)]  # [(0, 4), (1, 0), (4, 4)]  # [(0, 0), (2, 2)]
# [(1, 2), (3, 3)]  # [(0, 0), (1, 0)]  # [(0, 0), (0, 2)]  # [(0, 0), (0, 3)]  # [(0, 0), (2, -2)]

start = time.time_ns()
print(f'highest val: {first_impossible(stones_)}')
print(f'rec iters: {rec_counter}')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
