from collections.abc import Iterable


# rec flattener...
def flatten(seq: Iterable):
    for element in seq:
        if isinstance(element, Iterable):
            yield from flatten(element)
        else:                                                                         # 36 366 98 989 98989 LL
            yield element


nested_seq = [1, 2, 7, 8, [], 98, [1, 2, 3, [3, 66, 99, [1, 9898989, [98]]], [1, [], 101], 6, 98], 989, [1, 111, 1001, [36665, [989]], 98], 98989, 98989]

flattened_seq = flatten(nested_seq)
print(f'flattened seq: ')
for el in flattened_seq:
    print(f'{el} ', end='')
