from functools import lru_cache


def formula(n):
    if n == 0:
        return 1
    m = abs(n)
    aux = [f'{validate_num(combinations(m, i))}{validate_monomial("a", m - i)}{validate_monomial("b", i)}' for i in range(m + 1)]
    res = '+'.join(aux)
    return f'1/({res})' if n < 0 else res


def validate_num(num: int) -> str:
    return '' if num == 1 else f'{num}'


def validate_monomial(symbol: str, num: int) -> str:
    if num == 0:
        res = ''
    elif num == 1:
        res = symbol
    else:
        res = f'{symbol}^{num}'
    return res


@lru_cache
def combinations(n: int, k: int) -> int:
    # border case:
    if n == k:
        return 1
    # usual return:
    return (combinations(n - 1, k) * n) // (n - k)


print(f'res: {formula(-10)}')
