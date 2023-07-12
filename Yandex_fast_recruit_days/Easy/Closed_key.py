# accepted on coderun


def closed_keys_q():
    gcd, lcm = get_pars()
    if lcm % gcd != 0:
        return 0
    gcd_factors, lcm_factors = factors(gcd), factors(lcm)
    for _ in range(len(gcd_factors)):
        lcm_factors.remove(gcd_factors[_])
    return 2 ** len(set(lcm_factors))


def factors(number) -> list[int]:
    n = int(number ** .5) + 1
    era = [1] * n
    primes = []
    for p in range(2, n):
        if era[p]:
            primes.append(p)
            for i in range(p * p, n, p):
                era[i] = False
    divisors = []
    x = number
    for i in primes:
        while x % i == 0:
            x //= i
            divisors.append(i)
    if x != 1:
        divisors.append(x)
    return divisors


def get_pars() -> tuple[int, int]:
    gcd, lcm = [int(_) for _ in input().split(' ')]
    return gcd, lcm


print(f'closed keys quantity: {closed_keys_q()}')
# print(f'factors: {factors(80765450077)}')
# print(f'{factors(527)}, {factors(9486)}')
