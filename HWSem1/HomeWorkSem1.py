def get_first_n_members_of_seq(length):  # Сформировать список из N членов последовательности. Для N = 5: 1, -3, 9, -27, 81 и т.д.
    list = []
    pow = 1

    for i in range(0, length):
        list.append(pow)
        pow *= -3

    return list


def count_overlapping_substrings(s1, s2):  # Пользователь вводит две строки, определить количество вхождений одной строки s2 в другую s1
    counter = 0
    i = -1
    while True:
        i = s1.find(s2, i + 1)
        if i == -1:
            return counter
        counter += 1


def get_factorial_list(length):  # Сформировать программу, получающую набор произведений чисел от 1 до N. Для N = 4: [1, 2, 6, 24]
    list = []
    curr_fact = 1

    for i in range(1, length + 1):
        curr_fact *= i
        list.append(curr_fact)

    return list


def get_digit_sum(number):  # Посчитать сумму цифр в вещественном числе
    while number % 1 != 0:
        number *= 10
    print(f'number = {number}')

    sum = 0

    while number > 0:
        sum += number % 10
        number //= 10

    return sum

def write_in_morse(str):
    char_to_dots = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', ' ': ' ', '0': '-----',
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.',
        ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-',
        '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.'
    }

    result = ''

    for symbol in str.upper():
        result += char_to_dots[symbol]

    return result


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


def guess_what_num(left, right):  # computer try to guess what number we picked
    counter = 0

    print(f'The game begins!\n\nPlease pick a number between {left} and {right} then let the computer guess it')

    while left < right:
        pivot = (left + right) // 2

        print(f'{counter}-th try: is number equal to {pivot}? (enter: less, more or yes)')

        str = input()

        if str == "more":
            counter += 1
            left = pivot
        elif str == "less":
            counter += 1
            right = pivot
        elif str == "yes":
            print(f'number is {pivot} - right, been found in {counter} steps!')
            return
        else:
            print("enter: less, more or yes")



print(count_overlapping_substrings('avarnikabcdefabcdefabc', 'abcdefabc')) # an example for 1st task

print('avarnikabcdefabcdefabc'.count('abcdefabc'))
# -> 6

print(get_first_n_members_of_seq(8))  # an example for 2nd task

print(get_factorial_list(9))  # an example for 3rd task

print(get_digit_sum(987.123))  # an example for 4th task

print(write_in_morse('Ruslan is strange person'))

print(get_palindrome(21136698629, True))

# print(get_palindrome(988999888899999))  # -->> eternal cycle

guess_what_num(0, 127)
