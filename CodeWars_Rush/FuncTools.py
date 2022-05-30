from functools import reduce

k = reduce(lambda x, y: x * y, reversed([1, 2, 3, 4, 5]))

min_el = reduce(lambda x, y: x if x < y else y, reversed([1, 2, 3, 66, 9, 98, 9, 4, 5]))
max_el = reduce(lambda x, y: x if x > y else y, reversed([1, 2, 3, 66, 9, 98, 9, 4, 5]))

do_smth = reduce(lambda row1, row2: row1 if reduce(lambda x, y: x * y, row1) < reduce(lambda x, y: x * y, row2) else row2, [[1, 2, 366], [4, 5, 6], [7, 8, 9]])

print(sum([1, 2, 3]))

a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
a[-2] = 0

print(a)

a = a[::-1]

print(a)

print(a[-1])

print(k)
print(f'min = {min_el}, max =  {max_el}')

print(do_smth)
