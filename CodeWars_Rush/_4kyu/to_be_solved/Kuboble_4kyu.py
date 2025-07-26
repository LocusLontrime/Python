# accepted on codewars.com
import re
import time

djdi = ((0, 1), (-1, 0), (0, -1), (1, 0))
bfs_steps: int


def move(k: int, dj: int, di: int, board: list[list[str]], rows: int, cols: int, _coords: list) -> list:
    j_, i_ = _coords[k]
    coords_ = [[el for el in pair] for pair in _coords]
    # move cycle:
    while 0 <= j_ + dj < rows and 0 <= i_ + di < cols:
        cell = board[j_ + dj][i_ + di]
        # break-condition
        if cell == 'X' or [j_ + dj, i_ + di] in _coords:
            break
        # coords incrementation...
        j_ += dj
        i_ += di
    coords_[k] = [j_, i_]
    return coords_


def stringify(coords_: list):
    return ''.join(''.join(str(el) for el in row) for row in coords_)


def parse_board(map_: str):
    # searching for pieces:
    pieces = re.findall(r"[A-WYZ]", map_)
    print(f'{pieces = }')
    # convenient board type:
    board = [[el for el in row.split(' ') if el] for row in map_.split(';')]
    for row in board:
        print(f'{row}')
    # other pars:
    rows, cols = len(board), len(board[0])
    pieces_n = len(pieces)
    # coords:
    pieces_coords = [0 for _ in range(pieces_n)]
    pieces_desired_coords = [0 for _ in range(pieces_n)]
    # let us find pieces initial and desired coords:
    for j in range(rows):
        for i in range(cols):
            for k in range(pieces_n):
                for el in board[j][i]:
                    if el == pieces[k]:
                        pieces_coords[k] = [j, i]
                    elif el == pieces[k].lower():
                        pieces_desired_coords[k] = [j, i]

    return board, rows, cols, pieces, pieces_n, pieces_coords, pieces_desired_coords


def kuboble(map_: str) -> tuple[int, str]:
    global bfs_steps
    bfs_steps = 0
    # parsing board:
    board, rows, cols, pieces, pieces_n, pieces_coords, pieces_desired_coords = parse_board(map_)
    # non-recursive the shortest solution search:
    queue = [(pieces_coords, f'', 0)]
    # initializing the set for visited spots:
    visited = set()
    # core algo (bfs shortest path search):
    while queue:
        bfs_steps += 1
        # pops-out the first coords element:
        _coords, path, step_ = queue.pop(0)
        # check vor visiting:
        if stringify(_coords) not in visited:
            # visiting the pieces' placement ->
            visited.add(stringify(_coords))
            # check for win:
            if _coords == pieces_desired_coords:
                return step_, path
            # next iteration of the moves:
            for dj, di in djdi:
                for k in range(pieces_n):
                    coords_ = move(k, dj, di, board, rows, cols, _coords)
                    queue += [(coords_, path + f'|{coords_}|', step_ + 1)]


map_55 = ". X . . ;a X b . ;. C cB A"
map_3 = "A B . ;a b . ;X . ."
map_23 = "X . X . ;. . . . ;. . b . ;a X B A"
map_10 = "X . X b ;. a . . ;X . B A"

map_13 = "X . Ba A ;X X . . ;. b . ."
map_15 = "A Ba . . ;X . X . ;. . b ."

map_long = "X . . aC B A ;. b . . . . ;X . X . X X ;. c . . . . ;. . X . . . "

start = time.time_ns()
print(f'res -> {kuboble(map_long)}')
finish = time.time_ns()

print(f'time elapsed -> {(finish - start) // 10 ** 6} milliseconds')
print(f'bfs_steps -> {bfs_steps}')

# print(f'{[[1, 2], [3, 2], [1, 3]] == [[1, 2], [3, 2], [1, 3]]}')

# print(f'coords stringified -> {stringify([[1, 2], [3, 2], [1, 3]])}')


