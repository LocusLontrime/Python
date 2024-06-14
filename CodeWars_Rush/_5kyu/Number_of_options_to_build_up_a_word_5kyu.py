# accepted on codewars.com
from collections import defaultdict as d


rec_counter: int


def get_options_count(target: str, words: tuple[str, ...]):
    global rec_counter
    rec_counter = 0
    graph = d(set)
    for word in words:
        wl = len(word)
        for i in range(len(target) - wl + 1):
            if word == target[i: i + wl]:
                graph[i].add(i + wl)
    print(f'{graph = }')
    return rec_core(0, len(target), graph, {})


def rec_core(i: int, n: int, graph: d[int, set], memo_table: dict) -> int:
    global rec_counter
    rec_counter += 1
    # base case:
    if i == n:
        return 1
    # core:
    if i not in memo_table.keys():
        memo_table[i] = 0
        for i_ in graph[i]:
            memo_table[i] += rec_core(i_, n, graph, memo_table)
    # returns res:
    return memo_table[i]


target_, words_ = 'prolongation', ('pr', 'l', 'o', 'ga', 'ti', 'n', 'p', 'r', 'g', 'a', 'pro', 't', 'i', 'prolo')  # -> 16
target_x, words_x = 'totatutatuto', ('t', 'o', 'a', 'to', 'ta', 'tu', 'u', 'tot')  # -> 80

print(f'res: {get_options_count(target_x, words_x)}')
print(f'{rec_counter = }')
