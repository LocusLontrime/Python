import heapq
import math
from collections import defaultdict as d


dfs_iters: int
sols: int
path_found: list['Cell']


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
        self.distance_to = 98  # starting point
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


