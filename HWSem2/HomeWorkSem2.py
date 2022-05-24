# Найти сумму чисел списка стоящих на нечетной позиции
import random
def get_sum(list):
    sum = 0
    for i in range(1, len(list), 2):
        sum += list[i]
    return sum


print(get_sum([1, 2, 3, 4, 5, 6, 7, 8, 9]))
# Найти произведение пар чисел в списке. Парой считаем первый и последний элемент, второй и предпоследний и т.д.
# Пример: [2, 3, 4, 5, 6] => [12, 15, 16]; [2, 3, 5, 6] => [12, 15]
def get_product(list):
    left, right, product, prod_list = 0, len(list) - 1, 0, []
    while left <= right:
        product = list[left] * list[right]
        prod_list.append(product)
        left += 1
        right -= 1
    return prod_list


print(get_product([2, 3, 4, 5, 6]))
print(get_product([2, 3, 5, 6]))
# В заданном списке вещественных чисел найдите разницу между максимальным и минимальным значением дробной части элементов.
# Пример: [1.1, 1.2, 3.1, 5, 10.01] => 0.19
def get_diff(list):
    max_part = 0
    min_part = 1
    for i in list:
        max_part = max(max_part, i % 1)
        min_part = min(min_part, (1 if i % 1 == 0 else i % 1))
    return max_part - min_part

print(get_diff([1.1, 1.2, 3.1, 5, 10.01]))
# Написать программу преобразования десятичного числа в двоичное
def dec_to_bin(dec_number,):
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
    if bin_number == 0:
        return 0
    if bin_number % 10 == 1:
        return bin_to_dec(bin_number // 10) * 2 + 1
    else:
        return bin_to_dec(bin_number // 10) * 2


k = lambda bin_number: 0 if bin_number == 0 else bin_to_dec(bin_number // 10) * 2 + (1 if bin_number % 10 == 1 else 0)  # just a way to solve

print(bin_to_dec(1100010))
print(k(1100010))

#2. Создайте программу, которая будет играть в игру “коровы и быки” с пользователем. Игра работает так:
# Случайным образом генерируйте 4-значное число. Попросите пользователя угадать 4-значное число.
# За каждую цифру, которую пользователь правильно угадал в нужном месте, у них есть “корова”.
# За каждую цифру, которую пользователь угадал правильно, в неправильном месте стоит “бык”.
# Каждый раз, когда пользователь делает предположение, скажите им, сколько у них “коров” и “быков”.
# Как только пользователь угадает правильное число, игра окончена. Следите за количеством догадок,
# которые пользователь делает на протяжении всей игры, и сообщите пользователю в конце.
def bulls_and_cows():
    def get_digits(num, list):
        if num == 0:
            return list
        else:
            list.insert(0, num % 10)
            return get_digits(num // 10, list)

    n = random.randint(1000, 9999)
    print(f'initial n: {n}')
    digits = get_digits(n, [])
    flag = True
    counter = 0

    while flag:
        counter += 1
        print('Enter a number')
        num = int(input())
        bulls = 0
        cows = 0
        if num == n:
            flag = False
            print(f'you won, steps done: {counter}')
        curr_digits = get_digits(num, [])
        for i in range(0, 4):
            if curr_digits[i] == digits[i]:
                bulls += 1
            if curr_digits[i] in digits:
                cows += 1
        cows -= bulls
        print(f'bulls = {bulls}, cows = {cows}')

    print(f'digits {digits}')

    return n

print(bulls_and_cows())

# 3.Каждый следующий элемент ряда Фибоначчи получается при сложении двух предыдущих. Начиная с 1 и 2, первые 10 элементов будут:
# 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
def get_fib_list(N):
    f1, f2, list = 1, 0, [0]
    for i in range(0, N):
        f2 = f2 + f1
        f1 = f2 - f1
        list.append(f2)
        list.insert(0, f2 if i % 2 == 0 else -f2)
    return list


print(get_fib_list(989))
# 4. Простые делители числа 13195 - это 5, 7, 13 и 29.
# Каков самый большой делитель числа 600851475143, являющийся простым числом?
def get_primes(n):  # Eratosthenes' sieve
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
    max_prime_div = 1
    divisors = get_primes(int (number ** 0.5))
    for i in divisors:
        if number % i == 0:
            max_prime_div = i
    return max_prime_div


print(get_primes(100))
print(get_max_prime_divisor(600851475143))
print(get_max_prime_divisor(87625999))
print(600851475143 / 6857)

# 5. 2520 - самое маленькое число, которое делится без остатка на все числа от 1 до 10.
# Какое самое маленькое число делится нацело на все числа от 1 до 20?
def min_number(N):

    factors = get_primes(int(N ** 0.5) + 1)

    def get_factors(number):
        primes = factors  # get_primes(int(number ** 0.5) + 1)
        factor_dict = {1: 1}
        for i in primes:
            if i * i > number:
                break
            while number != 0 and number % i == 0:
                number /= i
                # print(f'number = {number}')
                if i in factor_dict:
                    factor_dict[i] += 1
                else:
                    factor_dict[i] = 1
            if number == 1:
                break
        if number != 1:
            # print(f'lala {number}')
            factor_dict[number] = 1
        return factor_dict

    res_factor_dict = {1: 1}
    product = 1

    for i in range(2, N + 1):
        curr_f_dict = get_factors(i)
        for item in curr_f_dict:
            if item in res_factor_dict:
                res_factor_dict[item] = max(res_factor_dict[item], curr_f_dict[item])
            else:
                res_factor_dict[item] = curr_f_dict[item]

    for i in res_factor_dict:
        product *= int(i ** res_factor_dict[i])

    print(res_factor_dict)

    return product


print(min_number(10))
print(min_number(20))
print(min_number(100))
print(min_number(100000))

# print(get_factors(9366))
