import heapq
import math
from collections import defaultdict as d


dfs_iters: int
sols: int


class Cell:
    walk = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self, j: int, i: int, length: int):
        self.j, self.i = j, i
        self.length = length
        self.weight = 1
        # for coloured crosswords:
        self.colour = ...
        # for building the shortest path of Nodes from the starting point to the ending one
        self.prev_cell = None
        # memoization for dp A*, aggregated cost of moving from start to the current Node:
        self.distance_to = math.inf  # Infinity chosen for convenience and algorithm's logic
        # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node:
        self.heuristic_distance = 0
        # f = h + g or total cost of the current Node is not needed here
        self.solved = True if self.length == 1 else False  # if the bridge from this cell to another one is built
        # for dp:
        self.visited = False

    def __hash__(self):
        return hash((self.j, self.i))

    def __eq__(self, other):
        return (self.j, self.i) == (other.j, other.i)

    def __lt__(self, other):
        return self.heuristic_distance + self.distance_to < other.heuristic_distance + other.distance_to

    def __str__(self):
        return f'{self.length}({self.j}, {self.i})[{"V" if self.visited else "E"}][{"S" if self.solved else "N"}]'

    def __repr__(self):
        return str(self)

    def possible_ways(self, board: list[list['Cell']], height: int, width: int):
        return [board[self.j + dj][self.i + di] for dj, di in self.walk if
                0 <= self.j + dj < height and 0 <= self.i + di < width]

    @property
    def f(self):
        return self.distance_to + self.heuristic_distance

    @staticmethod
    def is_direction_valid(j: int, i: int, max_j: int, max_i: int):
        """checks if the moving in that direction is valid"""
        return 0 <= j < max_j and 0 <= i < max_i

    # resets two fields for a cell:
    def clear(self):
        self.distance_to = math.inf
        self.prev_cell = None

    # various heuristic distances from one cell to another:
    def calc_manhattan_distance(self, other: 'Cell') -> int:
        return abs(self.j - other.j) + abs(self.i - other.i)

    @staticmethod
    def no_heur(self, other: 'Cell') -> int:
        return 0

    def dfs(self, length: int, aim: 'Cell', board: list[list['Cell']], height: int, width: int) -> int:
        global dfs_iters, sols
        dfs_iters += 1
        # print(f'j, i, length: {self.j, self.i, length}')
        # validation:
        if length <= aim.length:
            # border case:
            if self == aim:
                print(f'length: [{length}/{aim.length}]')
                if length == aim.length:
                    print(f'BINGO!!!')
                    sols += 1
                    return 1
            # visiting:
            self.visited = True
            # body or rec:
            res = 0
            cell = None
            if sols <= 1:
                # manhattan sort (heuristical speed boost):
                for next_cell in sorted(self.possible_ways(board, height, width), key=lambda c: abs(aim.length - length - abs(c.j - aim.j) - abs(c.i - aim.i))):
                    if not next_cell.solved and not next_cell.visited and next_cell.length in [0, aim.length]:
                        if sols <= 1:
                            delta = next_cell.dfs(length + 1, aim, board, height, width)
                            res += delta
                            if delta:
                                cell = next_cell
            if res == 1:
                cell.prev_cell = self
            # unvisiting:
            self.visited = False
            # returning accumulated res:
            return res
        else:
            return 0

    def recover_path(self, aim: 'Cell') -> list['Cell']:
        # the last point of the path found
        cell_ = aim
        reversed_shortest_path = []
        # path restoring (here we get the reversed path)
        while cell_ != self:
            reversed_shortest_path.append(cell_)
            cell_ = cell_.prev_cell
        # start cell adding:
        reversed_shortest_path.append(self)
        print(f'reversed_shortest_path: {reversed_shortest_path}')
        # reversing the path:
        path = list(reversed(reversed_shortest_path))
        print(f'path: {path}')
        return path

    def modified_dijkstra(self, aim: 'Cell', board: list[list['Cell']], height: int, width: int) -> list['Cell'] or None:
        """returns path (list of Cells) if exists and unique, if no path exists or 2 or more exist -> returns None"""
        print(f'THE FIRST DIJKSTRA: ')
        path_ = self.dijkstra(aim, board, height, width)
        if not path_:
            # there is no path:
            return None
        # check for uniqueness:
        for cell_ in path_:
            # weight increasing:
            cell_.weight = 2
        # a try to find another path:
        print(f'THE SECOND DIJKSTRA: ')
        another_path_ = self.dijkstra(aim, board, height, width)
        # backtracking:
        for cell_ in path_:
            # weight decreasing, returning to defaults:
            cell_.weight = 1
        if not another_path_:
            # there is only one unique path:
            return path_
        else:
            # there are multiple paths:
            return None

    def dijkstra(self, aim: 'Cell', board: list[list['Cell']], height: int, width: int) -> list['Cell']:
        """searches for a path in neighbourhood of self-Cell"""
        cells_to_be_visited = [self]
        self.distance_to = 0  # starting point
        # shaping priority queue (heap)
        heapq.heapify(cells_to_be_visited)
        # coordinates of cells visited:
        visited_cells = set()
        # flag of finding solution (path):
        flag = False
        # while there is at least one not visited passable cell we continue cycling:
        while len(cells_to_be_visited) > 0:
            # executing the current cell from the priority queue (heap)
            curr_cell = heapq.heappop(cells_to_be_visited)
            print(f'curr_cell: {curr_cell}')
            visited_cells.add((curr_cell.j, curr_cell.i))
            # border case:
            if curr_cell == aim:  # and curr_cell.colour == aimed_colour:
                flag = True
                break
            # here we're looking for all the adjacent and passable nodes for a current node and pushing them to the heap (priority queue)
            for next_cell in curr_cell.possible_ways(board, height, width):
                # searching in the local neighbourhood of the initial point of length = aim_length:
                # TODO: CHECK THIS CONDITION!!!
                if curr_cell.distance_to <= aim.length:
                    # cell should not be solved:
                    if next_cell.length in [0, aim.length] and not next_cell.solved:
                        # Dijkstra dp:
                        if next_cell.distance_to > curr_cell.distance_to + curr_cell.weight:  # a kind of dynamic programming
                            next_cell.distance_to = curr_cell.distance_to + curr_cell.weight  # every step distance from one node to an adjacent one is equal to 1
                            next_cell.heuristic_distance = 0  # heuristic function, needed for sorting the nodes to be visited in priority order
                            # next step preparation:
                            next_cell.prev_cell = curr_cell  # constructing the path
                            heapq.heappush(cells_to_be_visited, next_cell)  # adding node to the heap
        # solution existence check:
        if not flag:
            # there is no solution...
            return []
        # the last point of the path found
        cell_ = aim
        reversed_shortest_path = []
        # path restoring (here we get the reversed path)
        while cell_.prev_cell:
            reversed_shortest_path.append(cell_)
            cell_ = cell_.prev_cell
        # start cell adding:
        reversed_shortest_path.append(self)
        print(f'reversed_shortest_path: {reversed_shortest_path}')
        # reversing the path:
        path = list(reversed(reversed_shortest_path))
        print(f'path: {path}')
        # clearing some pars:
        for j, i in visited_cells:
            board[j][i].clear()
        # returning the right shortest path
        return path


