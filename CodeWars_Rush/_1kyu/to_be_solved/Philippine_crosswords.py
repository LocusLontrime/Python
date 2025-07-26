# -*- coding: utf-8 -*-
import time

from collections import defaultdict as d

from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup


dfs_iters: int
sols: int
path_found: list['Cell']


# TODO: 0. implement an algo part which can adjust THRESHOLD value depending on the situation on the board... +(done)
THRESHOLD = 1_000  # ??? questionable value...


class Cell:
    # unit vectors (directions of movement):
    walk = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self, j: int, i: int, length: int):
        # coordinates and bridge-length:
        self.j, self.i = j, i
        self.length = length
        # for coloured crosswords:
        self.colour = ...
        # for building the shortest path of Nodes from the starting point to the ending one
        self.prev_cell = None
        # f = h + g or total cost of the current Node is not needed here
        self.solved = True if self.length == 1 else False  # if the bridge from this cell to another one is built
        # for dp:
        self.visited = False

    def __hash__(self):
        return hash((self.j, self.i))

    def __eq__(self, other):
        return (self.j, self.i) == (other.j, other.i)

    def __str__(self):
        return f'{self.length}({self.j}, {self.i})[{"V" if self.visited else "E"}][{"S" if self.solved else "N"}]'

    def __repr__(self):
        return str(self)

    def possible_ways(self, board: list[list['Cell']], height: int, width: int):
        return [board[self.j + dj][self.i + di] for dj, di in self.walk if
                0 <= self.j + dj < height and 0 <= self.i + di < width]

    @staticmethod
    def is_direction_valid(j: int, i: int, max_j: int, max_i: int):
        """checks if the moving in that direction is valid"""
        return 0 <= j < max_j and 0 <= i < max_i

    # resets two fields for a cell:
    def clear(self):
        self.prev_cell = None

    def manhattan(self, other: 'Cell') -> int:
        """calculates manhattan heuristic distances from one cell to another"""
        return abs(self.j - other.j) + abs(self.i - other.i)

    def dfs(self, length: int, start: 'Cell', aim: 'Cell', board: list[list['Cell']], height: int, width: int):
        # TODO: 3. if passable cells quantity equals to the bridge length required -> the first path found is all we need to calculate!!!
        global dfs_iters, sols, path_found
        if dfs_iters < THRESHOLD:
            # main condition of path building (validation that is crucial for performance):
            if length + self.manhattan(aim) <= aim.length:
                dfs_iters += 1
                # border case (the aim reached, the path's length fits the appropriate distance towards the aim):
                if self == aim and length == aim.length:
                    # path recovering:
                    path = start.recover_path(aim)
                    if sols == 0:
                        # the first path found:
                        path_found = path
                        sols += 1
                    else:
                        # another one found, checks if the path identical in the sense of cells covered or not:
                        if set(path) != set(path_found):  #
                            # the path seems drawing a different ornament:
                            sols += 1
                # visiting:
                self.visited = True
                # body or rec:
                if sols <= 1:
                    # manhattan sort (heuristical speed boost) FAIL:
                    # TODO: CHECK THIS FOR PERFORMANCE INCREASE!!!
                    for next_cell in self.possible_ways(board, height, width):  # sorted(, key=lambda c: abs(aim.length - length - c.manhattan(aim))):
                        if not next_cell.solved and not next_cell.visited and (next_cell.length == 0 or next_cell == aim):
                            if sols <= 1:
                                next_cell.prev_cell = self
                                next_cell.dfs(length + 1, start, aim, board, height, width)
                # unvisiting:
                self.visited = False

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
        # reversing the path:
        path = list(reversed(reversed_shortest_path))
        return path


