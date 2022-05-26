# Найти сумму чисел списка стоящих на нечетной позиции (Locus_Lontrime HW)
import math
def get_sum(numbers_list):
    """
    :param numbers_list: numbers
    :return: sum of elements with odd indexes
    """
    sum = 0
    for i in range(0, len(numbers_list), 2):
        sum += numbers_list[i]
    return sum


print(get_sum([1, 2, 3, 4, 5, 6, 7, 8, 9]))


# Найти произведение пар чисел в списке. Парой считаем первый и последний элемент, второй и предпоследний и т.д.
# Пример: [2, 3, 4, 5, 6] => [12, 15, 16]; [2, 3, 5, 6] => [12, 15]
def get_product(numbers_list):
    """
    :param numbers_list: numbers
    :return: list of products of following elements: first * last, second * one before last and so on...
    """
    left, right, product, prod_list = 0, len(numbers_list) - 1, 0, []  # two-pointers approach
    while left <= right:  # stop conditional
        product = numbers_list[left] * numbers_list[right]
        prod_list.append(product)
        left += 1  # pointers walking
        right -= 1
    return prod_list


print(get_product([2, 3, 4, 5, 6]))
print(get_product([2, 3, 5, 6]))


# В заданном списке вещественных чисел найдите разницу между максимальным и минимальным значением дробной части элементов.
# Пример: [1.1, 1.2, 3.1, 5, 10.01] => 0.19
def get_diff(numbers_list):
    """
    :param numbers_list: float numbers
    :return: diff between max and min fractional parts
    """
    max_part = 0  # initial values for max and min vars
    min_part = 1
    for i in numbers_list:
        max_part = max(max_part, i % 1)
        min_part = min(min_part, (1 if i % 1 == 0 else i % 1))  # min fractional part cannot be equal to zero (0.0)
    return max_part - min_part


print(get_diff([1.1, 1.2, 3.1, 5, 10.01]))


