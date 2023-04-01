import time  # accepted on codewars.com

rec_counter: int


def first_impossible(stones: list[tuple[int, int]]):  # LL 36 366 98 989
    global rec_counter
    rec_counter = 0
    # initial value of the first stones placed:
    INIT_VAL = 1
    # dictionary of possible cells for the stones placements:
    neighs = dict()
    stones_placed = set(stones)
    higher_vals = set()
    # deltas for the neighs seeking:
    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]

    def get_neighs(_y: int, _x: int):
        for dy, dx in walk:
            y_, x_ = _y + dy, _x + dx
            if (y_, x_) not in stones_placed:
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
            stones_placed.remove((_y, _x))
        else:
            stones_placed.add((_y, _x))

    def recursive_seeker(val_: int):
        """seeks for all the game solving ways int order to define the highest value
        of the first stone that cannot be placed"""
        global rec_counter
        rec_counter += 1
        # cells, that fits the current value of stone:
        possibles = [k for k, v in neighs.items() if v == val_ and k not in stones_placed]
        # cycling through all the available for stones placement cells with the v == val_:
        for y_, x_ in possibles:
            # stone placement:
            process_stone(y_, x_, val_)
            # recurrent relation:
            recursive_seeker(val_ + 1)
            # backtracking:
            process_stone(y_, x_, val_, True)
        else:
            higher_vals.add(val_)
    # at first, we initialize all data structures needed:
    initialize_neighs()
    # secondly we start recursively seeking for the highest value implacable stone on all the possible ways of solving:
    recursive_seeker(INIT_VAL + 1)
    # returns the highest value among the higher ones:
    return max(higher_vals)


stones_ = [(8, 2), (1, 0), (2, 5), (0, 7), (3, 6), (6, 8)]  # [(0, 0), (2, -2)]
# [(0, 2), (3, 0), (5, 2)]  # [(0, 4), (1, 0), (4, 4)]  # [(0, 0), (2, 2)]
# [(1, 2), (3, 3)]  # [(0, 0), (1, 0)]  # [(0, 0), (0, 2)]  # [(0, 0), (0, 3)]  # [(0, 0), (2, -2)]

start = time.time_ns()
print(f'highest val: {first_impossible(stones_)}')
print(f'rec iters: {rec_counter}')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
