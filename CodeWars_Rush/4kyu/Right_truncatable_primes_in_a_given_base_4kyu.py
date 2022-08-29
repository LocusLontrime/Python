from Miller_Rabin import is_prime


def get_right_truncatable_primes(base):

    prime_chains = []

    def rec_seeker(current_prime_chain):

        flag_of_proceeding = False

        for i in range(0, base):
            new_number = current_prime_chain * base + i

            if is_prime(new_number):
                rec_seeker(new_number)
                flag_of_proceeding = True
            else:
                if 2000 < new_number < 3000:
                    print(new_number)
        if not flag_of_proceeding:
            prime_chains.append(current_prime_chain)

    rec_seeker(0)

    return sorted(prime_chains)


print(get_right_truncatable_primes(16))
# print(get_right_truncatable_primes(19))
# print(get_right_truncatable_primes(10))
# print(get_right_truncatable_primes(8))
# print(get_right_truncatable_primes(6))
# print(get_right_truncatable_primes(4))
# print(get_right_truncatable_primes(2))
