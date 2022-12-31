import heapq
import numpy as np


def four_pass(stations: list[int]):
    the_path = CandyFactory(stations).solve()
    return [CandyFactory.get_num(y, x) for (y, x) in the_path]


class CandyFactory:
    J_MAX, I_MAX = 9, 9
    PARTS = [(1, 2), (2, 3), (3, 4)]
    PATTERNS = [
        [(2, 1, 3, 1), (3, 4, 2, 1), (2, 3, None, 1)],
        [(3, 4, 2, 1), (2, 1, 3, 1), (2, 3, None, 1)],
        [(1, 2, None, 1), (2, 3, None, 1), (3, 4, None, 1)],
        [(3, 4, None, 1), (2, 3, None, 1), (1, 2, None, 1)],
        [(2, 3, 4, 1), (3, 4, 2, 1), (1, 2, 3, 1)],
        [(2, 3, 1, 1), (1, 2, 3, 1), (3, 4, 2, 1)]

    ]

    def __init__(self, stations):
        self.field = [[Node(j, i) for i in range(self.J_MAX + 1)] for j in range(self.I_MAX + 1)]
        # getting neighs for all the cells on the field:
        for row in self.field:
            for node in row:
                node.get_neighs(self)
        # stations points:
        self.station_points = [self.get_point(s) for s in stations.copy()]
        # here the result path will be built:
        self.shortest_path = []
        self.MULTIPLIER = -1

    @staticmethod
    def get_point(num: int):
        return num // 10, num % 10

    @staticmethod
    def get_num(y: int, x: int):
        return 10 * y + x

    def get_node(self, point: tuple[int, int]):
        return self.field[point[0]][point[1]]

    def solve(self):
        print(f'station_points: {self.station_points}')
        the_shortest_ones = []
        for i, pattern in enumerate(self.PATTERNS):
            for iteration in [0, 1]:
                self.shortest_path = []
                the_shortest_ones.append([])
                self.MULTIPLIER *= -1
                print(f'PATTERN: {pattern}, iteration: {iteration}, MULTIPLIER: {self.MULTIPLIER}')
                for ind, trio in enumerate(pattern):
                    curr_path = self.get_node(self.station_points[trio[0] - 1]).a_star(
                        self.get_node(self.station_points[trio[1] - 1]), self,
                        None if trio[2] is None else self.get_node(self.station_points[trio[2] - 1]), trio[3])
                    print(f'current path: {curr_path}')
                    if len(curr_path) > 1:
                        self.shortest_path += curr_path[(1 if ind in [0, 1] else 0):]
                        the_shortest_ones[i * 2 + iteration].append(curr_path)
                    else:
                        self.shortest_path = []
                        break
                print(f'shortest path len={len(self.shortest_path)}: {self.shortest_path}')

        shortest_paths = []
        print(f"the_shortest_ones' length: {len(the_shortest_ones)}")
        for i in [0, 1]:
            if len(s1 := the_shortest_ones[i + 0]) == 3:
                print(f'pattern 1 path, i: {i}')
                shortest_paths.append(s1[0][1:][::-1] + s1[2] + s1[1][1:])
            if len(s2 := the_shortest_ones[i + 2]) == 3:
                print(f'pattern 2 path, i: {i}')
                shortest_paths.append(s2[1][1:][::-1] + s2[2] + s2[0][1:])
            if len(s3 := the_shortest_ones[i + 4]) == 3:
                print(f'pattern 3 path, i: {i}')
                shortest_paths.append(s3[0] + s3[1][1:] + s3[2][1:])
            if len(s4 := the_shortest_ones[i + 6]) == 3:
                print(f'pattern 4 path, i: {i}')
                shortest_paths.append(s4[2] + s4[1][1:] + s4[0][1:])
            if len(s5 := the_shortest_ones[i + 8]) == 3:
                print(f'pattern 5 path, i: {i}')
                shortest_paths.append(s5[2] + s5[0][1:] + s5[1][1:])
            if len(s6 := the_shortest_ones[i + 10]) == 3:
                print(f'pattern 6 path, i: {i}')
                shortest_paths.append(s6[1] + s6[0][1:] + s6[2][1:])

        # # min possible path length:
        # min_nodes = len((p := path12 + path23[1:] + path34[1:]))
        # length = len(set(p))
        # print(f'min_nodes: {min_nodes}, length: {length}')

        if len(shortest_paths) == 0:
            return []

        print(f'shortest_paths: ')
        for s_path in shortest_paths:
            print(f'shortest path: {s_path}')

        the_shortest_one = list(sorted(shortest_paths, key=lambda x: len(x)))[0]
        print(f'path_length: {len(the_shortest_one)}')
        return [self.get_num(node.y, node.x) for node in the_shortest_one]

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
        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or total cost of the current Node is not needed here

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)

    def __hash__(self):
        return hash((self.y, self.x))

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

    def __str__(self):
        return f'{self.y, self.x}'

    def __repr__(self):
        return str(self)

    def clear(self):
        self.previously_visited_node = None
        self.g = np.Infinity
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

    def a_star(self, other, candy_factory: 'CandyFactory', obstacle=None, multiplier=1):
        nodes_to_be_visited = [self]
        self.g = 0
        heapq.heapify(nodes_to_be_visited)
        # main cycle:
        while nodes_to_be_visited:
            curr_node = heapq.heappop(nodes_to_be_visited)
            # stop condition of finding the shortest path:
            if curr_node == other:
                break
            # next step of a-star:
            for neigh in curr_node.neighs:
                if neigh not in candy_factory.shortest_path and (neigh.y, neigh.x) not in [(point[0], point[1]) for
                                                                                           point in
                                                                                           candy_factory.station_points
                                                                                           if point not in [
                        (self.y, self.x), (other.y, other.x)]]:
                    if neigh.g > curr_node.g + 1:
                        neigh.g = curr_node.g + 1
                        neigh.h = neigh.manhattan_distance(other) + ((
                                                                                 candy_factory.J_MAX + candy_factory.I_MAX - multiplier * candy_factory.MULTIPLIER * neigh.manhattan_distance(
                                                                             obstacle)) if obstacle is not None else 0)
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
cf = CandyFactory([44, 72, 61, 67])

# cf = CandyFactory()
# cf = CandyFactory()
# cf = CandyFactory()
path = cf.solve()
print(f'PATH: {path}')

print(f'PATTERNS: {CandyFactory.PATTERNS}')

