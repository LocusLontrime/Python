# -*- coding: utf-8 -*-


# 1. Напишите функцию для транспонирования матрицы

# let us assume, that we have a numerical matrix:
def transpose(matrix_: list[list[int]]) -> list[list[int]]:
    return [[matrix_[y][x] for y in range(len(matrix_))] for x in range(len(matrix_[0]))]


# a simple printing method for a matrix:
def show(matrix_: list[list[int]]) -> None:
    for row in matrix_:
        print(f'{row}')


# test:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [9, 9, 9]
]


print(f'matrix: ')
show(matrix)

print(f'matrix transposed: ')
show(transpose(matrix))