def solve(board: list[list[int]], height: int, width: int, cells_to_be_solved: int):
    # TODO: 1. too hard for dfs-backtracking pairs need to be postponed to the next iterations... (dfs iterations threshold) +(done)
    # TODO: 2. some structures like square of 2s can be solved in different ways, therefore one appropriate solution should be chosen... (backtracking)
    global dfs_iters, sols, path_found, THRESHOLD
    dfs_iters, sols, path_found = 0, 0, []
    # board of cells constructing:
    board_processed = process_board(board, height, width)
    # dict of pairs of equal length building:
    cells_dict = d(list['Cell'])
    for j in range(height):
        for i in range(width):
            cell_ = board_processed[j][i]
            length_ = cell_.length
            if length_ == 1:
                cell_.solved = True                                                     # 36 366 98 989 98989 LL
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
    # print(f'reachables before: ')
    # for k in cells_dict.keys():
    #     print(f'cells of length = {k}, size: {len(reachables[k])} -->> ')
    #     for key, val in sorted(reachables[k].items(), key=lambda x: len(reachables[k][x[0]])):
    #         print(f'...cell {key}: {val}')
    # core:
    iteration = 0
    proceed = True
    overall_solved = 0
    overall_dfs_steps = 0
    while proceed:
        proceed = False
        prevs = {}
        print(f'THRESHOLD: {THRESHOLD}, solved: [{overall_solved}/{cells_to_be_solved}]')
        while reachables:
            iteration += 1
            print(f'ITERATION: {iteration}')
            solved_cells = set()
            no_path_counter = 0
            for k in sorted(reachables.keys()):
                # print(f'NOW PROCESSING {k} LENGTH: ')
                inner_iters = 0
                for start_cell, neighbouring_cells in sorted(reachables[k].items(), key=lambda x: len(reachables[k][x[0]])):
                    if start_cell not in solved_cells:
                        # searching for a path:
                        if len(neighbouring_cells) == 1:
                            inner_iters += 1
                            aim_cell = neighbouring_cells.pop()
                            # print(f'start_cell, aim_cell: {start_cell, aim_cell}')
                            sols = 0  # sols counter nullifying:
                            dfs_iters = 0
                            path_found = []
                            start_cell.dfs(1, start_cell, aim_cell, board_processed, height, width)
                            overall_dfs_steps += dfs_iters
                            # print(f'{inner_iters}th paths_q: {sols}')
                            # print(f'...dp_iters: {dfs_iters}')
                            if dfs_iters < THRESHOLD:
                                if sols == 1:
                                    # board updating:
                                    # print(f'board updating: ')
                                    for path_cell in path_found:
                                        path_cell.solved = True
                                elif sols == 0:
                                    raise ValueError(f'NO PATH!!!')
                                else:
                                    neighbouring_cells.add(aim_cell)
                            else:
                                neighbouring_cells.add(aim_cell)
                                proceed = True
                            # solved cells set updating:
                            solved_cells.add(start_cell)
                            solved_cells.add(aim_cell)
                        else:
                            # 2 or more cells in set:
                            for neighbouring_cell in list(neighbouring_cells):
                                sols = 0  # sols counter nullifying:
                                dfs_iters = 0
                                path_found = []
                                start_cell.dfs(1, start_cell, neighbouring_cell, board_processed, height, width)
                                overall_dfs_steps += dfs_iters
                                if dfs_iters < THRESHOLD:
                                    if not sols:
                                        no_path_counter += 1
                                        # print(f'NO PATH for {start_cell} and {neighbouring_cell}')
                                        neighbouring_cells.remove(neighbouring_cell)
                                else:
                                    proceed = True
            solved_cells = {cell for cell in solved_cells if cell.solved}
            overall_solved += len(solved_cells)
            print(f'solved_cells: {solved_cells}')
            print(f'{len(solved_cells)} cells solved')
            print(f'{no_path_counter} no-path bridges removed')
            # dict updating:
            update_dict(reachables, solved_cells)
            if prevs == solved_cells:
                print(f'THRESHOLD IS TO BE INCREASED...!!!')
                break
            prevs = solved_cells

        if proceed:
            THRESHOLD *= 2

        print(f'reachables after: ')
        for k in reachables.keys():
            print(f'cells of length = {k}, size: {len(reachables[k])} -->> ')
            for key, val in sorted(reachables[k].items(), key=lambda x: len(reachables[k][x[0]])):
                print(f'...cell {key}: {val}')

    print(f'board processed AFTER: ')  # 36 366 98 989
    for row in board_processed:
        print(f'{"".join(["*" if cell.solved else "." for cell in row])}')

    print(f'FINAL THRESHOLD: {THRESHOLD}')
    print(f'reachables: {reachables}')
    print(f'{iteration} global iterations made')
    print(f'overall solved: [{overall_solved}/{cells_to_be_solved}]')
    print(f'overall dfs iters: {overall_dfs_steps}')


