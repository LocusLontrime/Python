# accepted on codewars.com 36 366 98 989 98989
import time

recursive_counter = 0
strs = []


def elder_age(m: int, n: int, l: int, t: int) -> int:
    global recursive_counter, strs
    string_builder = ''
    result = 0

    # returns the minimal power of two that is bigger than the number
    def min_bigger_power_of_two(num: int) -> int:
        res = 1
        while res < num:
            res *= 2

        return res

    # calculates consecutive sum from l value to r inclusively
    def calc_sum(left_value: int, right_value: int) -> int:
        if right_value <= 0:
            return 0
        if left_value <= 0:
            left_value = 1
        return (right_value * (right_value + 1) - (left_value - 1) * left_value) // 2

    # some print
    recursive_counter += 1
    string_builder += f'{recursive_counter}-th step: m, n, l, t = {m}, {n}, {l}, {t}\n'
    # just for convenience let n be the max of two (m, n) values
    if n < m:
        n, m = m, n
        string_builder += f'    n < m case, the values has been swapped, now: m, n = {m}, {n}\n'
    # now let us find the borders of our calculations, they will be the minimal powers of two,
    # that bigger than m and n respectively
    pow_n, pow_m = min_bigger_power_of_two(n), min_bigger_power_of_two(m)
    string_builder += f'    pow_m: {pow_m}, pow_n: {pow_n}, loss: {l}\n'
    # base case:
    if 0 in [m, n]:
        string_builder += f'    {m if n else n} = 0, elder gets 0 seconds'
        result = 0
    # border case, if there is no need in further calculations, coz of nullifying the transmission by prevailing losses:
    elif l >= pow_n:
        string_builder += f'    l: {l} > pow_n: {pow_m}'
        result = 0
    # this is more suitable situation, worshippers' rectangle located between pow_n and pow_n//2 borders and
    # the field of calculations is pow_n * pow_n:
    elif pow_n == pow_m:
        string_builder += f'    pow_n == pow_m case\n'
        string_builder += f'    base sum: {(base_sum := (m + n - pow_n) * calc_sum(1, pow_n - l - 1))}, next elder: {(next_elder := elder_age(pow_m - m, pow_n - n, l, t))}\n'
        result = (base_sum + next_elder) % t
    # more complicated situation, the calculations are being performed in pow_n // 2 * pow_n rectangle:
    elif pow_n > pow_m:
        string_builder += f'    pow_n > pow_m case\n'
        # horizontal border of calculations field
        pow_m_new = pow_n // 2
        string_builder += f'    pow_m been changed, now pow_m: {pow_m_new}\n'
        # sum of XORs in pow_m_new * pow_n rectangle
        string_builder += f'    pow_m_new * pow_n rectangle sum: {(rectangle_sum := pow_m_new * calc_sum(1, pow_n - l - 1))}, constant sum from upper-right square: {(constant_sum := (pow_m_new + pow_n - m - n) * calc_sum(pow_m_new - l, pow_n - l - 1))}\n'
        # addition and return, inner case of comparison pow_m_new and l
        string_builder += f'    {"pow_m_new > l case" if pow_m_new > l else "pow_m_new <= l case"}\n'
        string_builder += f'    variable sum from upper left square: {(variable_sum := (pow_m_new - m) * calc_sum(1, pow_m_new - l - 1))}, additional to elder sum from upper right square: {(additional_sum := (pow_m_new - l if pow_m_new > l else 0) * (pow_m_new - m) * (pow_n - n))}, next elder: {(next_elder := elder_age(pow_m_new - m, pow_n - n, l - pow_m_new if pow_m_new < l else 0, t))}\n'
        result = (rectangle_sum - constant_sum - variable_sum + additional_sum + next_elder) % t

    string_builder += f'STEP RESULT: {result}\n'
    strs.insert(0, string_builder)

    recursive_counter -= 1

    if not recursive_counter:
        print_log()
        print('FINAL RESULT: ', end='')

    return result


def print_log():
    global strs
    for string in strs:
        print(string)


# print(elder_age(8, 5, 1, 100))
# print(elder_age(25, 31, 0, 100007))
# print(elder_age(545, 435, 342, 1000007))

start = time.time_ns()
print(elder_age(28827050410, 35165045587, 7109602, 13719506))
finish = time.time_ns()

print(f'Time elapsed: {(finish - start) // 10 ** 6} milliseconds')


def calc_sum_new(left_value: int, right_value: int) -> int:
    if left_value <= 0:
        left_value = 1
    return (right_value * (right_value + 1) - (left_value - 1) * left_value) // 2

# print(calc_sum_new(-10, 5))


# print(math.log2(35165045587))

