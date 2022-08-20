# accepted on codewars.com
from functools import reduce
upside_down_digits = [0, 1, 6, 8, 9]
upside_down_digits_reflected = {0: 0, 1: 1, 6: 9, 8: 8, 9: 6}
upside_down_digits_middle = [0, 1, 8]


def upsidedown(x: str, y: str) -> int:  # 1608091
    # border cases of left value included
    return upside_downs_before_n(y) - (int(x) if x in ['0', '1'] else upside_downs_before_n(str(int(x) - 1)))


def upside_downs_before_n(n: str) -> int:
    length = len(n)
    numbers_quantity = reduce(lambda y, x: y + x, [n_digit_upside_downs(k) for k in range(1, length)], 0)  # all upside down numbers before the max power of ten that are less than n
    print(f'numbers quantity: {numbers_quantity}')

    digits_before_quantity = [0] * int((length + 1) / 2)  # array for counting the number of upside-down digits less than the relative digit on the left side of the n

    # calculating digits_before_quantity's elements in cycle
    for index in range(len(digits_before_quantity)):
        for num in upside_down_digits_middle if length % 2 == 1 and index == int((length - 1) / 2) else upside_down_digits:  # here we count the case of one digit in the middle of number n
            if num < int(n[index]) and not(index == 0 and num == 0):  # n cannot have an opening zero
                digits_before_quantity[index] += 1

    print(f'digits_before_quantity: {digits_before_quantity}')

   # cycling all over the left sided digits in n (including the middle one if such exists)
    for i in range(len(digits_before_quantity)):
        current_digit = int(n[i])
        possible_digits_quantity = 0

        len_remained = (length - 2 * i) // 2 - 1  # the length of remained digits chain starting at the current_digit (not including) and ending at middle digits (not including)

        # border cases in cycle, here we reach the middle point of n for both cases (n is oven or odd)
        if len_remained == 0 and length % 2 == 0 or len_remained == -1 and length % 2 == 1:
            inner_flag = int(n[i]) in (upside_down_digits if len_remained == 0 else upside_down_digits_middle)

            # checks if the n is upside down or can be upside down with the left side built
            if inner_flag:
                for q in range(i, 0 - 1, -1):
                    if int(n[length - 1 - q]) > upside_down_digits_reflected[int(n[q])]:
                        break
                    elif int(n[length - 1 - q]) < upside_down_digits_reflected[int(n[q])]:
                        inner_flag = False
                        break

            possible_digits_quantity += digits_before_quantity[i] + (1 if inner_flag else 0)
        else:
            possible_digits_quantity = digits_before_quantity[i] * 5 ** len_remained * (3 if length % 2 == 1 else 1)

        numbers_quantity += possible_digits_quantity

        print(f'n[i]: {n[i]}, possible_digits_quantity: {possible_digits_quantity}, l: {len_remained}')

        # if the sequence of current digits cannot now build an upside-down number-border we must break
        if current_digit not in (upside_down_digits_middle if length % 2 == 1 and i == int((length - 1) / 2) else upside_down_digits):
            break

    # counts the null case
    return numbers_quantity + (1 if length == 1 else 0)  # (1 if (length % 2 == 1 and n[(length - 1) // 2] in upside_down_digits_middle) else 0)


# counts the n-digits upside down numbers
def n_digit_upside_downs(n: int) -> int:
    return 4 * 5 ** (n // 2 - 1) * (3 if n % 2 == 1 else 1) if n > 1 else 3


# print(n_digit_upside_downs(10))
# print(n_digit_upside_downs(5))
# print(n_digit_upside_downs(4))
# print(n_digit_upside_downs(3))
# print(n_digit_upside_downs(2))
# print(n_digit_upside_downs(1))
#
#
# print(upside_downs_before_n('12345678900000000') - upside_downs_before_n('100000'))
#
# print(upside_downs_before_n('100000'))
#
# print([1, 2, 3, 4, 5, 6][0:])
#
# print('36 366 98 989')
#
# print(2 * 5 ** 6 * 3)

# print(upside_downs_before_n('0'))
# print(upside_downs_before_n('10'))
#
# print(upside_downs_before_n('6'))
# print(upside_downs_before_n('25'))
#
# print(upside_downs_before_n('100'))
# print(upside_downs_before_n('1000'))
# #
# print(upside_downs_before_n('6'))
# print(upside_downs_before_n('25'))

# print(upsidedown('100', '1000'))

# print(upside_downs_before_n('7'))
#

# print(upsidedown('100000', '12345678900000000'))
#
# print(f"for 100000: {upside_downs_before_n('100000')}")
# print(f"for 99999: {upside_downs_before_n('99999')}")

# print(upsidedown('1', '45898942362076547326957326537845432452352'))

# print(f"for 45898942362076547326957326537845432452352: {upside_downs_before_n('45898942362076547326957326537845432452352')}")
# print(f"for 1: {upside_downs_before_n('1')}")
# print(f"for 0: {upside_downs_before_n('0')}")
#

print(upside_downs_before_n('91860016911896699999881969116891999999999990000081801698146670000000000186753656598712475643285764768901111186787'))
# print(len('91860016911896699999881969116891999999999990000081801698146670000000000186753656598712475643285764768901111186787'))

print('36.6')

