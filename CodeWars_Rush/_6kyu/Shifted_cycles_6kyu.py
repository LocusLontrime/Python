# accepted on codewars.com
def gen(n: int, iterable):
    iterator = iter(iterable)
    sliding_tuple = ()
    for _ in range(n):
        sliding_tuple += (next(iterator),)
    print(f'{sliding_tuple = }')
    yield sliding_tuple
    while 1:
        try:
            el = next(iterator)
        except StopIteration:
            iterator = iter(iterable)
            el = next(iterator)

        sliding_tuple = sliding_tuple[1:] + (el,)
        print(f'...{sliding_tuple = }')
        yield sliding_tuple


arr_ = [1, 2, 3, 4, 5]

# print(f'{arr_[-1:] + arr_[:2]}')

g = gen(2, arr_)

for i in range(98):
    print(f'{next(g)}')

# it = iter(arr_)

# print(f'{it = }')

# for _ in range(3):
#     print(f'{next(it)}')
#
# tup = (1, 2, 3, 4, 5)
#
# print(f'{tup[2: 3] + (4,)}')
