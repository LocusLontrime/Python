import random
MR_THRESHOLD = 25


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


def prepare():

    result = []
    counter = 0

    i = 0
    while True:
        i += 1

        squared = i ** 2
        cubed = i ** 3

        squared_rev = int(str(squared)[::-1])
        cubed_rev = int(str(cubed)[::-1])

        if is_prime(squared_rev) and is_prime(cubed_rev):
            counter += 1
            result.append(i)
            # print(i)

        if counter == 250:
            break

    return result  # x is the n-th term of the sequence


memo_table = prepare()


def sq_cub_rev_prime(n):
    return memo_table[n - 1]


print(memo_table)


print(str(123456)[::-1])

print(sq_cub_rev_prime(1))
print(sq_cub_rev_prime(2))
print(sq_cub_rev_prime(3))
print(sq_cub_rev_prime(4))

print(len('def squirrel(h,H,S):return H*(h*h+S*S)**.5/h'))


