tuple1 = (i for i in range(1_000))
tuple2 = (i for i in range(1_000))


def gen():
    yield 98


tuple3 = gen()

print(f'{tuple(tuple1) = }')
print(f'{tuple(tuple2) = }')
print(f'{tuple(tuple3) = }')

contains = 98 in tuple1
c = tuple3 in tuple1
contains_all = all(elem in tuple1 for elem in tuple2)

print(f'{contains = }')
print(f'{c = }')
print(f'{contains_all = }')



