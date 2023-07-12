# accepted on coderun
import sys


def errors_probs():
    pairs = get_pars()
    weights = [a * b for a, b in pairs]
    weight = sum(weights)
    return '\n'.join([str(w / weight) for w in weights])


def get_pars() -> list[tuple[int, int]]:
    n = int(input())
    pairs = []
    for _ in range(n):
        a, b = [int(_) for _ in input().split(' ')]
        pairs.append((a, b))
    return pairs


print(f'errors probabilities:\n{errors_probs()}')


