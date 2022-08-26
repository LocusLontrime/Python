# accepted on codewars.com
import math


def totient(n):  # 36 366 98 989 98989
    def is_not_prime(number):  # fast check (not as Miller Rabin test)
        return 2 not in [number, pow(2, number, number)]  # 2 ** number % number
    if n is not None and type(n) is int and n >= 1:
        totient_val = n
        rem_n = n
        primes = []
        for i in range(2, int(math.sqrt(n)) + 1):
            flag = True
            for prime in primes:
                if i % prime == 0:
                    flag = False
                    break
            if flag:
                primes.append(i)
                while rem_n > 0 and rem_n % i == 0:
                    flag = False
                    rem_n //= i
                if not flag:
                    totient_val *= 1 - 1 / i
                if rem_n == 1 or not is_not_prime(rem_n):
                    break
        if rem_n > 1:
            totient_val *= 1 - 1 / rem_n

        return int(totient_val)
    else:
        return 0


print(totient(9999999985))
