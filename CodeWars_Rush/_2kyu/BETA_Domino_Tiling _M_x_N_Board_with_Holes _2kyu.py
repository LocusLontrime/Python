# accepted on codewars.com
from collections import defaultdict as d

walk = ((0, 1), (1, 0), (0, -1), (-1, 0))

# Python3 implementation of Hopcroft Karp algorithm for
# maximum matching
from queue import Queue

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
    def addEdge(self, u, v):
        self.__adj[u].append(v)  # Add u to v's list.

    # Returns true if there is an augmenting path, else returns
    # false
    def bfs(self):
        Q = Queue()
        # First layer of vertices (set distance as 0)
        for u in range(1, self.__m + 1):
            # If this is a free vertex, add it to queue
            if self.__pairU[u] == NIL:
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
                    if self.__dist[self.__pairV[v]] == INF:
                        # Consider the pair and add it to queue
                        self.__dist[self.__pairV[v]] = self.__dist[u] + 1
                        Q.put(self.__pairV[v])
        # If we could come back to NIL using alternating path of distinct
        # vertices then there is an augmenting path
        return self.__dist[NIL] != INF

    # Returns true if there is an augmenting path beginning with free vertex u
    def dfs(self, u):
        if u != NIL:
            # Get all adjacent vertices of the dequeued vertex u
            for v in self.__adj[u]:
                if self.__dist[self.__pairV[v]] == self.__dist[u] + 1:
                    # If dfs for pair of v also returns true
                    if self.dfs(self.__pairV[v]):
                        self.__pairV[v] = u
                        self.__pairU[u] = v
                        return True
            # If there is no augmenting path beginning with u.
            self.__dist[u] = INF
            return False
        return True

    def hopcroftKarp(self):
        # pairU[u] stores pair of u in matching where u
        # is a vertex on left side of Bipartite Graph.
        # If u doesn't have any pair, then pairU[u] is NIL
        self.__pairU = [0 for _ in range(self.__m + 1)]

        # pairV[v] stores pair of v in matching. If v
        # doesn't have any pair, then pairU[v] is NIL
        self.__pairV = [0 for _ in range(self.__n + 1)]

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
                if self.__pairU[u] == NIL and self.dfs(u):
                    result += 1
        return result


def max_domino_tiling(grid: list[list[bool]]) -> int:
    bipartite_graph, v, e = get_b_graph(grid)
    print(f'{v, e = }')
    print(f'{bipartite_graph = }')
    # now let us define the maximum cardinality matching for the bipartite graph built:
    b_g = BipGraph(v, e)
    for k, v in bipartite_graph.items():
        for vertex_ in v:
            b_g.addEdge(k, vertex_)
    result = b_g.hopcroftKarp()
    print(f'{result = }')
    return result


def get_b_graph(grid: list[list[bool]]) -> tuple[dict, int, int]:
    graph = d(list)
    translate = {}
    v, e = 0, 0
    for j in range(j_max := len(grid)):
        for i in range(i_max := len(grid[0])):
            if grid[j][i]:
                if (j + i) % 2 == 0:
                    v += 1
                    # links:
                    for dj, di in walk:
                        # validation:
                        if 0 <= (j_ := j + dj) < j_max and 0 <= (i_ := i + di) < i_max:
                            if grid[j_][i_]:
                                # edges building (only from evens when j + i % 2 == 0 to odds when ... == 1):
                                graph[v] += [j_ * i_max + i_]
                else:
                    e += 1
                    translate[j * i_max + i] = e
    graph = {k: [translate[el] for el in v] for k, v in graph.items()}

    return graph, v, e


grid_ = [
    [True, True, True, False],
    [True, True, True, True],
    [True, True, True, True],
    [False, True, True, True]
]

max_domino_tiling(grid_)
