# accepted on codewars.com approx 3.5s seconds, fast enough
import time
import heapq
import numpy as np
from itertools import permutations as perms


def four_pass(stations: list[int]):                                                   # 36 366 98 989 98989 LL
    candy_f = CandyFactory(stations)
    the_path = candy_f.solve()
    return [candy_f.get_num(node.y, node.x) for node in the_path] if the_path else None


class CandyFactory:
    # styles:
    BOLD = "\033[1m"
    # colours:
    BLACK = "\033[30m{}"
    RED = "\033[31m{}"
    GREEN = "\033[32m{}"
    YELLOW = "\033[33m{}"
    BROWN = "\033[34m{}"
    PURPLE = "\033[35m{}"
    CYAN = "\033[36m{}"
    LIGHT_GREEN = "\033[1;32m{}"
    X = "\033[37m{}"
    END = "\033[0m"

    def __init__(self, stations, j_max=10, i_max=10):
        self.COLOURS = [self.RED, self.GREEN, self.YELLOW, self.BROWN, self.PURPLE, self.CYAN, self.LIGHT_GREEN,
                        self.BLACK, self.X]
        self.J_MAX, self.I_MAX = j_max, i_max
        self.field = [[Node(j, i) for i in range(self.I_MAX)] for j in range(self.J_MAX)]
        self.max_a_star_iters = 0
        # getting neighs for all the cells on the field:
        for row in self.field:
            for node in row:
                node.get_neighs(self)
        # stations points and nodes:
        station_points = [self.get_point(s) for s in stations.copy()]
        self.station_nodes = [self.field[j][i] for (j, i) in station_points]
        self.station_pairs = [(self.station_nodes[i], self.station_nodes[i + 1], i) for i in
                              range(len(self.station_nodes) - 1)]
        self.the_shortest_possible = sum([pair[0].manhattan_distance(pair[1]) for pair in self.station_pairs]) + 1
        self.multiplier = -1

    def get_point(self, num: int):
        return divmod(num, self.I_MAX)

    def get_num(self, y: int, x: int):
        return self.I_MAX * y + x

    def get_node(self, point: tuple[int, int]):
        return self.field[point[0]][point[1]]

    # visualisation of hint method:
    def get_hint(self):
        return self.BOLD.format('') + (f"{self.BOLD + '{}'}".format(" --->>> ")).join(
            [self.colour_str_inv(f'st{i + 1}', self.COLOURS[i]) for i in
             range(len(self.station_nodes))]) + self.colour_str('', self.END)

    def solve(self):
        print(f'stations: {self.station_nodes}')
        print(f'station_pairs: {self.station_pairs}')
        perm_station_pairs = list(perms(self.station_pairs))
        # print(f'perm_station_pairs: {perm_station_pairs}')
        print(f'the shortest possible path length: {self.the_shortest_possible}')
        min_path_length = np.Infinity
        sh_p_dict = {}
        path_found_counter = 0
        # for all the permutations of the stations pairs we will be seeking for the shortest possible paths, consisting of three parts:
        for perm in perm_station_pairs:  # 36 366 98 989
            # print(f'PERM: {perm}')
            path_dicts = self.rec_path_seeker(perm, set(), {}, 0)
            for path_dict in path_dicts:
                path_found_counter += 1
                # print(f'ANOTHER ONE SOLUTION {path_found_counter} BEEN FOUND: ')
                # print(f'path_dict: {path_dict}')
                # self.show_path(path_dict)
                # path restoring from path dict:
                current_path_length = 1 + sum([len(value) for value in path_dict.values()])
                if current_path_length == self.the_shortest_possible:
                    # if we have found a path with the minimal possible length, we return it:
                    the_shortest_one = self.restore_path(path_dict)
                    print(f'the_shortest_one length: {current_path_length}')
                    self.show_path(path_dict)
                    return the_shortest_one
                elif current_path_length < min_path_length:
                    print(f'THE FIRST OR SHORTER PATH BEEN FOUND: ')
                    print(f'LENGTH: {current_path_length}')
                    self.show_path(path_dict)
                    min_path_length = current_path_length
                    sh_p_dict = path_dict.copy()
        the_shortest_one = self.restore_path(sh_p_dict)
        # the shortest path found:
        print(f'the_shortest_one length: {len(the_shortest_one)}')
        self.show_path(sh_p_dict)
        print(f'HINT: {self.get_hint()}')
        print(f'max_a_star_iters: {self.max_a_star_iters}')
        return the_shortest_one

    def restore_path(self, path_dict):
        return [self.station_nodes[0]] + sum([path_dict[k] for k in range(len(self.station_pairs))],
                                             []) if path_dict else []

    # just for the visualization:
    def show_path(self, path_dict: dict[int, list['Node']]):
        for row in self.field:
            for node in row:
                if node in self.station_nodes:
                    print(f'{self.station_nodes.index(node) + 1}', end=' ')
                else:
                    for key in path_dict.keys():
                        if node in path_dict[key]:
                            self.colour_print('p', self.COLOURS[key])
                            break
                    else:
                        print(f'.', end=' ')
            print()
        print()

    # colour printing/returning and colour reset methods:
    def colour_print(self, char, colour):
        print((self.BOLD + colour.format(char) + self.END), end=' ')

    def colour_str(self, char, colour):
        return (self.BOLD + colour + self.END).format(char)

    def colour_str_inv(self, char, colour):
        return char + (self.BOLD + colour).format('')

    def rec_path_seeker(self, permutation: tuple['Node', 'Node', int], used_nodes: set['Node'],
                        path_dict: dict[int: list['Node']], path_parts_complete: int):
        # print(f'depth: {path_parts_complete}')
        # self.show_path(path_dict)
        if path_parts_complete == len(self.station_pairs):
            # base case (a whole path exists):
            yield path_dict.copy()
            return
        # priority deviation of goal vector (left or right):
        for i in range(2):
            self.multiplier *= -1
            # pathfinding:
            path_part = permutation[path_parts_complete][0].a_star(permutation[path_parts_complete][1], used_nodes,
                                                                   self)
            if len(path_part) > 1:
                # path dict building:
                key = permutation[path_parts_complete][2]
                path_dict[key] = (p := path_part[1:])
                yield from self.rec_path_seeker(permutation, used_nodes | set(p), path_dict, path_parts_complete + 1)
                path_dict.pop(key)

    def clear(self):
        for row in self.field:
            for node in row:
                node.clear()


