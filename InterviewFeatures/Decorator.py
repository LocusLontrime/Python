import functools
import time


def dec(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        f = func(*args, **kwargs)
        runtime = round(1000 * (time.perf_counter() - start), 2)
        _wrapper.time_elapsed = runtime
        return f

    return _wrapper


@dec
def smth():
    for i in range(10 ** 6):
        k = pow(i ** 2, i, 1_000_000_007)


smth()
print(f'time_elapsed: {smth.time_elapsed} milliseconds')


