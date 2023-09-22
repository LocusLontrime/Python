FIB_CYCLE_LENGTH = 60


def last_fib_digit(n: int):
    return pre_compute(FIB_CYCLE_LENGTH)[n % FIB_CYCLE_LENGTH - 1]


def pre_compute(k: int) -> list[int]:
    fibs = [1 for _ in range(k)]
    for i in range(2, k):
        fibs[i] = (fibs[i - 1] + fibs[i - 2]) % 10
    return fibs


print(f'last dig: {last_fib_digit(1000000009)}')
