# accepted on coderun
from collections import defaultdict as d


def uniq_elements_q():
    array = get_pars()
    uniques = d(int)
    for el in array:
        uniques[el] += 1
    return sum(1 for key in uniques.keys() if uniques[key] == 1)


def get_pars() -> list[int]:
    n = input()
    return [int(_) for _ in input().split(' ') if _.isdigit()]


print(f'count: {uniq_elements_q()}')
