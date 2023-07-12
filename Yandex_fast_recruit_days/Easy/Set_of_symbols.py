# accepted on coderun
import sys


def min_length():
    s, c = get_pars()
    c = set(c)
    length = len(c)
    for j in range(length, l := len(s) + 1):
        for i in range(l - j):
            print(f'j, i: {j, i}, substring: {(sub_ := s[i: i + j])}')
            set_ = set(sub_)
            print(f'set_: {set_}')
            if set_ == c:
                return j
    return 0


def get_pars():
    s = input()
    c = input()
    return s, c


s1 = {1, 2, 3, 4, 5}
s2 = {1, 2, 3, 4, 5, 6}

# print(f'{s1 == s2}')

print(f'length: {min_length()}')
