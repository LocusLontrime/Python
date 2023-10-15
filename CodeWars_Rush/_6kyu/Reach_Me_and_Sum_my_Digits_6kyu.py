def sum_dig_nth_term(init_val, pattern_l, nth_term):  # accepted on codewars.com
    def digits_sum(number):
        if number == 0:
            return 0
        else:
            return digits_sum(number // 10) + number % 10
    # print(digits_sum(init_val))
    nth_term -= 1

    elements_sum = 0
    elements_partial_sum = 0

    for i in pattern_l:
        elements_sum += i

    length = len(pattern_l)

    rem = nth_term % length

    for i in range(0, rem):
        elements_partial_sum += pattern_l[i]

    multiple = nth_term // length

    # print(f'number = {init_val + multiple * elements_sum + elements_partial_sum}')

    return digits_sum(init_val + multiple * elements_sum + elements_partial_sum)


print(sum_dig_nth_term(10, [1, -2, 3, -4, 5, -6, 7, -8, 9], 222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222))  # 23


# return x  # sum of digits of nthTerm of the generated sequence

