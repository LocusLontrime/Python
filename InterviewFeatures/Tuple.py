tuple1 = tuple(range(1_000_000))
tuple2 = tuple(range(1_000_000))

# contains_all = all(elem in tuple1 for elem in tuple2)
contains_all_ = set(tuple1).issubset(tuple2)

print(f'{contains_all_ = }')





