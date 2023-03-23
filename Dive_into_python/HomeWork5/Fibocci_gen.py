# -*- coding: utf-8 -*-


# 3. Создайте функцию генератор чисел Фибоначчи (см. Википедию)

def fib_gen(size_: int):
    # previous and next fibs:
    _fib, fib_ = 0, 1
    for i in range(size_):
        yield _fib
        fib_ = _fib + fib_
        _fib = fib_ - _fib


size = 10
print(f'first {size} fibs: {list(fib_gen(size))}')



