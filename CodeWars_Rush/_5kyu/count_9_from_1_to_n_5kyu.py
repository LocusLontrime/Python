# accepted on codewars.com
import math


# too long
def count_nines(max_num):

    # memoization
    memo_table = [-1] * len(str(max_num))

    # inner recursive method, algo core
    def recursive_seeker(n: int) -> int:
        if n < 10:
            if n < 9:
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
        if int(number) == 9:
            count_all += n - 9 * int(math.pow(10, str_num - 1)) + 1

        if n == int(math.pow(10, str_num - 1)) - 1 and memo_table[str_num - 1] == -1:
            memo_table[str_num - 1] = count_all

        return count_all

    return recursive_seeker(max_num)


# fast enough
def count_nines_fast(n):

    def rec_count(num):
        if num == 0:
            return 0
        else:
            digit = num % 10
            rem_n = num // 10
            return 10 * rec_count(rem_n) + rem_n + sum(str(10 * rem_n + i).count('9') for i in range(digit))

    return rec_count(n + 1)


print(count_nines(908))
print(count_nines_fast(908))

# print(int('000989'))
