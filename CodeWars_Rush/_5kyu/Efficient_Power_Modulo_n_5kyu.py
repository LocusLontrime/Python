# accepted on codewars.com
def power_mod(x: int, y: int, n: int) -> int:
    # base cases:
    if x == 0:
        return 0
    if y == 0:
        return 1
    # the core:
    if y % 2:
        # y is odd:
        k = ((x % n) * (power_mod(x, y - 1, n) % n)) % n
    else:
        # y is even:
        k = power_mod(x, y // 2, n)
        k = (k * k) % n
    # returns res (k may be less than 0 -> we should add n to it):
    return (k + n) % n


x_, y_, n_ = 35594, 670333548, 6931391  # 2, 3, 5

print(f'{x_} ^ {y_} mod {n_} -> {power_mod(x_, y_, n_)}')