def update_dict(reachables: dict, solved_cells: set):
    for k in list(reachables.keys()):
        keys = list(reachables[k].keys())
        for key in keys:  # 36 366 98 989 LL
            if key in solved_cells:
                reachables[k].pop(key)
            else:
                reachables[k][key] -= solved_cells
            if not reachables[k][key]:
                reachables[k].pop(key)
        if not reachables[k]:
            reachables.pop(k)


def process_board(board: list[list[int]], height, width) -> list[list['Cell']]:
    return [[Cell(j, i, board[j][i]) for i in range(width)] for j in range(height)]


def parse_board(board: list[str]):
    board_parsed = []
    for row in board:
        board_parsed.append([0 if ch == ' ' else int(ch) for ch in row])
    return board_parsed


def get_board_from_site(id_: int) -> tuple[list[list[int]], int, int, int]:  # 55825
    url = f'https://grandgames.net/filippinskie/id{id_}'                                # 36 366 98 989 98989 LL
    try:
        page = requests.get(url)
        print(page.status_code)
        soup = BeautifulSoup(page.text, "html.parser")
        # size parsing:
        size = soup.findAll('div', title='Размер')[0].text  # div title='Размер'
        width, height = map(int, size.split('x'))
        print(f'size: {height, width}')
        # board info getting:
        something = soup.findAll('td', class_=['', 'FKN_1', 'FKN_1 FKL_1'])  # , id='i4-0'
        print(f'something: {something}')
        # board parsing:
        board = [[0 for _ in range(width)] for _ in range(height)]
        counter = 0
        for i in range(width):
            for j in range(height):
                info = something[j * width + i].text
                if info:
                    board[j][i] = int(info)
                    if board[j][i] > 1:
                        counter += 1
                # print(f'val: {board[j][i]}')
        return board, height, width, counter
    except HTTPError as ex:
        if ex.code != 404:
            raise ValueError(f'404 error!!!')


mini_board = [
    [9, 0, 0],
    [0, 0, 0],
    [0, 0, 9]
]

no_path_board = [
    [16, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 16]
]

cute_board = [
    [25, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 25],
]

