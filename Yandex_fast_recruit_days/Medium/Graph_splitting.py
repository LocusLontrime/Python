# accepted on coderun
import sys


def is_bipartite(graph, max_w: int) -> bool:
    """
    :type graph: List[set[Tuple[int, int]]]
    :type max_w: int
    :rtype: bool
    """
    visited = [0 for _ in range(len(graph))]   # 0-not visited; 1-blue; 2-red;
    for i in range(len(graph)):
        if graph[i] and visited[i] == 0:                                              # 36.6 98
            visited[i] = 1
            q = [i]
            ind_ = 0
            while ind_ != len(q):
                v = q[ind_]  # every point
                ind_ += 1
                for e, w in graph[v]:  # every edge
                    if w > max_w:
                        continue
                    if visited[e] != 0:
                        if visited[e] == visited[v]:
                            return False
                    else:
                        visited[e] = 3 - visited[v]
                        q.append(e)
    return True


def split():
    n, m, graph, max_weight = get_pars()
    if is_bipartite(graph, max_weight):
        print(f'{max_weight}')
        return

    lb, rb = 0, max_weight + 1

    while rb - lb > 1:
        middle = (rb + lb) // 2
        if is_bipartite(graph, middle):
            lb = middle
        else:
            rb = middle

    print(f'{rb}')


def get_pars():
    n, m = map(int, input().split())
    graph = [set() for _ in range(n)]
    max_weight = 0
    edges = [tuple(map(int, sys.stdin.readline().split())) for i in range(m)]
    for u, v, w in edges:
        graph[u - 1].add((v - 1, w))
        graph[v - 1].add((u - 1, w))
        max_weight = max(max_weight, w)
    return n, m, graph, max_weight


split()
