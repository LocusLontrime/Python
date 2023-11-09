# accepted on codewars.com
from collections import Counter


def exchange_sort(sequence: list[int]):
    counter = Counter(sequence)
    results, border, ans = [0, 0, 0], 0, 0
    counters = [counter[i] for i in range(7, 9 + 1)]
    for j in range(3):
        results[j] = Counter(sequence[border: (border := border + counters[j])])
    for j in range(3):
        for i in range(j + 1, 3):
            if k := min(results[j][i + 7], results[i][j + 7]):
                results[j][i + 7] -= k
                results[i][j + 7] -= k
                ans += k
    return ans + 2 * sum(v for k, v in results[0].items() if 7 != k)


s = [8, 9, 7, 8, 7, 9, 9, 7, 8, 9, 8, 7, 8]
s_ = [8, 8, 7, 9, 9, 9, 8, 9, 7]
print(f'res: {exchange_sort(s_)}')



