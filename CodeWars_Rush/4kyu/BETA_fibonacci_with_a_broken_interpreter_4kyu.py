from functools import lru_cache

fibs: list[int]


class LambdaRec:
    pass


LambdaRec.__class_getitem__ = lambda f: [0, 1][f] if f < 2 else AuxFib[f - 1] + AuxFib[f - 2]


@lru_cache
def fibo(n):
    return LambdaRec[n]


class AuxFib:
    pass


AuxFib.__class_getitem__ = fibo

print(fibo(100))

