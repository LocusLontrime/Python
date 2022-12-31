# accepted on codewars.com approx 8-9 seconds, need to be optimized a bit
import time
import heapq
import numpy as np
from itertools import permutations as perms


def four_pass(stations: list[int]):
    the_path = CandyFactory(stations).solve()
    return [CandyFactory.get_num(node.y, node.x) for node in the_path] if the_path else None


class CandyFactory:
    J_MAX, I_MAX = 9, 9
    PARTS = [(1, 2), (2, 3), (3, 4)]

    def __init__(self, stations):
        self.field = [[Node(j, i) for i in range(self.J_MAX + 1)] for j in range(self.I_MAX + 1)]
        # getting neighs for all the cells on the field:
        for row in self.field:
            for node in row:
                node.get_neighs(self)
        # stations points and nodes:
        station_points = [self.get_point(s) for s in stations.copy()]
        self.station_nodes = [self.field[j][i] for (j, i) in station_points]
        self.station_pairs = [(self.station_nodes[i], self.station_nodes[i + 1], i) for i in range(len(self.station_nodes) - 1)]
        self.the_shortest_possible = sum([pair[0].manhattan_distance(pair[1]) for pair in self.station_pairs]) + 1
        self.multiplier = -1

    @staticmethod
    def get_point(num: int):
        return num // 10, num % 10

    @staticmethod
    def get_num(y: int, x: int):
        return 10 * y + x

    def get_node(self, point: tuple[int, int]):
        return self.field[point[0]][point[1]]

    def solve(self):
        print(f'stations: {self.station_nodes}')
        print(f'station_pairs: {self.station_pairs}')
        perm_station_pairs = list(perms(self.station_pairs))
        print(f'perm_station_pairs: {perm_station_pairs}')
        shortest_paths = []
        print(f'the shortest possible path length: {self.the_shortest_possible}')
        # for all the permutations of the stations pairs we will be seeking for the shortest possible paths, consisting of three parts:
        for perm in perm_station_pairs:
            print(f'PERM: {perm}')
            path_dicts = self.rec_path_seeker(perm, [], {}, 0)
            for path_dict in path_dicts:
                print(f'path_dict: {path_dict}')
                # path restoring from path dict:
                a_path = [self.station_nodes[0]] + sum([path_dict[k] for k in range(len(self.station_pairs))], [])
                if len(a_path) == self.the_shortest_possible:
                    # if we have found a path with the minimal possible length, we return it:
                    print(f'the_shortest_one length: {len(a_path)}')
                    self.show_path(a_path)
                    return a_path
                shortest_paths.append(a_path)
        print(f'all candidates to be the shortest path: ')
        for shortest_path in shortest_paths:
            print(f'POSSIBLE SHORTEST PATH of length {len(shortest_path)}: ')
            self.show_path(shortest_path)
        # the shortest path found:
        the_shortest_one = list(sorted(shortest_paths, key=lambda k: len(k))[0] if shortest_paths else [])
        print(f'the_shortest_one length: {len(the_shortest_one)}')
        self.show_path(the_shortest_one)
        return the_shortest_one

    # just for the visualization:
    def show_path(self, path_to_be_shown: list['Node']):
        for row in self.field:
            for node in row:
                if node in self.station_nodes:
                    print(f'{self.station_nodes.index(node) + 1}', end=' ')
                elif node in path_to_be_shown:
                    print(f'p', end=' ')
                else:
                    print(f'.', end=' ')
            print()
        print()

    def rec_path_seeker(self, permutation: tuple['Node', 'Node', int], used_nodes: list['Node'], path_dict: dict[int: list['Node']], path_parts_complete: int):
        if path_parts_complete == 3:
            # base case (a whole path exists):
            yield path_dict.copy()
            return
        # priority deviation of goal vector (left or right):
        for i in range(2):
            self.multiplier *= -1
            # pathfinding:
            path_part = permutation[path_parts_complete][0].a_star(permutation[path_parts_complete][1], used_nodes, self)
            if len(path_part) > 1:
                print(f'{path_parts_complete}th path_part: {path_part}')
                self.show_path(path_part)
                # path dict building:
                key = permutation[path_parts_complete][2]
                path_dict[key] = (p := path_part[1:])
                yield from self.rec_path_seeker(permutation, used_nodes + p, path_dict, path_parts_complete + 1)
                path_dict.pop(key)

    def clear(self):
        for row in self.field:
            for node in row:
                node.clear()

    @staticmethod
    def is_valid(j, i):
        pass


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

    def __hash__(self):
        return hash((self.y, self.x))

    def __lt__(self, other):
        # if f = g + h values for 2 nodes are the same -->> we compare vector_cross_deviations for two nodes:
        return (self.g + self.h, self.vector_cross_deviation) < (other.g + other.h, other.vector_cross_deviation)

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
            if 0 <= new_j <= CandyFactory.J_MAX and 0 <= new_i <= CandyFactory.I_MAX:
                self.neighs.append(candy_factory.field[new_j][new_i])

    def manhattan_distance(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def can_reach(self, other):
        pass

    # a star with scalar-deviation tiebreaker:
    def a_star(self, other: 'Node', used_nodes: list['Node'], candy_factory: 'CandyFactory'):
        iters = 0
        nodes_to_be_visited = [self]
        self.g = 0
        heapq.heapify(nodes_to_be_visited)
        # main cycle:
        while nodes_to_be_visited:
            iters += 1
            curr_node = heapq.heappop(nodes_to_be_visited)
            # print(f'{iters}th iteration')  # , now entering node: {curr_node}
            # stop condition of finding the shortest path:
            if curr_node == other:
                break
            # next step of a-star:
            for neigh in curr_node.neighs:
                if neigh not in used_nodes and neigh not in [node for node in candy_factory.station_nodes if node != other]:
                    y, x = other.y - self.y, other.x - self.x
                    dy, dx = neigh.y - curr_node.y, neigh.x - curr_node.x
                    # vector-cross product of the vector between start and finish points and the vector, co-directional with the current direction of movement:
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

    def bypass(self, other, obstacle):
        pass


# print(f'{four_pass([1, 69, 95, 70])}')

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
cf11 = CandyFactory([43, 45, 94, 71])
cf = CandyFactory([89, 66, 75, 59])


# cf = CandyFactory()
# cf = CandyFactory()
# cf = CandyFactory()
start = time.time_ns()
cfcf = CandyFactory([44, 72, 61, 67])
path = cf.solve()
print(f'PATH: {path}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 3} microseconds')

# print(f'PATTERNS: {CandyFactory.PATTERNS}')