def solve(board: list[list[int]], height: int, width: int):
    global dfs_iters, sols
    dfs_iters, sols = 0, 0
    # board of cells constructing:
    board_processed = process_board(board, height, width)
    print(f'board processed: ')
    for row in board_processed:
        print(f'{row}')
    # dict of pairs of equal length building:
    cells_dict = d(list['Cell'])
    for j in range(height):
        print(f'j, length: {j, len(board[j])}')
        for i in range(width):
            cell_ = board_processed[j][i]
            length_ = cell_.length
            if length_ == 1:
                cell_.solved = True
            elif length_ > 1:
                cells_dict[length_].append(cell_)
    print(f'cells_dict: ')
    for k, v in cells_dict.items():
        print(f'cells of length = {k} ({len(v)}): {v}')
    # reachables structure building:
    reachables = {}
    for k, v in cells_dict.items():
        reachables[k] = d(set['Cell'])
        for i1 in range(len(v) - 1):
            for i2 in range(i1 + 1, len(v)):
                if abs(v[i1].j - v[i2].j) + abs(v[i1].i - v[i2].i) < v[i1].length:
                    reachables[k][v[i1]].add(v[i2])
                    reachables[k][v[i2]].add(v[i1])

    print(f'reachables before: ')
    for k in cells_dict.keys():
        print(f'cells of length = {k}, size: {len(reachables[k])} -->> ')
        for key, val in sorted(reachables[k].items(), key=lambda x: len(reachables[k][x[0]])):
            print(f'...cell {key}: {val}')

    # core:
    iteration = 0
    iters = 5 + 2
    inner_iters = 0
    for iter_ in range(1, iters + 1):
        print(f'ITERATION: {iter_}')
        solved_cells = set()
        for k in reachables.keys():
            print(f'NOW PROCESSING {k} LENGTH: ')
            for start_cell, neighbouring_cells in sorted(reachables[k].items(), key=lambda x: len(reachables[k][x[0]])):
                if start_cell not in solved_cells:
                    # searching for a path:
                    if len(neighbouring_cells) == 1:
                        inner_iters += 1
                        aim_cell = neighbouring_cells.pop()
                        print(f'start_cell, aim_cell: {start_cell, aim_cell}')
                        sols = 0  # sols counter nullifying:
                        paths_q = start_cell.dfs(1, aim_cell, board_processed, height, width)
                        print(f'{inner_iters}th paths_q: {paths_q}')
                        print(f'dp_iters: {dfs_iters}')
                        if paths_q == 1:
                            # path recovering:
                            print(f'path recovering...')
                            path = start_cell.recover_path(aim_cell)
                            # board updating:
                            print(f'board updating: ')
                            for path_cell in path:
                                path_cell.solved = True
                        elif paths_q == 0:
                            raise ValueError(f'NO PATH!!!')
                        else:
                            neighbouring_cells.add(aim_cell)
                        # solved cells set updating:
                        solved_cells.add(start_cell)
                        solved_cells.add(aim_cell)
                    else:
                        # 2 or more cells in set:
                        for neighbouring_cell in list(neighbouring_cells):
                            sols = 0  # sols counter nullifying:
                            path_q = start_cell.dfs(1, neighbouring_cell, board_processed, height, width)
                            if not path_q:
                                print(f'NO PATH for {start_cell} and {neighbouring_cell}')
                                neighbouring_cells.remove(neighbouring_cell)
        solved_cells = {cell for cell in solved_cells if cell.solved}
        print(f'solved_cells: {solved_cells}')
        print(f'{len(solved_cells)} cells solved')
        # dict updating:
        for k in list(reachables.keys()):
            keys = list(reachables[k].keys())
            for key in keys:
                if key in solved_cells:
                    reachables[k].pop(key)
                else:
                    reachables[k][key] -= solved_cells
                if not reachables[k][key]:
                    reachables[k].pop(key)
            if not reachables[k]:
                reachables.pop(k)

    print(f'reachables after: ')
    for k in reachables.keys():
        print(f'cells of length = {k}, size: {len(reachables[k])} -->> ')
        for key, val in sorted(reachables[k].items(), key=lambda x: len(reachables[k][x[0]])):
            print(f'...cell {key}: {val}')

    print(f'board processed AFTER: ')  # 36 366 98 989
    for row in board_processed:
        print(f'{"".join(["*" if cell.solved else "." for cell in row])}')

    # start = board_processed[5][3]
    # aim = board_processed[4][6]
    # print(f'start, aim: {start, aim}')
    # sols = 0  # sols counter nullifying:
    # path_q = start.dfs(1, aim, board_processed, height, width)
    # print(f'path_q: {path_q}')
    # print(f'dfs iters: {dfs_iters}')


