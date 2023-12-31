def topological_sort(graph: dict):
    stack = []
    visited = set()
    for v in graph.keys():
        if v not in visited:
            dfs(v, graph, visited, stack)
    for v in stack[::-1]:
        print(f'{v}')


def dfs(vertex: int, graph: dict, visited: set, stack: list[int]):
    visited.add(vertex)
    for neigh in graph[vertex]:
        if neigh not in visited:
            dfs(neigh, graph, visited, stack)
    stack.append(vertex)


# ex:
graph_ = {
    1: {4},
    4: {2, 3},
    3: {2},
    2: {}
}

graph_x = {
    5: {3, 6},
    6: {1, 4},
    3: {2, 4},
    12: {4},
    4: {2},
    2: {1, 8, 10},
    8: {},
    1: {7},
    7: {},
    10: {9},
    9: {11},
    11: {}
}

topological_sort(graph_x)


