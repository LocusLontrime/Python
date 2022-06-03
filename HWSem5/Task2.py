# 2. Вы когда-нибудь играли в игру "Крестики-нолики"?
# Попробуйте создать её, причем чтобы сыграть в нее можно было в одиночку.
from functools import reduce

xs_os = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]


def play_xs_os():
    turns_counter = 0

    while True:

        turns_counter += 1

        while True:

            print(f'Turn: {turns_counter}')
            print('Enter a coordinates to put your sign')
            point = tuple(input())
            point = int(point[0]), int(point[1])

            flag = turns_counter % 2 == 1

            if xs_os[point[0]][point[1]] == 0:
                xs_os[point[0]][point[1]] = -1 if flag else 1
                print(f'Player №{1 if flag else 2} puts a {"cross" if flag else "zero"} in point with coords: {point}')
                break
            else:
                print(f'the cell is busy, choose a different coords')

        print('Board: ')
        for i in range(3):
            print(xs_os[i])
        print()
        # checks 1. whether player wins or 2. game_is_over

        for i in range(3):  # verticals & horizontals
            sum1 = reduce(lambda x, y: x + y, [xs_os[0][i], xs_os[1][i], xs_os[2][i]])
            sum2 = reduce(lambda x, y: x + y, [xs_os[i][0], xs_os[i][1], xs_os[i][2]])
            if sum1 == 3 or sum2 == 3:
                print(f'Player2 wins the game!!!')
                print('The game is finished')
                return
            if sum1 == -3 or sum2 == -3:
                print(f'Player1 wins the game!!!')
                print('The game is finished')
                return

        d = [xs_os[x][x] for x in range(3)]

        main_diag_sum = xs_os[0][0] + xs_os[1][1] + xs_os[2][2]
        aux_diag_sum = xs_os[2][0] + xs_os[1][1] + xs_os[0][2]

        if main_diag_sum == 3 or aux_diag_sum == 3:
            print(f'Player2 wins the game!!!')
            break
        if main_diag_sum == -3 or aux_diag_sum == -3:
            print(f'Player1 wins the game!!!')
            break

        if turns_counter == 9:
            print('No one wins...')
            break

    print('The game is finished')


play_xs_os()

# matrix = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]
#
# d = [matrix[x][x] for x in range(3)]
# c = [matrix[2 - x][x] for x in range(3)]
#
# print(d)
# print(c)


