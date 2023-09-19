# accepted on codewars.com
import sys

sys.setrecursionlimit(10_000)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def spiralize(size):
    # Making a snake
    spiral_m = [[0 for _ in range(size)] for _ in range(size)]
    spiral_order_rec(0, 0, 0, spiral_m, size)
    print(f'SPIRAL MATRIX of {size}x{size} size -->> ')
    for row in spiral_m:
        print(row)


def spiral_order_rec(counter: int, j: int, i: int, spiral_m: list[list[int]], size: int):
    print(f'counter: {counter}')
    # filling:
    spiral_m[j][i] = 1
    # deltas for next step Coords
    dj, di = directions[counter % 4]
    # approx stop condition:
    if counter > 2 * size:
        return
    # forward branch:
    if is_valid(j + dj, i + di, size):
        if is_valid(j + 2 * dj, i + 2 * di, size) and spiral_m[j + 2 * dj][i + 2 * di] == 1:
            spiral_order_rec(counter + 1, j, i, spiral_m, size)
        else:
            while is_valid(j + dj, i + di, size) and (not is_valid(j + 2 * dj, i + 2 * di, size) or spiral_m[j + 2 * dj][i + 2 * di] != 1):
                if spiral_m[j + dj + directions[(counter + 1) % 4][0]][i + di + directions[(counter + 1) % 4][1]] == 1:
                    break
                print(f'nj, ni: {j, i}')
                j, i = j + dj, i + di
                spiral_m[j][i] = 1
            else:
                spiral_order_rec(counter, j, i, spiral_m, size)
    else:
        # direction change branch:
        spiral_order_rec(counter + 1, j, i, spiral_m, size)


def is_valid(j: int, i: int, size: int):
    return 0 <= min(j, i) and max(j, i) < size


spiralize(1000)
