# accepted on codewars.com 1472ms...
import math
import heapq
import time

MODULO = 15
DIRS_Q = 4


class Node:
    djdidpos = ((0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 0, 1))
    DIRS = {(0, 1): 'E', (1, 0): 'S', (0, -1): 'W', (-1, 0): 'N'}

    def __init__(self, j: int, i: int, val: int, pos: int):
        self.j, self.i = j, i
        self.val = val
        self.pos = pos  # 0 -> North, 1 -> East, 2 -> South, 3 -> West
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one

        self.g = math.inf  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic

    def __eq__(self, other: 'Node'):
        return self.j, self.i, self.pos == other.j, other.i, other.pos

        # this is needed for using Node objects in priority queue like heapq and so on

    def __lt__(self, other: 'Node'):
        return self.g < other.g  # the right sigh is "<" for __lt__() method

    def dijkstra(self, ej: int, ei: int, grid: list[list[list['Node']]], max_j: int, max_i: int):
        vertexes_to_be_visited = [self]
        self.g = 0

        heapq.heapify(vertexes_to_be_visited)
        # just for convenience...
        iterations = 0

        node = None

        while len(vertexes_to_be_visited) > 0:
            curr_node: Node = heapq.heappop(vertexes_to_be_visited)
            # just a number of a-star iterations needed for building the shortest path from starting node to the ending one
            iterations += 1
            print(f'curr node j, i, pos: ({curr_node.j}, {curr_node.i}, {curr_node.pos}), iteration: {iterations}')

            # stop condition, here we reach the ending point (no matter at what pos):
            if (curr_node.j, curr_node.i) == (ej, ei):
                print(f'The path is done in {iterations} iterations')
                node = curr_node
                break

            # here we're looking for all the adjacent and passable nodes for a current node and pushing them to the heap (priority queue)
            for i, (dj, di, dpos) in enumerate(self.djdidpos):
                if 0 <= (j_ := curr_node.j + dj) < max_j and 0 <= (i_ := curr_node.i + di) < max_i:
                    next_possible_node = grid[j_][i_][(curr_node.pos + dpos) % DIRS_Q]
                    # check for a wall:
                    if dpos or not is_wall(curr_node.val, i) and not is_wall(next_possible_node.val, (i + 2) % DIRS_Q):
                        if next_possible_node.g > curr_node.g + dpos:  # a kind of dynamic programming
                            next_possible_node.g = curr_node.g + dpos  # every step distance from one node to an adjacent one is equal to 1
                            next_possible_node.previously_visited_node = curr_node  # constructing the path
                            heapq.heappush(vertexes_to_be_visited, next_possible_node)  # adding node to the heap

        # the last point of the path found
        if node is None:
            return None
        print(f'node: {node.j, node.i, node.pos}')
        print(f'ints : {node.g + 1}')

        # path restoring (here we get the reversed path)
        reversed_shortest_path = []
        while node.previously_visited_node:
            reversed_shortest_path.append(node)
            node = node.previously_visited_node
        # we should not forget to add the start point:
        reversed_shortest_path.append(self)

        # returning the right shortest path
        return [(node.j, node.i, node.pos) for node in list(reversed(reversed_shortest_path))]


def maze_solver(ar: tuple):
    max_j, max_i = len(ar), len(ar[0])
    print(f'{max_j, max_i = }')
    sj, si = [(j, i) for j in range(max_j) for i in range(max_i) if ar[j][i] == 'B'][0]
    ej, ei = [(j, i) for j in range(max_j) for i in range(max_i) if ar[j][i] == 'X'][0]
    print(f'{sj, si, ej, ei = }')

    grid = [[[Node(j, i, rotate(el if type(el := ar[j][i]) is int else 0, pos), pos) for pos in range(DIRS_Q)] for i in
             range(max_i)] for j in range(max_j)]

    path = grid[sj][si][0].dijkstra(ej, ei, grid, max_j, max_i)

    if path is None:  # 36 366 98 989 98989 LL
        return None

    print(f'{path = }')
    # path translating:
    res = []
    interval_res = ''
    for i in range(len(path) - 1):
        print(f'{i} -> {path[i + 1], path[i] = }')
        if (p_ := path[i + 1])[2] == (_p := path[i])[2]:
            interval_res += Node.DIRS[p_[0] - _p[0], p_[1] - _p[1]]
        else:
            res += [interval_res]
            interval_res = ''
    res += [
        interval_res]  # TODO: It was a SUBTLE ERROR... there was no BRACKETS around 'interval_res' and the final intervals amount got greater...

    return res


def rotate(n: int, q: int = 0) -> int:  # 36 366 98 989 98989 LL
    return (n << q) % MODULO if n != 15 else 15


def is_wall(n: int, ind: int) -> int:
    return n & [1, 2, 4, 8][ind]


# for i_ in range(4):
# print(f'res({i_}): {is_wall(12, i_)}')

arr_ = (
    (9, 1, 9, 0, 13, 0),
    (14, 1, 11, 2, 11, 4),
    ('B', 2, 11, 0, 0, 15),
    (4, 3, 9, 6, 3, 'X')
)

arr_no_way = (
    ('B', 6, 12, 15, 11),
    (8, 7, 15, 7, 10),
    (13, 7, 13, 15, 'X'),
    (11, 10, 8, 1, 3),
    (12, 6, 9, 14, 7)
)

