# accepted on codewars.com
import heapq
import numpy as np


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
names = ['up', 'right', 'down', 'left']


def cheapest_path(t, start, finish):
    # a star implementation
    if len(t) == 0 or len(t[0]) == 0:
        return []

    grid_of_nodes = [[Node(j, i, t[j][i]) for i in range(len(t[0]))] for j in range(len(t))]

    path = a_star(grid_of_nodes, grid_of_nodes[finish[0]][finish[1]], grid_of_nodes[start[0]][start[1]])

    moves = []
    for ind, node in enumerate(path):
        if ind + 1 < len(path):
            moves.append(get_move(node, path[ind + 1]))

    return moves


def manhattan_heuristic(node1: 'Node', node2: 'Node'):
    return abs(node1.position.y - node2.position.y) + abs(node1.position.x - node2.position.x)


def a_star(grid: list[list['Node']], start: 'Node', finish: 'Node'):
    nodes_to_be_visited = [start]
    start.g = 0
    heapq.heapify(nodes_to_be_visited)

    while nodes_to_be_visited:
        curr_node = heapq.heappop(nodes_to_be_visited)

        if curr_node == finish:
            break

        for neigh in get_adjacent_ones(grid, curr_node):
            if neigh.g > curr_node.g + neigh.val:
                neigh.g = curr_node.g + neigh.val
                neigh.h = manhattan_heuristic(neigh, finish)
                neigh.previously_visited_node = curr_node
                heapq.heappush(nodes_to_be_visited, neigh)

    node = finish

    shortest_path = []

    # path restoring (here we get the reversed path)
    while node.previously_visited_node:
        shortest_path.append(node)
        node = node.previously_visited_node

    shortest_path.append(start)

    return list(shortest_path)


def get_adjacent_ones(grid: list[list['Node']], node: 'Node'):
    list_of_adj_nodes = []
    y, x = node.position.y, node.position.x
    for (j, i) in directions:
        # print(f'j, i: {j, i}')
        neigh_j, neigh_i = y + j, x + i
        if 0 <= neigh_j < len(grid) and 0 <= neigh_i < len(grid[0]) and not node.is_visited:
            neigh = grid[neigh_j][neigh_i]
            list_of_adj_nodes.append(neigh)
    return list_of_adj_nodes


def get_move(node1: 'Node', node2: 'Node'):
    j, i = node2.position.y - node1.position.y, node2.position.x - node1.position.x
    index = directions.index((j, i))
    return names[index]


# simple class for Node's coordinate pair representation
class Point:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.y},{self.x})'


# class, describing the node's signature
class Node:
    def __init__(self, y, x, val):
        self.position = Point(y, x)  # (2,5)
        self.val = val
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one
        self.is_visited = False  # flag of visiting the node (???)

        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or total cost of the current Node is not needed here

    def __eq__(self, other):
        return self.position == other.position

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other):
        return self.h + self.g < other.h + other.g  # the right sigh is "<" for __lt__() method


grid_ex = [
    [9, 1, 1, 1, 7, 8, 9, 3, 6],
    [5, 1, 7, 6, 6, 5, 4, 9, 9],
    [9, 1, 1, 1, 1, 3, 5, 5, 9],
    [9, 9, 9, 9, 1, 6, 9, 9, 5],
    [6, 6, 1, 1, 1, 7, 9, 1, 9],
    [5, 3, 1, 9, 9, 6, 8, 1, 7],
    [7, 7, 1, 7, 9, 6, 7, 1, 6],
    [8, 7, 1, 1, 1, 1, 1, 1, 8],
    [9, 9, 7, 3, 6, 4, 3, 6, 9]
]

grid_m = [
    [1, 19, 1, 1, 1],
    [1, 19, 1, 19, 1],
    [1, 19, 1, 19, 1],
    [1, 19, 1, 19, 1],
    [1, 1, 1, 19, 1]
]

# print(cheapest_path(grid_ex, (0, 1), (4, 7)))
print(cheapest_path(grid_m, (0, 0), (4, 4)))


