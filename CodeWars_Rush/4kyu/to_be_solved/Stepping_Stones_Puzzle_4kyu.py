import time  # accepted on codewars.com

rec_counter: int
place_counter: int

placement_time: int
unplacement_time: int


def first_impossible(stones: list[tuple[int, int]]):  # LL 36 366 98 989
    global rec_counter, place_counter, placement_time, unplacement_time

    rec_counter = 0
    place_counter = 0
    unplacement_time = 0
    placement_time = 0

    INIT_VAL = 1

    # dictionary of possible cells for the stones placements:
    neighs = dict()
    stones_placed = set(stones)
    possibles = dict()
    higher_vals = set()

    walk = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]
    print(f'walk: {walk}')

    def get_neighs(_y: int, _x: int, stones_placed_: set[tuple[int, int]]):
        for dy, dx in walk:
            y_, x_ = _y + dy, _x + dx
            if (y_, x_) not in stones_placed_:
                yield y_, x_

    def initialize_neighs():
        """initializes the initial placements for stones, using the 'stones' list"""
        for _y, _x in stones:
            # stones placement and memoization of stones have already been placed:
            place_stone(_y, _x, INIT_VAL)

    def place_stone(_y: int, _x: int, val: int):
        global place_counter
        place_counter += 1
        # as we are placing it we must remove the stone from the 'neighs' dict:
        if (_y, _x) in neighs.keys():
            neighs.pop((_y, _x))
        # so as it should be deleted from the possibles vals of the relative key:
        if val in possibles.keys() and (_y, _x) in possibles[val]:
            possibles[val].remove((_y, _x))
            if len(possibles[val]) == 0:
                possibles.pop(val)
        # and then add it to the stones_placed set
        stones_placed.add((_y, _x))
        # stone locating:
        neighbours = list(get_neighs(_y, _x, stones_placed))
        # print(f'neighbours {_y, _x} -->> {neighbours}')
        # neighbouring empty cells' val changing:
        for neigh_ in neighbours:
            # neighs dict updating:
            if neigh_ in neighs.keys():
                # changing possibles:
                possibles[neighs[neigh_]].remove(neigh_)
                if len(possibles[neighs[neigh_]]) == 0:
                    possibles.pop(neighs[neigh_])
                # neighs_ val updating:
                neighs[neigh_] += val
            else:
                neighs[neigh_] = val
            # reversed dict updating:
            if (k := neighs[neigh_]) in possibles.keys():
                possibles[k].add(neigh_)
            else:
                possibles[k] = {neigh_}

    def unplace_stone(_y: int, _x: int, val: int):
        # recovering the stone cell (adding it to the neighs):
        neighs[(_y, _x)] = val
        # rolling back the possibles' dict:
        if val in possibles.keys():
            possibles[val].add((_y, _x))
        else:
            possibles[val] = {(_y, _x)}
        # and then add it to the stones_placed set
        stones_placed.remove((_y, _x))
        # stone locating:
        neighbours = list(get_neighs(_y, _x, stones_placed))
        # print(f'neighbours {_y, _x} <<-- {list(reversed(neighbours))}')
        # now all the neighbouring empty cells' val changing backwards:
        for neigh_ in reversed(neighbours):
            # one step before reversed dict loading:
            possibles[neighs[neigh_]].remove(neigh_)
            if len(possibles[neighs[neigh_]]) == 0:
                possibles.pop(neighs[neigh_])
            # neighs_ val updating:
            neighs[neigh_] -= val
            if neighs[neigh_] == 0:
                neighs.pop(neigh_)
            # neighs dict updating (changing possibles):
            else:
                if neighs[neigh_] in possibles.keys():
                    possibles[neighs[neigh_]].add(neigh_)
                else:
                    possibles[neighs[neigh_]] = {neigh_}

    def recursive_seeker(val_: int, _y: int, _x: int):
        """seeks for all the game solving ways int order to define the highest value
         of the first stone that cannot be placed"""
        global rec_counter, placement_time, unplacement_time
        rec_counter += 1

        # time.sleep(0.5)

        # print(f'val: {val_}, (y, x): ({_y, _x})')

        # base case:
        if val_ not in possibles.keys():
            higher_vals.add(val_)
            return

        # cycling through all the available for stones placement cells with the val == val_:
        p = possibles[val_].copy()
        for y_, x_ in p:
            # print(f'(y_, x_): {y_, x_}')
            t1 = time.time_ns()
            # stone placement:
            place_stone(y_, x_, val_)
            t2 = time.time_ns()
            # recurrent relation:
            recursive_seeker(val_ + 1, y_, x_)
            t2_ = time.time_ns()
            # backtracking:
            unplace_stone(y_, x_, val_)
            t3 = time.time_ns()
            # time counting:
            placement_time += t2 - t1
            unplacement_time += t3 - t2_

    # at first, we initialize all data structures needed:
    initialize_neighs()

    print(f'stones_placed_: {stones_placed}')
    print(f'neighs_: {neighs}')
    print(f'possibles_: {possibles}')

    # secondly we start recursively seeking for the highest value implacable stone on all the possible ways of solving:
    recursive_seeker(INIT_VAL + 1, 0, 0)

    return max(higher_vals)


stones_ = [(0, 0), (2, -2)]  # [(8, 2), (1, 0), (2, 5), (0, 7), (3, 6), (6, 8)]
# [(0, 2), (3, 0), (5, 2)]  # [(0, 4), (1, 0), (4, 4)]  # [(0, 0), (2, 2)]
# [(1, 2), (3, 3)]  # [(0, 0), (1, 0)]  # [(0, 0), (0, 2)]  # [(0, 0), (0, 3)]  # [(0, 0), (2, -2)]

start = time.time_ns()
print(f'highest val: {first_impossible(stones_)}')
print(f'rec iters: {rec_counter}')
print(f'place iters: {place_counter}')
print(f'placement time: {placement_time // 10 ** 6} milliseconds')
print(f'unplacement time: {unplacement_time // 10 ** 6} milliseconds')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