arr_easy = (
    (4, 2, 5, 4),
    (4, 15, 11, 1),
    ('B', 9, 6, 8),
    (12, 7, 7, 'X')
)

arr_err = (  # error eliminated...
    (2, 2, 13, 12, 12),
    (4, 15, 9, 4, 13),
    (3, 13, 2, 7, 15),
    (10, 3, 15, 13, 14),
    (0, 6, 13, 9, 12),
    ('B', 7, 0, 5, 'X'),
    (6, 15, 13, 7, 7),
    (1, 10, 0, 2, 10)
)

arr_super = ((10, 5, 5, 14, 1, 12, 15, 6, 6, 4, 13, 5, 8, 8, 4, 12, 9, 3, 3, 8, 4, 13, 8, 5, 2),
             (2, 10, 4, 14, 15, 2, 5, 5, 5, 11, 0, 0, 7, 15, 2, 11, 14, 8, 3, 6, 2, 10, 4, 11, 3),
             (13, 0, 5, 3, 8, 8, 11, 7, 4, 4, 11, 15, 14, 2, 12, 13, 14, 4, 13, 13, 12, 3, 6, 10, 1),
             (8, 13, 15, 3, 14, 6, 0, 12, 1, 10, 1, 7, 0, 10, 8, 3, 3, 15, 3, 5, 5, 5, 4, 4, 14),
             (4, 12, 12, 4, 2, 6, 3, 1, 13, 5, 6, 9, 6, 8, 11, 12, 0, 1, 14, 5, 2, 6, 13, 0, 8),
             (3, 2, 10, 3, 14, 8, 11, 15, 3, 13, 4, 11, 15, 6, 4, 13, 8, 9, 12, 4, 14, 5, 9, 4, 1),
             (0, 2, 11, 3, 4, 15, 1, 5, 10, 12, 7, 2, 9, 11, 8, 9, 7, 3, 6, 0, 4, 3, 0, 13, 8),
             (1, 6, 4, 10, 14, 9, 9, 10, 8, 2, 14, 7, 7, 5, 0, 11, 6, 12, 3, 1, 13, 15, 10, 6, 3),
             (9, 10, 4, 11, 0, 15, 8, 0, 2, 4, 9, 7, 7, 3, 8, 15, 0, 12, 14, 9, 0, 2, 14, 11, 9),
             (5, 4, 14, 1, 8, 6, 11, 12, 4, 10, 3, 2, 1, 2, 2, 2, 10, 0, 1, 1, 8, 12, 12, 1, 1),
             (14, 10, 14, 6, 13, 8, 9, 6, 11, 6, 0, 11, 12, 3, 9, 4, 6, 5, 10, 4, 11, 6, 3, 8, 11),
             (11, 8, 10, 10, 12, 7, 9, 5, 11, 2, 1, 12, 1, 9, 14, 12, 3, 11, 9, 10, 12, 10, 6, 2, 13),
             (10, 0, 15, 2, 2, 6, 12, 11, 14, 11, 10, 12, 12, 0, 15, 13, 1, 10, 15, 8, 4, 1, 10, 6, 2),
             (15, 3, 11, 11, 8, 13, 1, 8, 7, 15, 1, 4, 14, 11, 15, 15, 9, 4, 5, 9, 8, 2, 4, 13, 8),
             (11, 8, 1, 8, 3, 11, 11, 12, 3, 7, 0, 13, 10, 15, 4, 3, 14, 8, 0, 2, 10, 15, 0, 15, 4),
             (13, 3, 14, 10, 13, 7, 10, 10, 14, 12, 10, 5, 14, 4, 0, 15, 1, 2, 13, 9, 10, 10, 10, 13, 2),
             (10, 3, 2, 10, 15, 0, 6, 12, 8, 1, 13, 12, 1, 2, 12, 11, 2, 14, 4, 14, 2, 9, 1, 2, 4),
             (5, 9, 1, 14, 0, 6, 7, 12, 8, 5, 8, 4, 14, 10, 15, 6, 4, 11, 8, 8, 11, 14, 7, 5, 9),
             (13, 0, 3, 7, 1, 15, 6, 5, 5, 7, 10, 1, 2, 5, 9, 13, 8, 9, 9, 11, 11, 3, 5, 9, 1),
             ('B', 13, 13, 14, 9, 2, 15, 10, 1, 6, 4, 15, 0, 0, 9, 9, 15, 15, 9, 12, 14, 6, 8, 8, 2),
             (7, 12, 12, 13, 8, 10, 4, 12, 10, 1, 2, 6, 0, 0, 9, 9, 8, 13, 4, 5, 0, 15, 4, 4, 0),
             (5, 1, 11, 8, 9, 6, 15, 3, 2, 14, 9, 0, 14, 12, 7, 1, 4, 2, 15, 13, 7, 10, 15, 13, 14),
             (10, 15, 7, 11, 2, 1, 1, 2, 9, 13, 8, 12, 12, 7, 8, 11, 8, 14, 12, 12, 15, 3, 11, 12, 8),
             (12, 2, 8, 14, 7, 13, 14, 5, 5, 12, 1, 12, 6, 15, 14, 1, 10, 1, 4, 10, 7, 9, 13, 6, 'X'),
             (1, 13, 11, 14, 3, 7, 8, 5, 12, 8, 6, 3, 11, 10, 15, 6, 10, 13, 10, 3, 11, 3, 10, 8, 11))

start = time.time_ns()
print(f'res: {maze_solver(arr_super)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