# Написать программу преобразования десятичного числа в двоичное
def dec_to_bin(dec_number):
    """
    :param dec_number: a number in dec representation
    :return: bin representation of the dec number given
    """
    if dec_number == 0:
        return 0
    if dec_number % 2 == 0:
        return 0 + 10 * dec_to_bin(dec_number // 2)
    else:
        return 1 + 10 * dec_to_bin(dec_number // 2)


f = lambda dec_number: 0 if dec_number == 0 else f(dec_number // 2) * 10 + (0 if dec_number % 2 == 0 else 1)  # just a way to solve
print(dec_to_bin(98))
print(f(98))


# Экстра-задачи:

# 1. Написать программу преобразования двоичного числа в десятичное.
def bin_to_dec(bin_number):
    """
    :param bin_number: a number in bin representation
    :return: dec representation of the bin number given
    """
    if bin_number == 0:
        return 0
    if bin_number % 10 == 1:
        return bin_to_dec(bin_number // 10) * 2 + 1
    else:
        return bin_to_dec(bin_number // 10) * 2


k = lambda bin_number: 0 if bin_number == 0 else bin_to_dec(bin_number // 10) * 2 + (1 if bin_number % 10 == 1 else 0)  # just a way to solve

print(bin_to_dec(1100010))
print(k(1100010))


# 2. Создайте программу, которая будет играть в игру “коровы и быки” с пользователем. Игра работает так:
# Случайным образом генерируйте 4-значное число. Попросите пользователя угадать 4-значное число.
# За каждую цифру, которую пользователь правильно угадал в нужном месте, у них есть “корова”.
# За каждую цифру, которую пользователь угадал правильно, в неправильном месте стоит “бык”.
# Каждый раз, когда пользователь делает предположение, скажите им, сколько у них “коров” и “быков”.
# Как только пользователь угадает правильное число, игра окончена. Следите за количеством догадок,
# которые пользователь делает на протяжении всей игры, и сообщите пользователю в конце.
import random


def bulls_and_cows():
    def get_digits(number, digits_list):
        """
        :param number: a number whose digits we want to get
        :param digits_list: aux list of digits
        :return: list of digits of a number given
        """
        if number == 0:
            return digits_list
        else:
            digits_list.insert(0, number % 10)
            return get_digits(number // 10, digits_list)

    n = random.randint(1000, 9999)  # a random generation of 4-digit number
    digits = get_digits(n, [])  # list of digits of picked number
    flag = True  # flag of game being on
    counter = 0  # counter of tries

    print('THE GAME "BULLS AND COWS" BEGINS!' )

    while flag:  # the main game-cycle
        counter += 1
        print('Enter a 4-digit number')

        str_number = input()

        if str_number == 'Exit' or str_number == 'exit':  # stop-game condition
            print('The game is ended')
            break

        num = int(str_number)

        if num < 1000 or num > 9999:
            continue
        bulls, cows = 0, 0  # bulls and cows counters
        if num == n:  # a win-case
            flag = False
            print(f'you won, steps done: {counter}')
        curr_digits = get_digits(num, [])
        digits_clone = digits.copy()

        # print(f'init_num: {digits}')

        for i in range(0, 4):
            if curr_digits[i] == digits_clone[i]:
                cows += 1
        for i in range(0, 4):
            if curr_digits[i] in digits_clone:
                digits_clone.remove(curr_digits[i])
                bulls += 1
        bulls -= cows
        print(f'bulls = {bulls}, cows = {cows}')


bulls_and_cows()  # here the game starts


# 3.Каждый следующий элемент ряда Фибоначчи получается при сложении двух предыдущих. Начиная с 1 и 2, первые 10 элементов будут:
# 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
def get_fib_list(n):
    """
    :param n: the length of the one wing of a fibs_list being built
    :return: list of fib numbers from -n to n
    """
    f1, f2, fibs_list = 1, 0, [0]
    for i in range(0, n):
        f2 = f2 + f1  # a next fib
        f1 = f2 - f1  # one before next
        fibs_list.append(f2)
        fibs_list.insert(0, f2 if i % 2 == 0 else -f2)  # building of the negative-wing of a fibs_list
    return fibs_list


print(get_fib_list(15))


# 4. Простые делители числа 13195 - это 5, 7, 13 и 29.
# Каков самый большой делитель числа 600851475143, являющийся простым числом?
def get_primes(n):  # Eratosthenes' sieve
    """
    :param n: max number to which we should build the primes list
    :return: list of primes before or equal to n
    """
    # filling the list from 0 to n
    a = []
    for i in range(n + 1):
        a.append(i)

    # 1 is a prime number
    a[1] = 0

    # we begin from 3-th element
    i = 2
    while i <= n:
        # if the cell value has not yet been nullified -> it keeps the prime number
        if a[i] != 0:
            # the first multiple will be two times larger
            j = i + i
            while j <= n:
                # not a prime -> exchange it with 0
                a[j] = 0
                # proceed to the next number (n % i == 0)
                # it has the value that is larger by i
                j = j + i
        i += 1

    # list to set, all nulls except 1 got removed
    a = set(a)
    # here we delete the last null
    a.remove(0)
    return a


def get_max_prime_divisor(number):
    """
    :param number: a number given
    :return: max prime factor
    """
    max_prime_div = 1
    divisors = get_primes(int(number ** 0.5))  # iterating from 2 to max prime before or equal to sqrt(number)
    for i in divisors:
        if number % i == 0:
            max_prime_div = i  # the max prime factor is the last one
    return max_prime_div


print(get_primes(100))
print(get_max_prime_divisor(600851475143))
print(get_max_prime_divisor(87625999))
print(600851475143 / 6857)


# 5. 2520 - самое маленькое число, которое делится без остатка на все числа от 1 до 10.
# Какое самое маленькое число делится нацело на все числа от 1 до 20?
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

    # print(res_factor_dict) # dictionary checking

    return product


print(min_number(10))
print(min_number(20))
print(min_number(100))
# print(min_number(100000))  # optimization checking

# print(get_factors(9366))

print(math.factorial(10))
