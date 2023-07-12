# accepted on coderun
import math


def min_xor():
    tests = get_pars()
    res = []
    for test_ in tests:
        test_ = sorted(test_)
        min_xor_ = math.inf
        for i in range(len(test_) - 1):
            xor_ = test_[i] ^ test_[i + 1]
            min_xor_ = min(min_xor_, xor_)
        res.append(str(min_xor_))
    return '\n'.join(res)


def get_pars() -> list[list[int]]:
    t = int(input())
    tests = []
    for _ in range(t):
        input()
        tests.append([int(_) for _ in input().split(' ')])
    return tests


print(f'res:\n{min_xor()}')







