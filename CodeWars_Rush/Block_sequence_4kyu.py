# accepted on codewars.com (some troubles: 101, 804...)
import math

preset_str = ''

for i in range(1, 10):
    for j in range(1, i + 1):
        preset_str += str(j)


print(preset_str)


def solve(n):
    if n <= 45:
        return int(preset_str[n - 1])
    else:
        return int(get_numbers_in(get_blocks_in(n)))


def get_blocks_in(number):
    def get_powers_of_ten_in(n):
        aggregated_length = 0  # the length of the block sequence [1],[1,2],... in this representation "112123..." limited by power of ten

        i = 1  # iterations counter
        multiplier = 9  # quantity of i-digit numbers (0 excluded)
        seq_length = 0  # length of numbers sequence started from 1 to 10 ** (i - 1) - 1
        while True:
            seq_length += (multiplier // 10) * (i - 1)
            new_length = aggregated_length + seq_length * multiplier + i * multiplier * (multiplier + 1) // 2

            if n - new_length < 0:  # here the length current block sequence exceeds number, cycle should be stopped
                i -= 1
                break
            else:
                aggregated_length = new_length

            multiplier *= 10
            i += 1

        return i, aggregated_length, seq_length  # max power of ten, block seq length and prev seq length

    power, l_n_prev, seq = get_powers_of_ten_in(number)
    print(f'power: {power}')  # testing

    part = 2 * seq / (power + 1) + 1  # calc for convenience

    # how many blocks find their place after the max power of ten?
    k = math.floor((-part + math.sqrt((part ** 2 + 8 * (number - l_n_prev) / (power + 1)))) / 2)

    max_n = 10 ** power - 1 + k  # the max possible block number

    return number - l_n_prev - seq * k - (power + 1) * k * (k + 1) // 2  # the max possible block number and the length remained


def get_numbers_in(number_remained):

    print(f'number remained: {number_remained}')

    def get_powers_of_ten_in(rem):

        aggregated_length = 0

        i = 1
        multiplier = 9
        while True:

            new_length = aggregated_length + multiplier * i

            if rem - new_length < 0:
                i -= 1
                break
            else:
                aggregated_length = new_length

            multiplier *= 10
            i += 1

        return i, aggregated_length

    power, length_before_max_power_of_ten = get_powers_of_ten_in(number_remained)

    max_num_before_max_power_of_ten = 10 ** power - 1

    k = math.floor((number_remained - length_before_max_power_of_ten) / (power + 1))

    max_num_before_the_num_given = max_num_before_max_power_of_ten + k

    index_of_digit = number_remained - length_before_max_power_of_ten - k * (power + 1)

    print(f'max num: {max_num_before_the_num_given}, index of digit: {index_of_digit}')

    return str(max_num_before_the_num_given)[-1] if index_of_digit == 0 else str(max_num_before_the_num_given + 1)[index_of_digit - 1]


# some optimization in terms of code lines
def get_blocks_num(number: int) -> int:

    def bin_rec_search(left_num, right_num):

        if left_num == right_num:
            return left_num

        pass

    pass


# print(9 // 10)
#
# print(get_blocks_in(11))
# print(get_blocks_in(17))
# print(get_blocks_in(56))

# print(solve(100))
# print(solve(2100))
# print(solve(31000))
# print(solve(999999999999999999))
# print(solve(1000000000000000000))
# print(solve(999999999999999993))
#
# print(get_numbers_in(10))

print(solve(1))
print(solve(2))
print(solve(3))

print(solve(10))


print(solve(804))
print(solve(101))

