# 5. 2520 - самое маленькое число, которое делится без остатка на все числа от 1 до 10.
# Какое самое маленькое число делится нацело на все числа от 1 до 20?

from HWSem2.AddTask4 import get_primes  # import of the method from another task solved


def min_number(n):
    """
    :param n: max_number
    :return: the min_number for which: min_number % i = 0, i from 1 to max_number
    """
    primes = get_primes(int(n ** 0.5) + 1)

    def get_factors(number):
        """
        :param number: number to be factorized
        :return: factorization dictionary
        """
        factor_dict = {1: 1}  # factor dictionary initialization
        for prime in primes:
            if prime * prime > number:  # get prime factors before sqrt(number)
                break
            while number != 1 and number % prime == 0:
                number /= prime
                if prime in factor_dict:
                    factor_dict[prime] += 1  # increases a power (value) of this prime factor
                else:
                    factor_dict[prime] = 1  # adds a new prime factor to the dict
            if number == 1:  # if a number is equal to one -> factorization is over
                break
        if number != 1:  # the last factor that is bigger than sqrt(number) is the prime factor (like in 2*3*17: 17 is the one)
            factor_dict[number] = 1
        return factor_dict

    res_factor_dict = {1: 1}
    product = 1

    for i in range(2, n + 1):  # for all elements from 2 to n we build a unique factors dictionary
        curr_f_dict = get_factors(i)
        for item in curr_f_dict:
            if item in res_factor_dict:  # if the factor is already in the res_factor_dict
                res_factor_dict[item] = max(res_factor_dict[item], curr_f_dict[item])  # if the power is larger -> extends the factors dictionary
            else:
                res_factor_dict[item] = curr_f_dict[item]  # if the factors' dictionary does not contain the current factor -> adds it with its power

    for i in res_factor_dict:  # here we're building the product
        product *= int(i ** res_factor_dict[i])

    print(res_factor_dict)

    # print(res_factor_dict) # dictionary checking

    return product


print(min_number(10))
print(min_number(20))
print(min_number(100))

print(min_number(100000))  # optimization checking
