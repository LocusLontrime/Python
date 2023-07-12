# accepted on coderun
import sys


def get_substrings_graph():
    words = get_pars()
    vertexes = dict()
    directed_edges = dict()
    # graph building:
    for word_ in words:
        for i in range(len(word_) - 2 - 1):
            w1_, w2_ = word_[i: i + 3], word_[i + 1: i + 4]
            h1, h2 = hash(w1_), hash(w2_)
            if h1 in vertexes.keys():
                w1_ = vertexes[h1]
            else:
                vertexes[h1] = w1_
            if h2 in vertexes.keys():
                w2_ = vertexes[h2]
            else:
                vertexes[h2] = w2_
            if (w1_, w2_) in directed_edges.keys():
                directed_edges[(w1_, w2_)] += 1
            else:
                directed_edges[(w1_, w2_)] = 1
    aux = "\n".join(f'{key[0]} {key[1]} {directed_edges[key]}' for key in directed_edges.keys())
    return f'{len(vertexes)}\n{len(directed_edges)}\n{aux}'


def get_pars() -> list[str]:
    t = int(input())
    words = [input() for _ in range(t)]
    return words


# print(f'{"aabsf"[1: 1 + 2]}')

print(f'graph:\n{get_substrings_graph()}')