def process_board(board: list[list[int]], height, width) -> list[list['Cell']]:
    return [[Cell(j, i, board[j][i]) for i in range(width)] for j in range(height)]


def backtrack(group_num: int, cells_dict: d[int, list['Cell']], board: list[list['Cell']], height: int, width: int):
    ...


def parse_board(board: list[str]):
    board_parsed = []
    for row in board:
        board_parsed.append([0 if ch == ' ' else int(ch) for ch in row])
    return board_parsed


mini_board = [
    [9, 0, 0],
    [0, 0, 0],
    [0, 0, 9]
]

board_ = [
    "7               2122 4  4",
    "                2  5 2  1",                                                      # 36 366 98 989 98989 LL
    "                  3 523  ",
    "                     3   ",
    "                  3 7 2  ",
    " 3                22 72  ",
    "7 2        34      4     ",
    " 324     333 343         ",
    "  22    5 1   3  43 1    ",
    "    453 33     4 3 4     "
]

# print(f'board parsed: ')
# for row_ in parse_board(board_):
#     print(f'{row_}')

mega_board = [
    [0, 0, 0, 0, 18, 11, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 8, 6, 0, 0, 0, 6, 0, 0, 0, 0, 13, 0, 0, 0, 13, 7, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 4, 0, 5, 5],
    [0, 3, 0, 0, 8, 1, 0, 0, 9, 0, 0, 0, 6, 0, 0, 0, 12, 0, 0, 5, 6, 0, 4, 0, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 5, 11, 0, 4, 5, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 11, 0, 0, 8, 0, 0, 2, 0, 3, 0, 3, 4, 0, 3, 0, 3, 0, 5, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 2, 2, 0, 8, 13, 0, 0, 0],
    [0, 3, 3, 0, 0, 8, 0, 0, 0, 0, 0, 6, 0, 7, 0, 7, 0, 2, 0, 5, 0, 12, 0, 0, 0, 5, 0, 0, 2, 2, 0, 3, 1, 4, 0, 5, 5, 0, 6, 1, 0, 0, 2, 2, 0, 0, 6],
    [0, 0, 0, 3, 0, 0, 5, 9, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 4, 4, 0, 3, 6, 1, 8, 0, 0, 2, 0, 0, 4, 6, 0, 0, 8, 0, 7, 1, 0, 0, 0, 6],
    [18, 0, 0, 5, 0, 3, 1, 3, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 5, 0, 5, 3, 4, 0, 0, 0, 0, 3, 2, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 5, 7, 0, 3, 0, 0, 5, 2, 3, 0, 2, 7, 4, 0, 0, 6, 2, 2, 1, 0, 0, 3, 0, 0, 4, 0, 5, 6, 0, 0, 0, 6, 0, 0, 0, 0, 3, 0, 0, 4, 7, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 6, 0, 0, 2, 2, 4, 0, 2, 11, 4, 0, 0, 5, 1, 4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 7, 5],
    [10, 0, 7, 0, 6, 0, 0, 2, 3, 4, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 3, 4, 0, 4, 4, 8, 0, 0, 5, 0, 0, 2, 9, 0, 4, 0, 0, 0, 0, 0, 0, 7],
    [0, 4, 0, 0, 0, 0, 5, 3, 0, 0, 9, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 3, 0, 4, 0, 2, 0, 6, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0, 4, 4, 0, 3, 0, 0],
    [0, 0, 0, 0, 11, 0, 0, 2, 2, 0, 4, 0, 0, 2, 0, 5, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 4, 0, 6, 0, 3, 4, 0, 0, 0, 8, 0, 0, 5, 0, 0, 3, 3],
    [0, 6, 4, 0, 0, 0, 0, 1, 0, 0, 4, 0, 0, 2, 0, 0, 11, 9, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 0, 3, 0, 0, 4, 0, 5, 0, 3, 0, 0, 5, 0, 4, 13, 0, 8, 3, 0],
    [0, 0, 0, 3, 11, 0, 0, 5, 0, 0, 9, 1, 0, 3, 0, 3, 0, 0, 0, 0, 3, 4, 0, 0, 0, 7, 1, 7, 3, 6, 0, 5, 0, 0, 3, 3, 0, 0, 6, 0, 0, 0, 0, 0, 0, 3, 4],
    [0, 0, 3, 5, 0, 5, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 3, 7, 2, 0, 8, 6, 0, 0, 0, 5, 0, 3, 0, 0],
    [0, 0, 2, 2, 0, 0, 8, 0, 0, 5, 0, 1, 0, 2, 9, 4, 4, 0, 0, 0, 4, 0, 4, 1, 2, 0, 0, 4, 0, 2, 0, 7, 4, 0, 0, 2, 0, 0, 4, 0, 13, 4, 0, 0, 0, 4, 0],
    [0, 0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 2, 0, 4, 8, 0, 0, 0, 4, 0, 0, 3, 2, 5, 0, 0, 0, 3, 0, 0, 6, 4, 0, 0, 0, 0, 3, 0, 8, 3],
    [0, 6, 7, 0, 0, 0, 5, 0, 9, 3, 0, 0, 0, 0, 1, 0, 3, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 4, 5, 0, 5, 0, 5, 3, 0, 2, 3, 0],
    [10, 6, 0, 0, 0, 7, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 7, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 7, 2],
    [0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 1, 0, 0, 0, 3, 0, 13, 0, 2],
    [0, 0, 6, 6, 4, 0, 3, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 2, 0, 0, 0, 11, 0, 0, 7, 0, 0],
    [0, 5, 0, 0, 0, 3, 3, 3, 1, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 3, 0, 7, 0, 0],
    [0, 0, 5, 0, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 2, 4, 0, 0, 3, 0, 4, 4, 0, 3, 0, 0, 0, 0, 4, 0],
    [0, 0, 6, 0, 0, 0, 3, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 3, 0, 0, 0, 0, 4, 3, 5, 1, 0, 7, 0, 4, 0],
    [6, 0, 0, 0, 0, 5, 0, 0, 4, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 5, 0, 0, 7, 0, 0, 0, 0, 3, 3, 0, 0, 1, 0, 11, 0, 0, 3, 0, 2],
    [0, 4, 3, 6, 4, 0, 0, 0, 0, 2, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0, 3, 3, 7, 0, 0, 2, 0, 0, 0, 0, 5, 3, 4, 1, 2],
    [0, 3, 0, 2, 0, 0, 3, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 6, 0, 5, 0, 2, 2, 0, 0, 7, 0, 3, 7, 1, 3, 0, 3, 2, 4, 0, 0, 0, 26, 0, 0, 0, 3],
    [4, 0, 0, 2, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 3, 0, 3, 2, 6, 0, 0, 4, 2, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 7, 3, 7],
    [10, 0, 0, 1, 4, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 4, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 2, 2, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 3, 0, 3, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 4, 0, 0, 4, 2, 2, 0, 3, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 3, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 5],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 2, 2, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 3, 0, 4, 4, 5, 0, 0, 0],
    [0, 3, 0, 3, 2, 6, 0, 0, 0, 3, 0, 3, 0, 0, 2, 2, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 3, 4, 1, 0, 6, 0, 4, 4, 2, 0, 6, 6, 0, 3, 0, 0, 0, 0, 9, 3, 1],
    [0, 6, 10, 1, 0, 0, 0, 1, 0, 6, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 0, 4, 0, 0, 6, 0, 3, 0, 0, 0, 0, 0, 0, 9, 1, 0, 3, 0, 7],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2, 0, 0, 0, 3, 1, 1, 0, 0, 3, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 3, 0, 0, 0, 2, 2, 3, 0, 0, 0, 5, 0, 0, 0, 0, 1, 0, 0, 0, 6, 0, 13, 0, 3, 0, 0, 4, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 3, 0, 3, 2, 0, 0, 1, 0, 2, 2, 0, 3, 1, 0, 0, 0, 1, 4, 0, 0, 6, 0, 0, 4, 0, 0, 7, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 2, 1, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 2, 0, 3, 5, 0, 0, 8, 3],
    [5, 3, 1, 4, 0, 6, 0, 6, 0, 0, 0, 0, 0, 3, 3, 1, 0, 4, 1, 0, 0, 3, 0, 3, 0, 9, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 5, 0, 0, 2, 0, 5, 0, 0, 0, 3, 0],
    [2, 0, 3, 8, 0, 0, 8, 5, 0, 2, 2, 6, 3, 3, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 2, 0, 0, 2, 1, 1, 0, 2, 2, 0, 2, 2, 0, 1, 0, 5, 0, 0, 3, 0, 0, 3, 1],
    [2, 0, 0, 5, 5, 0, 0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 8, 2, 0, 13, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 5],
    [5, 0, 3, 0, 0, 2, 0, 0, 1, 5, 0, 0, 0, 0, 4, 0, 2, 2, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 8, 9, 1, 0, 0],
    [5, 3, 0, 0, 5, 2, 6, 3, 0, 0, 0, 0, 6, 0, 2, 0, 7, 0, 3, 0, 3, 0, 0, 4, 0, 0, 4, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 4, 2, 3, 0, 0, 0, 0, 5, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 4, 0, 4, 2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 3, 0, 5, 0, 5, 26, 3, 0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 7, 0, 6, 0, 4, 0, 0, 0, 0, 0, 3, 1, 0, 6, 0, 0, 3, 8, 4, 0, 3, 0, 0, 5, 4, 5, 0, 0, 0, 4, 3, 0, 0, 9, 0, 0, 0, 7, 0, 0],
    [0, 5, 7, 0, 0, 3, 0, 3, 0, 5, 3, 0, 3, 4, 0, 0, 4, 0, 3, 0, 6, 4, 4, 0, 3, 13, 0, 0, 3, 4, 0, 0, 2, 2, 5, 3, 3, 0, 2, 2, 3, 0, 3, 3, 0, 3, 1]
]


# solve(mega_board, 45, 47)
# solve(parse_board(board_), 10, 25)
solve(mini_board, 3, 3)
