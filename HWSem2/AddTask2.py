# 2. Создайте программу, которая будет играть в игру “коровы и быки” с пользователем. Игра работает так:
# Случайным образом генерируйте 4-значное число. Попросите пользователя угадать 4-значное число.
# За каждую цифру, которую пользователь правильно угадал в нужном месте, у них есть “корова”.
# За каждую цифру, которую пользователь угадал правильно, в неправильном месте стоит “бык”.
# Каждый раз, когда пользователь делает предположение, скажите им, сколько у них “коров” и “быков”.
# Как только пользователь угадает правильное число, игра окончена. Следите за количеством догадок,
# которые пользователь делает на протяжении всей игры, и сообщите пользователю в конце.

import random


def bulls_and_cows():
    def get_digits(number, digits_list):
        """
        :param number: a number whose digits we want to get
        :param digits_list: aux list of digits
        :return: list of digits of a number given
        """
        if number == 0:
            return digits_list
        else:
            digits_list.insert(0, number % 10)
            return get_digits(number // 10, digits_list)

    n = random.randint(1000, 9999)  # a random generation of 4-digit number
    digits = get_digits(n, [])  # list of digits of picked number
    flag = True  # flag of game being on
    counter = 0  # counter of tries

    print('THE GAME "BULLS AND COWS" BEGINS!' )

    while flag:  # the main game-cycle
        counter += 1
        print('Enter a 4-digit number')

        str_number = input()

        if str_number == 'Exit' or str_number == 'exit':  # stop-game condition
            print('The game is ended')
            break

        num = int(str_number)

        if num < 1000 or num > 9999:
            continue
        bulls, cows = 0, 0  # bulls and cows counters
        if num == n:  # a win-case
            flag = False
            print(f'you won, steps done: {counter}')
        curr_digits = get_digits(num, [])
        digits_clone = digits.copy()

        # print(f'init_num: {digits}')

        for i in range(0, 4):
            if curr_digits[i] == digits_clone[i]:
                cows += 1
        for i in range(0, 4):
            if curr_digits[i] in digits_clone:
                digits_clone.remove(curr_digits[i])
                bulls += 1
        bulls -= cows
        print(f'bulls = {bulls}, cows = {cows}')


bulls_and_cows()  # here the game starts
