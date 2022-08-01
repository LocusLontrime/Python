# accepted on codewars.com
max_palindrome = -1
counter = 0


def numeric_palindrome(*args):
    global max_palindrome, counter
    max_palindrome = 0

    args = list(args) # for convenience

    # here we delete all the
    count_of_0 = 0
    count_of_1 = 0

    for el in args:
        if el == 0:
            count_of_0 += 1
        elif el == 1:
            count_of_1 += 1

    if count_of_1 > 2:
        for i in range(count_of_1 - 2):
            args.remove(1)

    if count_of_0 > 1:
        for i in range(count_of_0 - 1):
            args.remove(0)

    # here we check all the combinations of products of numbers given in the array *args
    def recursive_seeker(prev_mult, prev_index, curr_chain_length):
        global max_palindrome, counter

        counter += 1

        # base cases
        if prev_index == len(args):
            curr_max_palindrome = get_max_number_palindrome(prev_mult)

            print(f'finishing palindrome num: {curr_max_palindrome}')

            if curr_max_palindrome not in args and curr_max_palindrome > max_palindrome:
                max_palindrome = curr_max_palindrome

            return

        # body of rec
        curr_max_palindrome = get_max_number_palindrome(prev_mult)

        print(f'curr_max_palindrome: {curr_max_palindrome}')

        if curr_chain_length > 1 and curr_max_palindrome > max_palindrome:
            max_palindrome = curr_max_palindrome

        # recursion depth, here we prevent any repeats
        for index in range(prev_index + 1, len(args)):

            recursive_seeker(prev_mult * args[index], index, curr_chain_length + 1)

    # recursive call
    recursive_seeker(1, -1, 0)

    return max_palindrome


# finds the maximum numeric palindrome that can be build from the digits of the number given
def get_max_number_palindrome(number):  # 1877567751 {1:2, 5:2, 6:1, 7:4, 8:1}
    numbers_dict = dict()

    # here we get the dictionary of numbers of the pivot number
    def rec_seeker(number_remained):
        # the base case
        if number_remained == 0:
            return

        # the body of recursion
        curr_digit = number_remained % 10

        if curr_digit in numbers_dict.keys():
            numbers_dict[curr_digit] += 1
        else:
            numbers_dict[curr_digit] = 1

        # recursion depth
        rec_seeker(number_remained // 10)

    # invocation of rec method
    rec_seeker(number)

    this_max_palindrome = ''
    rev = sorted(numbers_dict)[::-1]  # sorts the keys in decreasing order

    # here we are building the left part of max palindrome
    for key in rev:
        if key == 0 and this_max_palindrome == '':
            continue

        while numbers_dict[key] > 1:
            this_max_palindrome = this_max_palindrome + str(key)
            numbers_dict[key] -= 2

    pivot_el = ''

    # adding the core of palindrome if such digit remained
    for key in rev:
        if numbers_dict[key] > 0:
            pivot_el += str(key)
            break

    # now we can get the full max palindrome
    res = this_max_palindrome + pivot_el + this_max_palindrome[::-1]

    return int(res) if res != '' else -1


# print(get_max_number_palindrome(1877567751))
#
#
# print([1, 2, 3, 4, 5, 6][:2] + [1, 2, 3, 4, 5, 6][3:])


# print(f'res: {numeric_palindrome(91, 2096, 8, 6, 615)}, counter: {counter}')
# # print((91 * 2096 * 8 * 6 * 615))
#
# print(get_max_number_palindrome(15000))

print(numeric_palindrome(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

print(get_max_number_palindrome(6))
