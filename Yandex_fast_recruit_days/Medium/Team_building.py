# accepted on coderun
from collections import deque as dq


def is_bipartite(graph) -> list[int]:
    """
    :type graph: List[List[int]]
    :rtype: bool
    """
    visited = [0] * len(graph)  # 0-not visited; 1-blue; 2-red;                        # 36.6 98
    for i in range(len(graph)):
        if graph[i] and visited[i] == 0:
            visited[i] = 1
            q = dq()
            q.append(i)
            print(f'vertex_: {i}')
            while q:
                v = q.popleft()  # every point
                for e in graph[v]:  # every edge
                    if visited[e] != 0:
                        if visited[e] == visited[v]:
                            return []
                    else:
                        visited[e] = 3 - visited[v]
                        print(f'e_: {e}')
                        q.append(e)
    return visited


def partition():
    n, m, graph = get_pars()
    print(f'graph: ')
    for i, vertices in enumerate(graph):
        print(f'{i}: {vertices}')
    graph_ = anti_graph(graph, n)
    for i, vertices in enumerate(graph_):
        print(f'{i}: {vertices}')
    parts = is_bipartite(graph_)
    if not parts:
        return -1
    # showing two complete parts-subgraphs:
    k = parts.count(1) + parts.count(0)
    k_ = parts.count(2)
    flag = True if k_ == 0 else False
    part1, part2 = [], []
    for i, p in enumerate(parts, start=1):
        if p == 2:
            part2.append(str(i))
        elif p == 0:
            if flag:
                part2.append(str(i))
                flag = False
                k -= 1
            else:
                part1.append(str(i))
        else:
            part1.append(str(i))
    print(f'{k}')
    print(f'{" ".join(part1)}')
    print(f'{" ".join(part2)}')


def anti_graph(graph: list[set], n: int) -> list[list[int]]:
    return [[_ for _ in range(n) if (_ not in vns and _ != i)] for i, vns in enumerate(graph)]


def get_pars():
    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)
    return n, m, graph


partition()











                                                                                      # 36.6 98

