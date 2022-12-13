# accepted on codewars.com
import math


def wpp(a, b, n):
    # solvability check:
    if n > max(a, b):
        return []
    if n % math.gcd(a, b) != 0:
        return []

    # general case (when solvable):
    # 1 phase -->> solving a diofant equation a * x + b * y = n, let us find x and y:
    def diophantine_eq_solve():
        for y in range(a):
            x = n + b * y
            if x % a == 0:
                return x // a, y

    def pour_from_a_to_b():
        if wpp.curr_a < b - wpp.curr_b:
            wpp.curr_b += wpp.curr_a
            wpp.curr_a = 0
        else:
            wpp.curr_a -= b - wpp.curr_b
            wpp.curr_b = b

    def empty_b():
        wpp.curr_b = 0

    def full_a():
        wpp.curr_a = a

    a_count, b_count = diophantine_eq_solve()
    wpp.curr_a, wpp.curr_b = 0, 0
    result_list = []
    while True:
        while wpp.curr_b < b and a_count > 0:
            full_a()
            result_list.append((wpp.curr_a, wpp.curr_b))
            pour_from_a_to_b()
            result_list.append((wpp.curr_a, wpp.curr_b))
            a_count -= 1
        if b_count <= 0:
            break
        empty_b()
        result_list.append((wpp.curr_a, wpp.curr_b))
        pour_from_a_to_b()
        result_list.append((wpp.curr_a, wpp.curr_b))
        b_count -= 1

    return result_list


print(wpp(7, 15, 6))
# print(wpp(5, 11, 3))
# print(wpp(5, 11, 7))

# print(wpp(59799, 97812, 77127))


