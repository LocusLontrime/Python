# accepted on coderun
import sys
from collections import defaultdict as d


def max_most_frequent_element():
    array = get_pars()
    elements_freq = d(int)
    max_val = 0
    max_most_frequent_one = 0
    for el in array:
        elements_freq[el] += 1
        max_val = max(max_val, elements_freq[el])
    print(f'max_val: {max_val}')
    for key_ in elements_freq.keys():
        if elements_freq[key_] == max_val:
            max_most_frequent_one = max(max_most_frequent_one, key_)
    return max_most_frequent_one


def get_pars() -> list[int]:
    input()
    return [int(_) for _ in input().split(' ')]


print(f'best el: {max_most_frequent_element()}')


