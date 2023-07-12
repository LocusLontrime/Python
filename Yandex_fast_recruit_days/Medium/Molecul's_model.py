# accepted on coderun
import sys
from collections import deque as dq


def cut_molecule():
    n, m, edges, q, queries = get_pars()
    graph = [[] for _ in range(n)]
    connected_components = [-1 for _ in range(n)]
    sq = set(queries)  # 36.6 98
    pre_edges = [_ for i, _ in enumerate(edges) if (i + 1) not in sq]
    del sq
    sizes = {}
    ccq = n
    res = [str(ccq)]
    for u, v in pre_edges + [edges[_ - 1] for _ in queries][::-1]:
        ccv = connected_components[v - 1]
        ccu = connected_components[u - 1]
        if ccu == ccv == -1:
            connected_components[u - 1] = connected_components[v - 1] = v
            sizes[v] = 2
            ccq -= 1
            append_edge(graph, u, v)
        elif ccu == -1:
            connected_components[u - 1] = ccv
            sizes[ccv] += 1
            ccq -= 1
            append_edge(graph, u, v)
        elif ccv == -1:
            connected_components[v - 1] = ccu
            sizes[ccu] += 1
            ccq -= 1
            append_edge(graph, u, v)
        else:  # 36.6 98
            if ccv != ccu:
                new_size = (s1 := sizes[ccv]) + (s2 := sizes[ccu])
                if s1 < s2:
                    bfs(graph, v - 1, connected_components, ccu)
                    sizes[ccu] = new_size
                else:
                    bfs(graph, u - 1, connected_components, ccv)
                    sizes[ccv] = new_size
                ccq -= 1
                append_edge(graph, u, v)
        res.append(str(ccq))
    print(f'{" ".join(res[m - len(queries):-1][::-1])}')


def append_edge(graph, u, v):
    graph[v - 1].append(u - 1)
    graph[u - 1].append(v - 1)


def bfs(graph: list, start_node: int, connected_components, val: int) -> int:
    deq = dq()
    deq.append(start_node)
    visited = {start_node}
    while deq:
        vertex_ = deq.popleft()
        connected_components[vertex_] = val
        visited.add(vertex_)
        for next_vertex in graph[vertex_]:
            if next_vertex not in visited:
                deq.append(next_vertex)
    return len(visited)


def get_pars():
    n, m = map(int, input().split())
    edges = [[int(_) for _ in input().split()] for _ in range(m)]
    q = int(input())
    queries = [int(_) for _ in input().split()]
    return n, m, edges, q, queries

    # 36.6 98


def main():
    cut_molecule()


if __name__ == '__main__':
    main()
