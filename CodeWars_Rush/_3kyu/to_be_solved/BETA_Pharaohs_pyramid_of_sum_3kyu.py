import math


invariants = [0, 1]


def pyramid_cost(data, k, p):
    n = len(data)

    if len(invariants) == 2:
        for inv in range(2, 10 ** 2 + 1):
            invariants.append((p - p // inv) * invariants[p % inv] % p)

    print(f'{invariants = }')

    delta_ = 1
    sum_ = delta_ * data[-1]

    for i in range(n - 1):
        delta_ = (delta_ * (k + i + 1) * invariants[i + 1]) % p
        sum_ = (sum_ + delta_ * data[-(i + 2)]) % p
        print(f'{delta_ = } | {data[-(i + 2)] = }')
    return sum_


def combs(n: int, m: int) -> int:
    return math.factorial(n) // (math.factorial(m) * math.factorial(n - m))


print(f'{combs(7, 3)}')
print(f'{combs(6, 2)}')
print(f'{combs(5, 1)}')

data1 = [9, 11, 4, 6, 4, 2]
print(f'res: {pyramid_cost([1, 1, 1, 1], 3, 127)}')
print(f'res: {pyramid_cost(data1, 3, 127)}')
