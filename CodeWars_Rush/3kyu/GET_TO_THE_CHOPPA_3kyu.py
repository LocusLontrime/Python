import heapq
import math
from heapq import heapify
from heapq import heappush
from heapq import heappop
import numpy as np


def find_shortest_path(grid, start_node, end_node):

    def choose_heuristic():
        def calc_manhattan_heuristic(node_1, node_2):
            return abs(node_1.position[0] - node_2.position[0]) + abs(node_1.position[1] - node_2.position[1])

        def calc_euclidian_heuristic(node_1, node_2):
            return math.sqrt((node_1.position[0] - node_2.position[0]) ** 2 + (node_1.position[1] - node_2.position[1]) ** 2)

        def calc_no_heuristic(node_1, node_2):
            return 0

        heuristics = {1: calc_manhattan_heuristic, 2: calc_euclidian_heuristic, 3: calc_no_heuristic}
        heur_names = ['Manhattan', 'Euclidian', 'No']

        for i in range(len(heur_names)):
            print(f'press {i + 1} for <{heur_names[i]} heuristic>')

        string = input()
        if string in [str(_ + 1) for _ in range(len(heur_names))]:
            print(f'{heur_names[(i := int(string)) - 1]} heuristic been chosen')
            return heuristics[i]
        else:
            print('Please, press 1, 2, or 3 for heuristic choice')
            choose_heuristic()

    heuristic = choose_heuristic()

    print(f'start_node: {start_node}, end_node: {end_node}')

    print(f'grid: {grid}')

    path = a_star(grid, start_node, end_node, heuristic)

    print(f"The shortest path's length: {len(path)}")

    return [node.position for node in path]


def a_star(grid, start_node, end_node, heuristic):

    vertexes_to_be_visited = [start_node]
    start_node.g = 0

    heapq.heapify(vertexes_to_be_visited)

    iterations = 0

    while len(vertexes_to_be_visited) > 0:
        curr_node = heapq.heappop(vertexes_to_be_visited)
        # just a number of a-star iterations needed for building the shortest path from starting node to the ending one
        iterations += 1
        print(f'curr node x, y: ({curr_node.position[0]}, {curr_node.position[1]}), iteration: {iterations}')

        # stop condition, here we reach the ending point
        if curr_node == end_node:
            print(f'The path is done in {iterations} iterations')
            break

        # here we're looking for all the adjacent and passable nodes for a current node and pushing them to the heap (priority queue)
        for next_possible_node in get_adjacent_ones(grid, curr_node):
            if not next_possible_node.is_visited:
                if next_possible_node.g > curr_node.g + 1:  # a kind of dynamic programming
                    next_possible_node.g = curr_node.g + 1   # every step distance from one node to an adjacent one is equal to 1
                    next_possible_node.h = heuristic(next_possible_node, end_node)  # heuristic function,
                    # needed for sorting the nodes to be visited in priority order
                    next_possible_node.is_visited = True  # this node has just been visited
                    next_possible_node.previously_visited_node = curr_node  # constructing the path
                    heapq.heappush(vertexes_to_be_visited, next_possible_node)  # adding node to the heap

    # the last point of the path found
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


# looks for all the adjacent and passable nodes
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


# not needed for the time being
def is_position_valid():
    pass


# class, describing the node's signature
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
        return self.h < other.h  # the right sigh is "-" for __lt__() method


# creates a testing grid
def create_grid():

    # just a shaped grid with all passable nodes
    grid = [[Node(i, j) for j in range(8)] for i in range(11)]

    # generating obstacles
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


# the main method call
print(find_shortest_path((c := create_grid()), c[0][0], c[10][7]))


