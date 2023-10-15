# accepted on codewars.com
import math


def tower(b, h, m):
    print(f'tower({b, h, m} call)')
    """Return base ** base ** ... ** base, where the height is h, modulo m. """
    # Returns  b ** b ** ... ** b, where the height is h, modulo m.
    # base cases:
    if m == 1:
        # k (mod 1)
        print(f'm = 1: zero return')
        return 0
    if b == 1 or h == 0:
        print(f'{"b = 1" if b == 1 else "h = 0"}: tower equals 1')
        # 1 ^ k, k ^ 0
        return 1
    print(f'trying to solve using a naive power tower method:')
    res = naive_pow_tow(b, h, m)
    if res > 0:
        print(f'success! naive pow-tow return: {res}')
        return res
    print(f'fail... let us continue the recursive descending')
    # calcs Euler's totient value for m:
    totient = eulers_totient_phi(m)  # totient(modulo)
    print(f'totient for modulo {m} -->> {totient}')
    # recurrent relation(from kyu's explanation of number theory)
    result = pow(b, tower(b, h - 1, totient) + totient, m)
    print(f'result: {result}')
    # returns the final res:
    return result


def naive_pow_tow(b, h, m):
    result = 1
    for i in range(h):
        result = pow(b, result)
        if result > m:
            return -1
    return result


# an algorithm for computing totient function:
def eulers_totient_phi(m):
    totient = m
    print(f'totient of {m}', end=' ')
    # searching for factors of m:
    for i in range(2, int(math.sqrt(m)) + 1):
        if m % i == 0:
            while m % i == 0:
                # if a current factor repeats
                m = m // i
            totient = totient * (1.0 - 1.0 / i)  # Euler's product formula
        if m == 1:
            break
    # there is a factor that is larger than sqrt(m), only one such factor is possible
    if m > 1:
        totient = totient * (1.0 - 1.0 / m)
    # totient is an integer:
    print(f'-->> {int(totient)}')
    return int(totient)


# nums = 3, 2, 4
# nums = 2, 4, 100000000
# nums = 2, 3, 65536
# nums = 2, 4, 131072
nums = 98948261627849869687362, 94837266576686847836265, 9686716736661

print(f'the final result of power tower for {nums} -->> {tower(nums[0], nums[1], nums[2])}')
