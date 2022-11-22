import heapq
import math
from heapq import heapify
from heapq import heappush
from heapq import heappop
import numpy as np


def find_shortest_path(grid, start_node, end_node):

    print(f'start_node: {start_node}, end_node: {end_node}')

    print(f'grid: {grid}')

    path = a_star(grid, start_node, end_node)

    print(f"The shortest path's length: {len(path)}")

    return path


def a_star(grid, start_node, end_node):

    vertexes_to_be_visited = [start_node]
    start_node.g = 0

    heapq.heapify(vertexes_to_be_visited)

    while len(vertexes_to_be_visited) > 0:
        curr_node = heapq.heappop(vertexes_to_be_visited)

        print(f'curr node x, y: ({curr_node.position[0]}, {curr_node.position[1]})')

        # stop condition, here we reach the ending point
        if curr_node == end_node:
            print(f'The path is done')
            break

        for next_possible_node in get_adjacent_ones(grid, curr_node):
            if not next_possible_node.is_visited:
                if next_possible_node.g > curr_node.g + 1:
                    next_possible_node.g = curr_node.g + 1
                    next_possible_node.h = calc_manhattan_heuristic(next_possible_node, end_node)
                    next_possible_node.is_visited = True
                    next_possible_node.previously_visited_node = curr_node
                    heapq.heappush(vertexes_to_be_visited, next_possible_node)

    node = end_node
    print(f'node: {node.position}')
    reversed_shortest_path = []

    # path restoring (here we get the reversed path)
    while node.previously_visited_node:
        reversed_shortest_path.append(node)
        node = node.previously_visited_node

    print(f'reversed_shortest_path: {reversed_shortest_path}')

    # returning the right shortest path
    return list(reversed(reversed_shortest_path))


def get_adjacent_ones(grid, node):
    list_of_adj_nodes = []

    x, y = node.position[0], node.position[1]

    if x > 0 and (n := grid[x - 1][y]).passable:
        list_of_adj_nodes.append(n)

    if x < len(grid) - 1 and (n := grid[x + 1][y]).passable:
        list_of_adj_nodes.append(n)

    if y > 0 and (n := grid[x][y - 1]).passable:
        list_of_adj_nodes.append(n)

    if y < len(grid[0]) - 1 and (n := grid[x][y + 1]).passable:
        list_of_adj_nodes.append(n)

    return list_of_adj_nodes


def calc_manhattan_heuristic(node_1, node_2):
    return abs(node_1.position[0] - node_2.position[0]) + abs(node_1.position[1] - node_2.position[1])


def calc_euclidian_heuristic(node_1, node_2):
    return math.sqrt((node_1.position[0] - node_2.position[0]) ** 2 + (node_1.position[1] - node_2.position[1]) ** 2)


# not needed for the time being
def is_position_valid():
    pass


class Node:

    def __init__(self, x, y, passability=True):
        self.position = (x, y)  # (2,5)

        self.passable = passability  # says if a cell is a wall or a path

        self.is_visited = False  # flag of visiting the current node

        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one

        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or total cost of the current Node is not needed here

    def __eq__(self, other):
        return self.position == other.position

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other):
        return self.h > other.h


def create_grid():

    grid = [[Node(i, j) for j in range(8)] for i in range(11)]

    grid[1][0].passable = False
    grid[1][1].passable = False
    grid[1][2].passable = False
    grid[2][2].passable = False
    grid[3][2].passable = False
    grid[3][0].passable = False
    grid[4][0].passable = False
    grid[5][0].passable = False
    grid[5][1].passable = False
    grid[5][2].passable = False
    grid[5][3].passable = False
    grid[5][4].passable = False
    grid[5][5].passable = False
    grid[3][4].passable = False
    grid[2][4].passable = False
    grid[1][4].passable = False
    grid[1][5].passable = False
    grid[1][6].passable = False
    grid[2][6].passable = False
    grid[3][6].passable = False
    grid[4][7].passable = False
    grid[5][7].passable = False
    grid[6][7].passable = False
    grid[7][7].passable = False
    grid[7][6].passable = False
    grid[7][5].passable = False
    grid[7][4].passable = False
    # grid[8][4].passable = False
    grid[7][0].passable = False
    grid[7][1].passable = False
    grid[9][1].passable = False
    grid[9][2].passable = False
    grid[9][3].passable = False
    grid[9][6].passable = False
    grid[10][5].passable = False

    print(f'grid been built')

    return grid


print(find_shortest_path((c := create_grid()), c[0][0], c[10][7]))


