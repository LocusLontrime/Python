# accepted on codewars.com
# -*- coding: utf-8 -*-
from queue import Queue

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

INF = 2147483647
NIL = 0


# A class to represent Bipartite graph for Hopcroft
# 3 Karp implementation
class BipGraph(object):
    # Constructor
    def __init__(self, m, n):
        # m and n are number of vertices on left
        # and right sides of Bipartite Graph
        self.__m = m
        self.__n = n
        # adj[u] stores adjacents of left side
        # vertex 'u'. The value of u ranges from 1 to m.
        # 0 is used for dummy vertex
        self.__adj = [[] for _ in range(m + 1)]

    # To add edge from u to v and v to u
    def add_edge(self, u, v):
        self.__adj[u].append(v)  # Add u to v’s list.

    # Returns true if there is an augmenting path, else returns
    # false
    def bfs(self):
        Q = Queue()
        # First layer of vertices (set distance as 0)
        for u in range(1, self.__m + 1):
            # If this is a free vertex, add it to queue
            if self.__pair_u[u] == NIL:
                # u is not matched3
                self.__dist[u] = 0
                Q.put(u)
            # Else set distance as infinite so that this vertex
            # is considered next time
            else:
                self.__dist[u] = INF
        # Initialize distance to NIL as infinite
        self.__dist[NIL] = INF
        # Q is going to contain vertices of left side only.
        while not Q.empty():
            # Dequeue a vertex
            u = Q.get()
            # If this node is not NIL and can provide a shorter path to NIL
            if self.__dist[u] < self.__dist[NIL]:
                # Get all adjacent vertices of the dequeued vertex u
                for v in self.__adj[u]:
                    #  If pair of v is not considered so far
                    # (v, pairV[V]) is not yet explored edge.
                    if self.__dist[self.__pair_v[v]] == INF:
                        # Consider the pair and add it to queue
                        self.__dist[self.__pair_v[v]] = self.__dist[u] + 1
                        Q.put(self.__pair_v[v])
        # If we could come back to NIL using alternating path of distinct
        # vertices then there is an augmenting path
        return self.__dist[NIL] != INF

    # Returns true if there is an augmenting path beginning with free vertex u
    def dfs(self, u):
        if u != NIL:
            # Get all adjacent vertices of the dequeued vertex u
            for v in self.__adj[u]:
                if self.__dist[self.__pair_v[v]] == self.__dist[u] + 1:
                    # If dfs for pair of v also returns true
                    if self.dfs(self.__pair_v[v]):
                        self.__pair_v[v] = u
                        self.__pair_u[u] = v
                        return True
            # If there is no augmenting path beginning with u.
            self.__dist[u] = INF
            return False
        return True

    def hopcroft_karp(self):
        # pairU[u] stores pair of u in matching where u
        # is a vertex on left side of Bipartite Graph.
        # If u doesn't have any pair, then pairU[u] is NIL
        self.__pair_u = [0 for _ in range(self.__m + 1)]

        # pairV[v] stores pair of v in matching. If v
        # doesn't have any pair, then pairU[v] is NIL
        self.__pair_v = [0 for _ in range(self.__n + 1)]

        # dist[u] stores distance of left side vertices
        # dist[u] is one more than dist[u'] if u is next
        # to u'in augmenting path
        self.__dist = [0 for _ in range(self.__m + 1)]
        # Initialize result
        result = 0

        # Keep updating the result while there is an
        # augmenting path.
        while self.bfs():
            # Find a free vertex
            for u in range(1, self.__m + 1):
                # If current vertex is free and there is
                # an augmenting path from current vertex
                if self.__pair_u[u] == NIL and self.dfs(u):
                    result += 1
        return result

    def __str__(self):
        return str(self.__adj)

    def __repr__(self):
        return str(self.__adj)


def max_domino_tiling(grid: list[list[bool]]):
    # for a start let us build a bipartite graph between black and white squares (in chess order):
    graph = build_bipartite_graph(grid)

    print(f'{graph}')

    # the result is the maximum cardinality matching:
    return graph.hopcroft_karp()


def build_bipartite_graph(grid: list[list[bool]]) -> BipGraph:
    max_j, max_i = len(grid), len(grid[0])

    print(f'{max_j, max_i = }')

    coords_to_vertices_black = {}
    coords_to_vertices_white = {}

    m, n = 0, 0

    for j in range(max_j):
        for i in range(max_i):
            if grid[j][i]:
                if (j + i) % 2 == 0:
                    m += 1
                    coords_to_vertices_black[j, i] = m
                else:
                    n += 1
                    coords_to_vertices_white[j, i] = n

    graph = BipGraph(m, n)
    for j in range(max_j):
        for i in range(max_i):
            if grid[j][i]:
                if (j + i) % 2 == 0:
                    print(f'{j, i = }')
                    # getting links:
                    for dj, di in DIRS:
                        if 0 <= (j_ := j + dj) < max_j and 0 <= (i_ := i + di) < max_i:
                            if grid[j_][i_]:
                                if (j_ + i_) % 2 != 0:
                                    graph.add_edge(coords_to_vertices_black[j, i], coords_to_vertices_white[j_, i_])

    print(f'{coords_to_vertices_black = }')
    print(f'{coords_to_vertices_white = }')

    return graph


grid_ = [
    [True, True, True, False],
    [True, True, True, True],
    [True, True, True, True],
    [False, True, True, True]
]  # ans: 6

print(f'res: {max_domino_tiling(grid_)}')
