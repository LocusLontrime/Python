# accepted on codewars.com
import heapq
import numpy as np


def find_shortest_path(grid, start_node, end_node):
    # print_grid(grid, start_node, end_node)

    # border cases:
    if len(grid) == 0 or len(grid[0]) == 0:
        return []
    elif len(grid) == len(grid[0]) == 1:
        if start_node is not None:
            return [start_node]

    print(f'grid_height: {len(grid)}, grid_width: {len(grid[0])}')

    def calc_manhattan_heuristic(node_1, node_2):
        return abs(node_1.position.x - node_2.position.x) + abs(node_1.position.y - node_2.position.y)

    conv = convert_grid(grid, start_node, end_node)
    path = a_star(conv[0], conv[1], conv[2], calc_manhattan_heuristic)

    return convert_path_back(grid, [node.position for node in path])


def a_star(grid, start_node, end_node, heuristic):
    vertexes_to_be_visited = [start_node]
    start_node.g = 0

    heapq.heapify(vertexes_to_be_visited)

    while len(vertexes_to_be_visited) > 0:
        curr_node = heapq.heappop(vertexes_to_be_visited)

        # stop condition, here we reach the ending point
        if curr_node == end_node:
            break

        # here we're looking for all the adjacent and passable nodes for a current node and pushing them to the heap (priority queue)
        for next_possible_node in get_adjacent_ones(grid, curr_node):
            if next_possible_node.g > curr_node.g + 1:  # a kind of dynamic programming
                next_possible_node.g = curr_node.g + 1  # every step distance from one node to an adjacent one is equal to 1
                next_possible_node.h = heuristic(next_possible_node, end_node)  # heuristic function,
                # needed for sorting the nodes to be visited in priority order
                next_possible_node.previously_visited_node = curr_node  # constructing the path
                heapq.heappush(vertexes_to_be_visited, next_possible_node)  # adding node to the heap

    # the last point of the path found
    node = end_node
    reversed_shortest_path = []

    # path restoring (here we get the reversed path)
    while node.previously_visited_node:
        reversed_shortest_path.append(node)
        node = node.previously_visited_node

    reversed_shortest_path.append(start_node)

    # returning the right shortest path
    return list(reversed(reversed_shortest_path))


# looks for all the adjacent and passable nodes
def get_adjacent_ones(grid, node):
    list_of_adj_nodes = []

    x, y = node.position.x, node.position.y

    if x > 0 and (n := grid[y][x - 1]).passable:
        list_of_adj_nodes.append(n)

    if x < len(grid[0]) - 1 and (n := grid[y][x + 1]).passable:
        list_of_adj_nodes.append(n)

    if y > 0 and (n := grid[y - 1][x]).passable:
        list_of_adj_nodes.append(n)

    if y < len(grid) - 1 and (n := grid[y + 1][x]).passable:
        list_of_adj_nodes.append(n)

    return list_of_adj_nodes


# simple class for Node's coordinate pair representation
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x},{self.y})'


# class, describing the node's signature
class Node:

    def __init__(self, x, y, passability=True):
        self.position = Point(x, y)  # (2,5)
        self.passable = passability  # says if a cell is a wall or a path
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one

        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or total cost of the current Node is not needed here

    def __eq__(self, other):
        return self.position == other.position

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other):
        return self.h + self.g < other.h + other.g  # the right sigh is "-" for __lt__() method


# converts a grid of nodes from codewars to a convenient grid of Nodes, using extended Node-class
def convert_grid(grid, start_node, end_node):
    converted_grid = [[Node(i, j, grid[j][i].passable) for i in range(len(grid[0]))] for j in range(len(grid))]
    converted_start_node, converted_end_node = converted_grid[start_node.position.x][start_node.position.y], \
                                               converted_grid[end_node.position.x][end_node.position.y]

    return converted_grid, converted_start_node, converted_end_node


# converts the shortest path found to the list of initial nodes from the grid given
def convert_path_back(grid, path):
    return [grid[point.y][point.x] for point in path]
