# accepted on codewars.com
walk = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
rev_walk = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}
walls = {0: '-', 1: '|', 2: '-', 3: '|'}
node_symbol = '+'


def break_pieces(shape: str):
    board = [[ch for ch in row] for row in shape.split('\n')]
    print(f'pre board: ')
    for row in board:
        print(f'{row}')
    while not set(board[0]) or set(board[0]) == {' '}:
        board = board[1:]
    while not set(board[-1]) or set(board[-1]) == {' '}:
        board = board[:-1]
    mj, mi = len(board), len(board[0])
    print(f'mj, mi: {mj, mi}')
    print(f'board: ')
    for row in board:
        print(f'{row}')
    # visited nodes:
    visited = [[[False for _ in range(len(walk))] for _ in range(mi)] for _ in range(mj)]
    # nodes to be visited:
    to_be_visited = {(0, 0, 0)}
    while to_be_visited:
        j, i, dir_ = to_be_visited.pop()
        print(f'j, i, dir_: {j, i, dir_}')
        # clockwise bypass:
        bypass(j, i, dir_, j, i, board, visited, to_be_visited, mj, mi)
        print(f'visited: ')
        for row in visited:
            print(f'{row}')
        print(f'to_be_visited: {to_be_visited}')


def bypass(j, i, dir_, j_start, i_start, board, visited, to_be_visited, mj, mi):
    temp_j, temp_i = j, i
    print(f'...bypassing j, i, dir_: {j, i, dir_}')
    dj, di = walk[dir_]
    while board[j][i] != node_symbol or (j, i) == (temp_j, temp_i):
        j, i = j + dj, i + di                                                           # 36 366 98 989 98989 LL
    print(f'...j_, i_: {j, i}')
    visited[j][i][_dir_ := (dir_ + 2) % len(walk)] = True
    if (triplet := (j, i, _dir_)) in to_be_visited:
        print(f'......removing triplet {j, i, _dir_} during bypassing')
        to_be_visited.remove(triplet)
    next_dir = investigate_node(j, i, dir_, board, visited, to_be_visited, mj, mi)
    # base case of reaching the initial point again:
    if (j, i) == (j_start, i_start):
        print(f'THE SHAPE IS DONE!!!')
        return
    print(f'......to_be_visited: {to_be_visited}')
    bypass(j, i, next_dir, j_start, i_start, board, visited, to_be_visited, mj, mi)


def investigate_node(j, i, dir_, board, visited, to_be_visited, mj, mi) -> int | None:
    print(f'......investigating a node: ')
    counter_dir = (dir_ + 2) % len(walk)
    next_dir, to_be_vis = None, None
    print(f'......counter_dir: {counter_dir}')
    flag = True
    for delta in range(1, len(walk)):
        dj_, di_ = walk[key := (counter_dir - delta) % len(walk)]
        print(f'......key: {key}')
        print(f'......dj_, di_: {dj_, di_}')
        if 0 <= j + dj_ < mj and 0 <= i + di_ < mi:
            if board[j + dj_][i + di_] == walls[key]:  # ?
                if flag:
                    next_dir = key
                    print(f'.....next_dir: {next_dir}')
                    flag = False
                if not visited[j][i][key]:  # direction!!!
                    if key != next_dir and key != counter_dir:
                        to_be_vis = key
                        print(f'.....to_be_vis: {to_be_vis}')
                        break
    visited[j][i][next_dir] = True
    if (triplet := (j, i, next_dir)) in to_be_visited:
        print(f'......removing triplet {j, i, next_dir} during investigation')
        to_be_visited.remove(triplet)
    if to_be_vis is not None:
        to_be_visited.add((j, i, to_be_vis))
    return next_dir


ex = f'\n' \
     f'+--+---------+\n' \
     f'|  |         |\n' \
     f'|  +---+     |\n' \
     f'|      |     |\n' \
     f'+------+-----+\n' \
     f'|      |     |\n' \
     f'|      |     |\n' \
     f'+------+-----+'
print(f'res: {break_pieces(ex)}')

# k = [1, 2, 98]
# print(f'{set(k)}')


