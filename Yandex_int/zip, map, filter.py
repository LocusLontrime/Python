matrix1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

matrix2 = [
    [10, 11, 12],
    [13, 14, 15],
    [16, 17, 18]
]

res1 = zip(*matrix1, *matrix2)

for row in res1:
    print(f'{row}')

res2 = filter(lambda x: sum(x) > 15, matrix1)
print(f'res_: {list(res2)}')


res3 = map(lambda x: int(x) ** 2, f'98989')
print(f'res3: {list(res3)}')

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

print(f'{arr[2:6]}')  # [3, 4, 5, 6]
print(f'{arr[1:-3]}')  # [2, 3, 4, 5, 6, 7, 8, 9]
print(f'{arr[-5:-3]}')  # [8, 9]
print(f'{arr[:-3]}')  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
