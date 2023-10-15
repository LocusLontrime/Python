# accepted on codewars.com
import sys
# directional dict for moving alongside the conveyor:
directions = {'r': (0, 1), 'd': (1, 0), 'l': (0, -1), 'u': (-1, 0)}
# for large tests it is necessary!
sys.setrecursionlimit(100000)


def path_counter(conveyor: str):
    # grid building, final conveyor cell's coordinates finding:
    grid, fy, fx = [], None, None
    for y, row in enumerate(conveyor.split('\n')):
        grid.append([])
        for x, el in enumerate(row):
            if el == 'f':
                fy, fx = y, x
            grid[y].append([el, False])
    Y, X = len(grid), len(grid[0])
    # result 2D-array initialization:
    result = [[-1 for _ in range(X)] for _ in range(Y)]

    def rec_paths_seeker(y_: int, x_: int, path_len: int):
        # is the cell has not already been visited:
        if not grid[y_][x_][1]:
            # making changes in the result 2D array:
            result[y_][x_] = path_len
            # memoization of visiting:
            grid[y_][x_][1] = True
            # looking for neighs:
            for dyx in directions.values():
                neigh_y, neigh_x = (y_ + dyx[0]) % Y, (x_ + dyx[1]) % X
                if (el_ := grid[neigh_y][neigh_x][0]) != 'f' and directions[el_] == (-dyx[0], -dyx[1]):
                    rec_paths_seeker(neigh_y, neigh_x, path_len + 1)
    # rec call:
    rec_paths_seeker(fy, fx, 0)
    return result


def print_2d_array(array2d: list[list], text: str):
    print(f'{text}')
    for row in array2d:
        print(f'{row}')


ex = """rlrlrlrl
rlrlfrll
uuuuuuuu
uuuuuuuu
dddddddu
rrrrrrru"""

ex_ = """dfllllll
drrurrdu
rrlruldu
rrrrrrru"""


print_2d_array(path_counter(ex_), f'solution: ')
