# -*- coding: utf-8 -*-
# Task 3. Программа загадывает число от 0 до 1000. Необходимо угадать число за 10 попыток.
# Программа должна подсказывать “больше” или “меньше” после каждой попытки. Для генерации случайного числа используйте код:
# from random import randint
# num = randint(LOWER_LIMIT, UPPER_LIMIT)
import random


def start_game():
    TRIES = 10
    LOW_BOUND, UPPER_BOUND = 0, 1000
    # the program picks a random number:
    num_picked = random.randint(LOW_BOUND, UPPER_BOUND)
    print(f'The game starts. You have only {TRIES} attempts to GUESS the integer num from '
          f'{LOW_BOUND} to {UPPER_BOUND}! Have a fun!..')
    for i in range(TRIES):
        while True:
            string = input(f'your guess: ')
            if string.isdigit():
                num_guessed = int(string)
                if num_guessed < LOW_BOUND or num_guessed > UPPER_BOUND:
                    print(f"you've guessed the number that does not fit the interval from "
                          f'{LOW_BOUND} to {UPPER_BOUND}, but it is your fail, an attempt has been used...')
                break
            else:
                print(f'please, enter some number, not a string')
        if num_guessed == num_picked:
            text = f'CONGRATULATIONS, you won, using {i + 1} attempts.'
        else:
            text = f"your number is {'bigger' if num_guessed > num_picked else 'lower'} " \
                   f"then the number picked, {TRIES - i - 1} attempts remained..."
        print(text)
    print(f'Sorry, you lost! All {TRIES} attempts have been used, the number picked is: {num_picked}')


start_game()






























































