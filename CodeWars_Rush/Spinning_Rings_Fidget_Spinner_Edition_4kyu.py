def spinning_rings(inner_max, outer_max):
    i = 1
    while True:
        outer_num = i % (outer_max + 1)
        inner_num = (inner_max - i + 1) % (inner_max + 1)

        if outer_num == inner_num:
            return i

        i += 1


# print(spinning_rings(2, 100))

# print(spinning_rings(10, 2))
# print(spinning_rings(2, 3))
# print(spinning_rings(20, 30))
# print(spinning_rings(99, 98))

# print(spinning_rings(2**24, 3**15))

for i in range(1, 300 + 1):
    for j in range(1, 300 + 1):
        k = spinning_rings(i, j)
        if k >= 602:
            print(i, j, k)

# print(spinning_rings(128, 100))
