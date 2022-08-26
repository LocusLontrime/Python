# Miller-Rabin test for primes, works for mega large n
MR_THRESHOLD = 1


import random


def get_pars(n):
    power, multiplier = 0, n
    while multiplier % 2 == 0:
        power += 1
        multiplier >>= 1
    return power, multiplier


def miller_rabin_test(a, p):

    power, multiplier = get_pars(p - 1)
    a = pow(a, multiplier, p)

    if a == 1:
        return True

    for i in range(power):
        if a == p - 1:
            return True
        a = pow(a, 2, p)

    return False


def is_prime(p):

    if p == 2:
        return True

    if p <= 1 or p % 2 == 0:
        return False

    return all(miller_rabin_test(random.randint(2, p - 1), p) for _ in range(MR_THRESHOLD))


# print(is_prime(123426017006182806728593424683999798008235734137469123231828679))
#
# print(is_prime(14044103))
# print(is_prime(2047))
#
# print([] + [1, 2, 3])

print(is_prime(5))
print(is_prime(4))
print(is_prime(100))
print(is_prime(1361))




