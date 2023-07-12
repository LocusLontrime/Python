# accepted on coderun
import sys
import math


def get_max_pleasure():
    n, m, a, b = get_pars()
    score = 0
    for j in range(m):
        visited = False
        min_delta = math.inf
        for i in range(n):
            if (b_ := b[i][j]) > (a_ := a[i][j]):
                score += b_
                min_delta = min(min_delta, b_ - a_)
            else:
                score += a_
                visited = True
        if not visited:
            score -= min_delta
    print(score)


def get_pars() -> tuple[int, int, list[list[int]], list[list[int]]]:
    n, m = [int(_) for _ in input().split(' ') if _.isdigit()]
    a = [[int(_) for _ in input().split(' ') if _.isdigit() or _[0] == '-' and _[1:].isdigit()] for _ in range(n)]
    b = [[int(_) for _ in input().split(' ') if _.isdigit() or _[0] == '-' and _[1:].isdigit()] for _ in range(n)]
    print(f'n, m, a, b: {n, m, a, b}')
    return n, m, a, b


get_max_pleasure()
