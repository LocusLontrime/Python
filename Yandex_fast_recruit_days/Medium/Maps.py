# accepted on coderun


def cards_lost():  # 36.6
    n, linears, squares, cubes = get_pars()
    # pre-calculations:
    whole_linears = (n * (n + 1)) // 2
    whole_squares = (n * (n + 1) * (2 * n + 1)) // 6
    whole_cubes = ((n * (n + 1)) // 2) ** 2
    # constants:
    a = whole_linears - linears
    b = whole_squares - squares
    c = whole_cubes - cubes
    print(f'a, b, c: {a, b, c}')
    # aux pars:
    b_ = (a ** 2 - b) // 2
    c_ = (a ** 3 + 2 * c) // 6 - a * b // 2
    print(f'a, b_, c_: {a, b_, c_}')
    # solving the cubic equation with z variable:
    # for a start lets do a factorization of the free term:
    factors = factorize(abs(c_), n)
    print(f'factors: {factors}')
    z = -1
    for z_ in factors:
        eq = z_ ** 3 - a * z_ ** 2 + b_ * z_ - c_
        # print(f'z: {z_}, eq: {eq}')
        if eq == 0:
            # print(f'z: {z_} is root!')
            z = z_
            break
    print(f'z: {z}')
    # now let us solve the quadratic equation with x var:
    d = (a - z) ** 2 - 4 * c_ // z
    x = (a - z + int(d ** .5)) // 2
    print(f'x: {x}')
    y = a - z - x
    print(f'y: {y}')
    return f'{x} {y} {z}'


def factorize(num: int, n: int) -> list[int]:
    factors = set()
    f_ = 2
    while f_ <= n and f_ ** 2 <= num:
        if num % f_ == 0:
            factors.add(f_)
            factors.add(num // f_)
        f_ += 1
    factors.add(num)
    return sorted(factors)


def get_pars():
    n = int(input())
    linears, squares, cubes = [int(i) for i in input().split()]
    return n, linears, squares, cubes


cards_lost()

