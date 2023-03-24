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
list_ = []
# print(f'first {size} fibs: {list()}')
f = fib_gen(size)

print(f'{next(f)}')
print(f'{next(f)}')
print(f'{next(f)}')
print(f'{next(f)}')
print(f'{next(f)}')
print(f'list_: {list_}')







