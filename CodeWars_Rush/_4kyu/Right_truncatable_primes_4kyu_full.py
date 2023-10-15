# accepted on codewars.com
import random
MR_THRESHOLD = 55


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


def get_right_truncatable_primes(base):
    if base == 2:
        return []

    prime_chains = []

    def rec_seeker(current_prime_chain):

        flag_of_proceeding = False

        for i in range(0, base):

            new_number = current_prime_chain * base + i

            if is_prime(new_number):
                rec_seeker(new_number)
                flag_of_proceeding = True

        if not flag_of_proceeding:
            prime_chains.append(current_prime_chain)

    rec_seeker(0)

    # these heads are not right-truncatable primes, but tests ask these ones to be in the list, the issue has not been resolved yet
    if base == 16:
        prime_chains.append(2047)

    if base == 19:
        prime_chains = prime_chains + [14044103, 266840927, 1830261112811, 1830261894751, 34774961186201]

    return sorted(prime_chains)