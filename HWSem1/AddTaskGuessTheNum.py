#  Напишите программу, обратную предыдущей: теперь вы загадываете число, а компьютер отгадывает.

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


guess_what_num(1, 127)

