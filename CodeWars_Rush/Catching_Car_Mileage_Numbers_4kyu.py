# accepted on codewars.com
def is_interesting(number, awesome_phrases):

    if number <= 7:
        return 0

    if 97 < number < 100:
        return 1

    def digit_and_zeroes(num):
        return str(num)[0] != '0' and set(str(num)[1:]) == set('0')

    def seq_incremental(num, flag):
        num_str = str(num)
        prev_digit = num_str[0]

        for i in range(1, len(num_str)):
            curr_num = (int(prev_digit) + (1 if flag else -1)) % 10

            if curr_num == 0 and i != len(num_str) - 1:
                return False

            if num_str[i] != str(curr_num):
                return False

            prev_digit = num_str[i]

        return True

    def all_the_same_ones(num):
        return len(set(str(num))) == 1

    def palindrome_num(num):
        return str(num) == str(num)[::-1]

    def awesome(num):
        return num in awesome_phrases

    def is_interesting_one(num):
        return digit_and_zeroes(num) or seq_incremental(num, True) or seq_incremental(num, False) or all_the_same_ones(num) or palindrome_num(num) or awesome(num)

    if is_interesting_one(number):
        return 2

    for i in range(number + 1, number + 3):
        if is_interesting_one(i):
            return 1

    return 0


print(is_interesting(1335, [1337, 256]))  # 1
print(is_interesting(11211, []))  # 2


