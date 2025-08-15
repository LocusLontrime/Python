# accepted on leetcode.com

import math
from collections import defaultdict


def shortest_super_string(words: list[str]) -> str:
    # array's length:
    n = len(words)
    # at first, let us create a word graph:
    graph = defaultdict(set)
    for j in range(n):
        for i in range(n):
            if j != i:
                w = calc_weight(words[j], words[i])
                graph[j] |= {(i, w)}
    graph[-1] = {(i, 0) for i in range(n)}
    print(f'{graph = }')
    # now we should use dynamic programming with bitmasks for a salesman problem:
    start_bitmask = 0
    memo_table = {}
    path = {}
    shortest_super_string_length = dp(-1, start_bitmask, n, graph, words, memo_table, path)
    print(f'{shortest_super_string_length = }')
    # finally, we need to recover the shortest superstring:
    print(f'{path = }')
    node = (-1, 0)
    shortest_superstring = f''
    while True:
        print(f'{node = }')
        node, word, w = path[node]
        print(f'-> {node, word, w}')
        if word != -1:
            shortest_superstring += words[word][:w]
        if node is None:
            break
    return shortest_superstring


def calc_weight(word1: str, word2: str) -> int:
    n1, n2 = len(word1), len(word2)
    w1_end = f''
    w2_start = f''
    max_length = 0
    i = 0
    while i < min(n1, n2):
        w1_end = word1[n1 - i - 1] + w1_end
        w2_start += word2[i]
        # print(f'{w1_end, w2_start = }')
        if w1_end == w2_start:
            max_length = i + 1
        i += 1
    return n1 - max_length


def dp(word: int, state_bitmask: int, n: int, graph: dict, words: list[str], memo_table: dict, path: dict) -> int:
    print(f'{word = } | {bin(state_bitmask) = }')
    # base case:
    if state_bitmask == (1 << n) - 1:
        path[(word, state_bitmask)] = None, word, len(words[word])
        return len(words[word])
    # the core algo:
    if (word, state_bitmask) not in memo_table.keys():
        res = math.inf
        for word_, weight in graph[word]:
            # if the word_ has not been visited:
            if not (state_bitmask & (1 << word_)):
                # next step and visiting (bitmask update):
                r = dp(word_, state_bitmask | (1 << word_), n, graph, words, memo_table, path) + weight
                if r < res:
                    res = r
                    path[(word, state_bitmask)] = (word_, state_bitmask | (1 << word_)), word, weight
        memo_table[(word, state_bitmask)] = res
    return memo_table[(word, state_bitmask)]


test_ex = ["alex", "loves", "leetcode"]
test_ex_1 = ["catg", "ctaagt", "gcta", "ttca", "atgcatc"]

print(f'test ex res -> {shortest_super_string(test_ex)}')                             # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {shortest_super_string(test_ex_1)}')

# print(f'{calc_weight("gcta", "ctaagt") = }')

# b = 0b10101
# c = 0b01000
#
# x = b | c
#
# print(f'{bin(x) = }')

