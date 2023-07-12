# accepted on coderun
import sys


deltas = ((1, 1), (-1, 1), (-1, -1), (1, -1))


def cut_down():
    n, m, w, b, whites, blacks, turn = get_pars()
    checkers_board = [[' ' for i in range(n)] for j in range(m)]
    for j_, i_ in whites:
        checkers_board[j_ - 1][i_ - 1] = 'w'
    for j_, i_ in blacks:
        checkers_board[j_ - 1][i_ - 1] = 'b'
    for j_, i_ in (whites if turn == 'white' else blacks):
        for dj, di in deltas:
            if 0 <= j_ + dj - 1 < m and 0 <= i_ + di - 1 < n:
                if checkers_board[j_ + dj - 1][i_ + di - 1] == ('b' if turn == 'whites' else 'w'):
                    if 0 <= j_ + 2 * dj - 1 < m and 0 <= i_ + 2 * di - 1 < n:
                        if checkers_board[j_ + 2 * dj - 1][i_ + 2 * di - 1] == ' ':
                            return 'Yes'
    return 'No'


def get_pars() -> tuple[int, int, int, int, list[list[int, ...]], list[list[int, ...]], str]:
    n, m = [int(_) for _ in input().split(' ')]
    w = int(input())
    whites = [[int(_) for _ in input().split(' ')] for _ in range(w)]
    b = int(input())
    blacks = [[int(_) for _ in input().split(' ')] for _ in range(b)]
    turn = input()
    return n, m, w, b, whites, blacks, turn


print(f'{cut_down()}')



