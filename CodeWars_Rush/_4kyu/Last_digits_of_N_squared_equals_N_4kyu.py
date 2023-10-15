import time


def green(n):  #36 366 98 989
    print(f'n: {n}')

    automorph_numbers = []

    num1, num2 = 5, 6
    automorph_numbers += [num1, num2]
    counter, digit_counter = 2, 2

    while counter < n + n // 5:
        power_of_ten = 10 ** digit_counter
        num1 = num1 ** 2 % power_of_ten
        num2 = power_of_ten + 1 - num1
        print(f'num1, num2: {num1, num2}')
        automorph_numbers += [num1, num2]
        counter += 2
        digit_counter += 1

    automorph_numbers = list(sorted(automorph_numbers))
    automorph_numbers = [1] + automorph_numbers

    return automorph_numbers[n - 1]


start = time.time_ns()
print(green(100))
end = time.time_ns()
print(f'time elapsed: {(end - start) // 10 ** 6} milliseconds')


# k = ordered_set(range(1000))
# print(k)
# k |= ordered_set(range(7000, 7000 + 1))
# print(k)
