# accepted on codewars.com
import math
from functools import reduce


# max recursion depth exceeded for the max text value = 9000000000000000000
def count_digit_five(max_num: int) -> int:

    memo_table = [-1] * len(str(max_num))

    def recursive_seeker(n: int) -> int:
        if n < 10:
            if n < 5:
                return 0
            else:
                return 1

        str_num = math.floor(math.log10(n)) + 1
        number = str(n)[0]

        if n == int(math.pow(10, str_num - 1)) - 1 and memo_table[str_num - 1] != -1:
            return memo_table[str_num - 1]

        count_all = 0

        # first phase
        count_all += recursive_seeker(n - int(number) * int(math.pow(10, str_num - 1)))

        # second phase
        count_all += int(number) * recursive_seeker(int(math.pow(10, str_num - 1) - 1))

        # third phase
        if int(number) >= 6:
            count_all += int(math.pow(10, str_num - 1))
        elif int(number) == 5:
            count_all += n - 5 * int(math.pow(10, str_num - 1)) + 1

        if n == int(math.pow(10, str_num - 1)) - 1 and memo_table[str_num - 1] == -1:
            memo_table[str_num - 1] = count_all

        return count_all

    return recursive_seeker(max_num)


def dont_give_me_five(start, end):
    # count the numbers from start to end that don't contain the digit 5
    counter = 0

    # manipulation with diff ends of interval given and method below
    if start == 0 and end == 0:
        return 0
    elif end == 0:
        return cycle_count_digit_without_five(abs(start)) + 1
    elif start == 0:
        return cycle_count_digit_without_five(abs(end)) + 1
    elif start * end < 0:
        counter += cycle_count_digit_without_five(abs(start)) + cycle_count_digit_without_five(abs(end)) + 1
    else:
        counter += abs(cycle_count_digit_without_five(abs(start)) - cycle_count_digit_without_five(abs(end))) + (1 if '5' not in str(min(abs(start), abs(end))) else 0)

    return counter


# a fast solution
def cycle_count_digit_without_five(max_num):
    # a string representation of a max number given
    str_max_num = str(max_num)
    new_num = ''  # a string for a new num

    for i in range(0, len(str_max_num)):  # some operations on number given: 19645779 -> 1854 5 999 -> 1854 4 888 -> 18545999 -> 1*9^4 + 4*9^3 + 8*9^2 + 8*9^1 + 8*9^0 = number
        if str_max_num[i] == '5':
            new_num += '4'
            new_num += '8' * (len(str_max_num) - i - 1)
            break

        new_num += (str(int(str_max_num[i]) - 1) if int(str_max_num[i]) > 5 else str_max_num[i])

    result = 0

    # translating to a system with base 10 from 9:
    for i in range(0, len(new_num)):
        result += int(new_num[i]) * 9 ** (len(new_num) - i - 1)

    return result

#
# print(int('1001', 9))


# print(count_digit_five(64))
# print(count_digit_five(65))
# print(count_digit_five(66))
# print(count_digit_five(99))
# print(count_digit_five(9000000000000000000))

# cycle_count_digit_without_five(19989856661)
# cycle_count_digit_without_five(144366)
# print(cycle_count_digit_without_five(90))
# print(cycle_count_digit_without_five(1001))

print(dont_give_me_five(984, 4304))  # 2449
print(dont_give_me_five(51, 60))  # 1
print(dont_give_me_five(-4436, -1429))  # 2194
print(dont_give_me_five(-2490228783604515625, -2490228782196537011))  # 520812180
print(dont_give_me_five(-9000000000000000000, 9000000000000000000))  # 2401514164751985937
print(dont_give_me_five(40076, 2151514229639903569))  # 326131553237897713
print(dont_give_me_five(-206981731, 2235756979031654521))  # 340132150309630357
print(dont_give_me_five(0, 1))
print(dont_give_me_five(5, 15))
print(dont_give_me_five(-5, 4))





