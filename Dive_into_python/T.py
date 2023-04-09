p1 = 98, 989
p2 = 989, 98989


def cross_product(x1, x2, y1, y2):
    return x1 * y2 - x2 * y1


print(f'cross product: {cross_product(*p1, *p2)}')

s1, s2 = sorted([989, 98])

print(f's1, s2: {s1, s2}')