board_ = [
    "7               2122 4  4",
    "                2  5 2  1",  # 36 366 98 989 98989 LL
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
    [0, 0, 0, 0, 18, 11, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 8, 6, 0, 0, 0, 6, 0, 0, 0, 0, 13, 0, 0, 0, 13, 7, 0, 0, 0, 11,
     0, 0, 0, 0, 0, 0, 4, 0, 5, 5],
    [0, 3, 0, 0, 8, 1, 0, 0, 9, 0, 0, 0, 6, 0, 0, 0, 12, 0, 0, 5, 6, 0, 4, 0, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0,
     5, 11, 0, 4, 5, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 11, 0, 0, 8, 0, 0, 2, 0, 3, 0, 3, 4, 0, 3, 0, 3, 0, 5, 0, 0, 3, 0, 3, 0, 0, 5, 0,
     0, 2, 2, 0, 8, 13, 0, 0, 0],
    [0, 3, 3, 0, 0, 8, 0, 0, 0, 0, 0, 6, 0, 7, 0, 7, 0, 2, 0, 5, 0, 12, 0, 0, 0, 5, 0, 0, 2, 2, 0, 3, 1, 4, 0, 5, 5, 0,
     6, 1, 0, 0, 2, 2, 0, 0, 6],
    [0, 0, 0, 3, 0, 0, 5, 9, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 4, 4, 0, 3, 6, 1, 8, 0, 0, 2, 0, 0, 4, 6, 0,
     0, 8, 0, 7, 1, 0, 0, 0, 6],
    [18, 0, 0, 5, 0, 3, 1, 3, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 5, 0, 5, 3, 4, 0, 0, 0, 0, 3, 2, 1, 0, 0, 0, 0,
     3, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 5, 7, 0, 3, 0, 0, 5, 2, 3, 0, 2, 7, 4, 0, 0, 6, 2, 2, 1, 0, 0, 3, 0, 0, 4, 0, 5, 6, 0, 0, 0, 6, 0, 0, 0, 0, 3,
     0, 0, 4, 7, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 6, 0, 0, 2, 2, 4, 0, 2, 11, 4, 0, 0, 5, 1, 4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 9, 0, 0, 0, 0, 7, 5],
    [10, 0, 7, 0, 6, 0, 0, 2, 3, 4, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 3, 4, 0, 4, 4, 8, 0, 0, 5, 0, 0, 2, 9,
     0, 4, 0, 0, 0, 0, 0, 0, 7],
    [0, 4, 0, 0, 0, 0, 5, 3, 0, 0, 9, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 3, 0, 4, 0, 2, 0, 6, 0, 0, 0, 0, 3, 2, 4,
     0, 0, 0, 4, 4, 0, 3, 0, 0],
    [0, 0, 0, 0, 11, 0, 0, 2, 2, 0, 4, 0, 0, 2, 0, 5, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 4, 0, 6, 0, 3, 4, 0, 0,
     0, 8, 0, 0, 5, 0, 0, 3, 3],
    [0, 6, 4, 0, 0, 0, 0, 1, 0, 0, 4, 0, 0, 2, 0, 0, 11, 9, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 0, 3, 0, 0, 4, 0, 5, 0, 3, 0,
     0, 5, 0, 4, 13, 0, 8, 3, 0],
    [0, 0, 0, 3, 11, 0, 0, 5, 0, 0, 9, 1, 0, 3, 0, 3, 0, 0, 0, 0, 3, 4, 0, 0, 0, 7, 1, 7, 3, 6, 0, 5, 0, 0, 3, 3, 0, 0,
     6, 0, 0, 0, 0, 0, 0, 3, 4],
    [0, 0, 3, 5, 0, 5, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 3, 7, 2, 0, 8,
     6, 0, 0, 0, 5, 0, 3, 0, 0],
    [0, 0, 2, 2, 0, 0, 8, 0, 0, 5, 0, 1, 0, 2, 9, 4, 4, 0, 0, 0, 4, 0, 4, 1, 2, 0, 0, 4, 0, 2, 0, 7, 4, 0, 0, 2, 0, 0,
     4, 0, 13, 4, 0, 0, 0, 4, 0],
    [0, 0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 2, 0, 4, 8, 0, 0, 0, 4, 0, 0, 3, 2, 5, 0, 0, 0, 3, 0, 0, 6,
     4, 0, 0, 0, 0, 3, 0, 8, 3],
    [0, 6, 7, 0, 0, 0, 5, 0, 9, 3, 0, 0, 0, 0, 1, 0, 3, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 4, 5,
     0, 5, 0, 5, 3, 0, 2, 3, 0],
    [10, 6, 0, 0, 0, 7, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 7, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 2, 7, 2],
    [0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3,
     1, 0, 0, 0, 3, 0, 13, 0, 2],
    [0, 0, 6, 6, 4, 0, 3, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 2,
     0, 0, 0, 11, 0, 0, 7, 0, 0],
    [0, 5, 0, 0, 0, 3, 3, 3, 1, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 7, 0, 0, 0,
     0, 0, 0, 0, 3, 0, 7, 0, 0],
    [0, 0, 5, 0, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 2, 4, 0, 0, 3, 0, 4,
     4, 0, 3, 0, 0, 0, 0, 4, 0],
    [0, 0, 6, 0, 0, 0, 3, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 3, 0, 0, 0, 0,
     4, 3, 5, 1, 0, 7, 0, 4, 0],
    [6, 0, 0, 0, 0, 5, 0, 0, 4, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 5, 0, 0, 7, 0, 0, 0, 0, 3, 3, 0,
     0, 1, 0, 11, 0, 0, 3, 0, 2],
    [0, 4, 3, 6, 4, 0, 0, 0, 0, 2, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0, 3, 3, 7, 0, 0, 2,
     0, 0, 0, 0, 5, 3, 4, 1, 2],
    [0, 3, 0, 2, 0, 0, 3, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 6, 0, 5, 0, 2, 2, 0, 0, 7, 0, 3, 7, 1, 3, 0, 3, 2,
     4, 0, 0, 0, 26, 0, 0, 0, 3],
    [4, 0, 0, 2, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 3, 0, 3, 2, 6, 0, 0, 4, 2, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 4, 7, 3, 7],
    [10, 0, 0, 1, 4, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 4, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     13, 0, 2, 2, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 3, 0, 3, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 4,
     0, 0, 4, 2, 2, 0, 3, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 3, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0,
     3, 0, 0, 0, 0, 0, 0, 3, 5],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 2, 2, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0,
     0, 3, 0, 4, 4, 5, 0, 0, 0],
    [0, 3, 0, 3, 2, 6, 0, 0, 0, 3, 0, 3, 0, 0, 2, 2, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 3, 4, 1, 0, 6, 0, 4, 4, 2, 0, 6, 6,
     0, 3, 0, 0, 0, 0, 9, 3, 1],
    [0, 6, 10, 1, 0, 0, 0, 1, 0, 6, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 0, 4, 0, 0, 6, 0, 3, 0, 0, 0,
     0, 0, 0, 9, 1, 0, 3, 0, 7],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2, 0, 0, 0, 3, 1, 1, 0, 0, 3, 0, 4,
     0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 3, 0, 0, 0, 2, 2, 3, 0, 0, 0, 5, 0, 0, 0, 0, 1, 0, 0, 0, 6,
     0, 13, 0, 3, 0, 0, 4, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 3, 0, 3, 2, 0, 0, 1, 0, 2, 2, 0, 3, 1, 0, 0, 0, 1, 4, 0,
     0, 6, 0, 0, 4, 0, 0, 7, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 2, 1, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 0, 3, 0, 3, 0, 0, 0,
     0, 2, 0, 3, 5, 0, 0, 8, 3],
    [5, 3, 1, 4, 0, 6, 0, 6, 0, 0, 0, 0, 0, 3, 3, 1, 0, 4, 1, 0, 0, 3, 0, 3, 0, 9, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 5, 0,
     0, 2, 0, 5, 0, 0, 0, 3, 0],
    [2, 0, 3, 8, 0, 0, 8, 5, 0, 2, 2, 6, 3, 3, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 2, 0, 0, 2, 1, 1, 0, 2, 2, 0, 2, 2, 0, 1,
     0, 5, 0, 0, 3, 0, 0, 3, 1],
    [2, 0, 0, 5, 5, 0, 0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 8, 2, 0, 13, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
     0, 3, 0, 3, 0, 0, 3, 0, 5],
    [5, 0, 3, 0, 0, 2, 0, 0, 1, 5, 0, 0, 0, 0, 4, 0, 2, 2, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     2, 0, 0, 3, 8, 9, 1, 0, 0],
    [5, 3, 0, 0, 5, 2, 6, 3, 0, 0, 0, 0, 6, 0, 2, 0, 7, 0, 3, 0, 3, 0, 0, 4, 0, 0, 4, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 4,
     2, 3, 0, 0, 0, 0, 5, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 4, 0, 4, 2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 3, 0, 5,
     0, 5, 26, 3, 0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 7, 0, 6, 0, 4, 0, 0, 0, 0, 0, 3, 1, 0, 6, 0, 0, 3, 8, 4, 0, 3, 0, 0, 5, 4, 5, 0, 0, 0, 4, 3,
     0, 0, 9, 0, 0, 0, 7, 0, 0],
    [0, 5, 7, 0, 0, 3, 0, 3, 0, 5, 3, 0, 3, 4, 0, 0, 4, 0, 3, 0, 6, 4, 4, 0, 3, 13, 0, 0, 3, 4, 0, 0, 2, 2, 5, 3, 3, 0,
     2, 2, 3, 0, 3, 3, 0, 3, 1]
]
# data = get_board_from_site()
start_ = time.time_ns()
#solve(*data)  # 56076, 55825, 54510 ?, 54891, 55032, 54524 ?, 54527, 335091, 329092, 55980, 56987, 55863, 56898, 56834, 55910, 55846
# solve(cute_board, 5, 5, 0)
solve(parse_board(board_), 10, 25, 0)
# solve(mini_board, 3, 3, 2)
# solve(cute_board, 5, 5, 2)
# solve(no_path_board, 4, 4, 2)
finish_ = time.time_ns()
print(f'time elapsed str: {(finish_ - start_) // 10 ** 6} milliseconds')
