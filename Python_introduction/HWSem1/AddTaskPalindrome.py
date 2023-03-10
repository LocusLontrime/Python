# Есть такая вещь - палиндром. Это когда слово читается с обеих сторон одинаково.
# Например, слово "шалаш". Также есть числовой палиндром. Если при обратном чтении числа (124 - 421)
# не получается то же самое, то они складываются (124+421) и проверяются вновь.
# Попробуйте написать функцию (или просто программу, но лучше все же функцию), находящую числовой палиндром

def get_palindrome(number, flag):

    def reverse(n):
        new_n = 0

        while n > 0:
            new_n *= 10
            new_n += n % 10
            n //= 10

        return new_n

    def is_palindrome(num):
        return reverse(num) == num

    counter = 0

    while not is_palindrome(number):  # an easy optimization -->> one call of reverse and then comparison
        number = number + reverse(number)
        counter += 1
        if flag:
            print(f'current number: {number}, counter: {counter}')

    return f'final number {number}'


print(get_palindrome(21136698629, True))

