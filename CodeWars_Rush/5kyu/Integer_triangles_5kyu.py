# accepted on codewars.com
import math


def give_triang(per):
    # your code here
    x = 0

    for b in range(1, per // 2 + 1):
        for a in range(1, b + 1):
            c = math.sqrt(a ** 2 + b ** 2 + a * b)

            if c % 1 == 0 and a + b + c <= per:
                x += 1
                print(a, b, c)

    return x  # number of integer triangles with one angle of 120 degrees


print(give_triang(50))

# print(97.0 == 97)
#
# f = 98.98
#
# print(f % 1)