class Node:
    walk = [(dy, dx) for dy in range(-1, 2) for dx in range(-1, 2) if dy * dx == 0 and (dy, dx) != (0, 0)]

    def __init__(self, y, x):
        self.y, self.x = y, x
        self.previously_visited_node = None
        self.neighs = []
        self.passability = True
        # move cost:
        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        # tie-breaker, used and works if and only if when f(node1) == f(node2):
        self.vector_cross_deviation = np.Infinity  # vector-cross product deviation of a path from the line start -->> finish
        # heuristic:
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or the main priority total cost of the current Node is not needed here

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)

    def __lt__(self, other):
        # if f = g + h values for 2 nodes are the same -->> we compare vector_cross_deviations for two nodes:
        return (self.g + self.h, self.vector_cross_deviation) < (other.g + other.h, other.vector_cross_deviation)

    def __hash__(self):
        return hash((self.y, self.x))

    def __str__(self):
        return f'{self.y, self.x}'

    def __repr__(self):
        return str(self)

    def clear(self):
        self.previously_visited_node = None
        self.g = np.Infinity
        self.vector_cross_deviation = np.Infinity
        self.h = 0

    def get_neighs(self, candy_factory: 'CandyFactory'):
        for dy, dx in self.walk:
            new_j, new_i = self.y + dy, self.x + dx
            if 0 <= new_j < candy_factory.J_MAX and 0 <= new_i < candy_factory.I_MAX:
                self.neighs.append(candy_factory.field[new_j][new_i])

    def manhattan_distance(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def can_reach(self, other):
        pass

    # a star with scalar-deviation tiebreaker:
    def a_star(self, other: 'Node', used_nodes: set['Node'], candy_factory: 'CandyFactory'):
        iters = 0
        nodes_to_be_visited = [self]
        forbidden_nodes = {node for node in candy_factory.station_nodes if node != other}
        self.g = 0
        heapq.heapify(nodes_to_be_visited)
        # main cycle:
        while nodes_to_be_visited:
            iters += 1
            # if iters % 1000 == 0:
            #     print(f'iters: {iters}')
            curr_node = heapq.heappop(nodes_to_be_visited)
            # print(f'{iters}th iteration')  # , now entering node: {curr_node}
            # stop condition of finding the shortest path:
            if curr_node == other:
                candy_factory.max_a_star_iters = max(candy_factory.max_a_star_iters, iters)
                break
            # next step of a-star:
            for neigh in curr_node.neighs:
                if neigh not in used_nodes and neigh not in forbidden_nodes:
                    # nonsense, but it works...
                    y, x = other.y - self.y, other.x - self.x
                    dy, dx = neigh.y - self.y, neigh.x - curr_node.x
                    # at first, it was vector-cross product of the vector between start and finish points and the vector, co-directional with the current direction of movement:
                    vector_cross_product = candy_factory.multiplier * (y * dx - x * dy)
                    # vector_cross_product is used as a tiebreaker for screening out lots of heuristically equals paths:
                    if (neigh.g, vector_cross_product) > (curr_node.g + 1, curr_node.vector_cross_deviation):
                        neigh.g = curr_node.g + 1
                        neigh.vector_cross_deviation = vector_cross_product
                        neigh.h = neigh.manhattan_distance(other)
                        neigh.previously_visited_node = curr_node
                        heapq.heappush(nodes_to_be_visited, neigh)
        # the first cell for path-restoring (from the end)
        node = other
        shortest_path = []
        # path restoring (here we get the reversed path)
        while node.previously_visited_node:
            shortest_path.append(node)
            node = node.previously_visited_node
        # and the last (the start etc.) cell:
        shortest_path.append(self)
        # clearing the nodes:
        candy_factory.clear()
        # returning the reversed shortest path:
        return list(reversed(shortest_path))


cf1 = CandyFactory([1, 69, 95, 70])
cf2 = CandyFactory([0, 49, 40, 99])
cf3 = CandyFactory([37, 61, 92, 36])
cf4 = CandyFactory([51, 24, 75, 57])
cf5 = CandyFactory([92, 59, 88, 11])
cf6 = CandyFactory([43, 55, 44, 45])
cf7 = CandyFactory([44, 72, 61, 67])
cf8 = CandyFactory([91, 85, 94, 22])
cf9 = CandyFactory([59, 90, 10, 31])
cf10 = CandyFactory([81, 10, 14, 98])
cf12 = CandyFactory([89, 66, 75, 59])
cf13 = CandyFactory([1, 624, 2, 979, 1000, 328, 213], 28,
                    36)  # approx 15 minutes of calcs with all printing... 36 366 98 989
cf = CandyFactory([1, 111, 223, 2, 198, 145, 95], 18, 18)
cf15 = CandyFactory([43, 29, 14, 39])
cf16 = CandyFactory([94, 90, 75, 92])
cf17 = CandyFactory([59, 12, 20, 39])
cf18 = CandyFactory([32, 27, 92, 38])
cf19 = CandyFactory([1704, 2849, 1198, 2500, 2288, 2348, 809, 178], 29, 100)  # too much time...

# cf = CandyFactory()
# cf = CandyFactory()
# cf = CandyFactory()
start = time.time_ns()
cfcf = CandyFactory([44, 72, 61, 67])
path = cf.solve()
print(f'PATH: {path}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# print(f'PATTERNS: {CandyFactory.PATTERNS}')
