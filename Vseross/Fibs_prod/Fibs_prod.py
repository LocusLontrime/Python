THRESHOLD = 10 ** 18


def fibs_prod(n: int) -> int:
    memo_table = {}
    result = rec_core(n, 0, get_fibs(), memo_table, '1')
    print(f'memo size: {len(memo_table)}')
    return result


def rec_core(rem: int, i: int, fibs: list[int], memo_table: dict[tuple[int, int], int], way: str) -> int:
    if (rem, i) not in memo_table.keys():
        # border case:
        if rem == 1:
            memo_table[(rem, i)] = 1
            return 1
        # body:
        res = 0
        for i_ in range(i, len(fibs)):
            fib = fibs[i_]
            if fib > rem:
                break
            if rem % fib == 0:
                res += rec_core(rem // fib, i_, fibs, memo_table, f'{way}*{fib}')
        memo_table[(rem, i)] = res
    return memo_table[(rem, i)]


def get_fibs() -> list[int]:
    _f, f_ = 1, 2
    fibs = []
    while f_ <= THRESHOLD:
        f_ = f_ + _f
        _f = f_ - _f
        fibs.append(_f)
    return fibs


print(f'fibs: {get_fibs()}')
n_ = 2 ** 8 * 3 * 5 ** 5 * 8 ** 3 * 13 ** 3 * 21 * 34 * 55 * 89 * 46368 * 832040 ** 2
print(f'n_ : {n_}')
print(f'ways: {fibs_prod(n_)}')
