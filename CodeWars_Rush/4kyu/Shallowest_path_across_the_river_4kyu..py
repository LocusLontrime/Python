# accepted on codewars.com
import heapq
from numpy import Infinity as inf

# threshold for priority calculating function
THRESHOLD = 100

dirs = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]


def shallowest_path(river):
    global THRESHOLD
    # river sizes, not included
    max_y, max_x = len(river), len(river[0])

    # next possible nodes:
    def find_neighbours(y: int, x: int):
        for direction in dirs:
            neigh_y, neigh_x = y + direction[0], x + direction[1]
            if 0 <= neigh_y < max_y and 0 <= neigh_x < max_x:
                grid[y][x].neighbours.append(grid[neigh_y][neigh_x])

    # path restoring:
    def get_path(node: 'Node'):
        path_restored = []
        current_node = node
        while current_node is not None:
            path_restored.append(current_node)
            current_node = current_node.prev_node
        # path reversing
        return list(reversed(path_restored))

    def clear(grid_of_nodes: list[list['Node']]):
        for y in range(max_y):
            for x in range(max_x):
                grid_of_nodes[y][x].distance_to = inf
                grid_of_nodes[y][x].prev_node = None
                grid_of_nodes[y][x].heuristic_distance = 0
                grid_of_nodes[y][x].max_path_depth = 0

    def calc_manhattan_horizontal_distance(current_node: 'Node'):
        return abs(current_node.coords.x - (max_x - 1))

    # building grid of Nodes:
    grid = [[Node(river[y][x], Point(y, x)) for x in range(max_x)] for y in range(max_y)]
    # searching for the neighbours:
    for y in range(max_y):
        for x in range(max_x):
            find_neighbours(y, x)
    # a-star implementation of search for the shallowest pass across the river:
    # 1. creating the heaps for the all possible starting nodes (that are located on the left beach of the river):
    nodes_to_be_visited_all_starting_points = [[grid[y][0]] for y in range(max_y)]
    # all the shallowest paths:
    shallowest_paths = []
    i = 0
    lowest_max_depth = inf
    for nodes_to_be_visited in nodes_to_be_visited_all_starting_points:
        # the start point has a zero-distance:
        nodes_to_be_visited[0].distance_to = 0
        nodes_to_be_visited[0].max_path_depth = nodes_to_be_visited[0].depth
        heapq.heapify(nodes_to_be_visited)
        # print(f'initial node: {nodes_to_be_visited[0]}')
        # 2. a star itself:
        while len(nodes_to_be_visited) > 0:
            # here we take the current node from heapified nodes_to_be_visited list:
            curr_node = heapq.heappop(nodes_to_be_visited)
            # print(f'Node: {curr_node}')
            # end-condition:
            if curr_node.coords.x == max_x - 1:
                print(f'FINISH!')
                # adding the shallowest path found to the results
                shallowest_paths.append((get_path(curr_node), d := curr_node.max_path_depth))
                lowest_max_depth = min(lowest_max_depth, d)
                break

            # cycling all over the possible neighbours:
            for neigh in curr_node.neighbours:
                # print(f"neigh: {neigh}, neigh's distance: {neigh.distance_to}, curr node: {curr_node}, curr node's distance: {curr_node.distance_to}")
                # condition of no return to visited nodes:
                if neigh.distance_to > curr_node.distance_to + 1:
                    # print(f'lala')
                    neigh.distance_to = curr_node.distance_to + 1
                    # print(f"neigh's new distance: {neigh.distance_to}")
                    neigh.heuristic_distance = calc_manhattan_horizontal_distance(neigh)
                    # transmits the max depth to the next node or changes it if the neigh's depth is bigger than the current max depth:
                    if neigh.depth > curr_node.max_path_depth:
                        neigh.max_path_depth = neigh.depth
                    else:
                        neigh.max_path_depth = curr_node.max_path_depth
                    # path memoization, needed for the path restoration
                    neigh.prev_node = curr_node
                    heapq.heappush(nodes_to_be_visited, neigh)

        # all the grid nodes' attributes gets reset to their default values:
        clear(grid)
        i += 1

    # now we are searching for the shallowest path among all the paths found
    # 1. filtering out the paths with min max depth
    for path in shallowest_paths:
        print(path)
    # 2. finding and returning the shortest one:
    the_shallowest_path_of_nodes = list(sorted([path for path in shallowest_paths if path[1] == lowest_max_depth], key=lambda x: len(x[0])))[0][0]
    return [(node.coords.y, node.coords.x) for node in the_shallowest_path_of_nodes]


class Node:
    # initialization:
    def __init__(self, depth: int, coords: 'Point'):
        # base attributes:
        self.depth = depth
        self.coords = coords
        # attributes from a star section:
        self.max_path_depth = 0  # ???
        self.distance_to = inf
        self.heuristic_distance = 0
        self.prev_node = None
        self.neighbours: list['Node'] = list()

    def __repr__(self):
        return f'{str(self.coords)}[{self.depth}]'

    def __str__(self):
        return f'{str(self.coords)}[{self.depth}]'

    # needed for prioritizing the nodes in heapq:
    def __lt__(self, other):
        self_val = THRESHOLD * self.max_path_depth + self.heuristic_distance + self.distance_to
        other_val = THRESHOLD * other.max_path_depth + other.heuristic_distance + other.distance_to
        # print(f'self_val" {self_val}, other_val: {other_val}')
        return self_val < other_val  # self.distance_to ???


class Point:
    # initialization:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __repr__(self):
        return f'({self.y}, {self.x})'

    def __str__(self):
        return f'({self.y}, {self.x})'


arr = [
    [2, 3, 2],
    [1, 1, 4],
    [9, 5, 2],
    [1, 4, 4],
    [1, 5, 4],
    [2, 1, 4],
    [5, 1, 2],
    [5, 5, 5],
    [8, 1, 9]
]

arr_x = [
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 1, 1, 1, 1, 1, 1, 1, 1],
    [8, 8, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 1, 1, 1, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 1, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 1, 8, 8, 8, 8, 8],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 8],
    [8, 8, 1, 8, 8, 8, 8, 8, 1, 8],
    [8, 8, 1, 8, 8, 8, 8, 8, 1, 8],
    [8, 8, 1, 1, 1, 1, 1, 1, 1, 8]
]

arr_y = [
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 5, 5, 5, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7, 7],
    [5, 5, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 5, 5, 5, 5, 5, 5, 5],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]

one_cell = [[3]]

print(f'The shallowest_path: {shallowest_path(arr_y)}')
