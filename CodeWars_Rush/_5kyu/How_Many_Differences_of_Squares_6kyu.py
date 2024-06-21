# accepted on codewars.com
def count_squareable(n: int) -> int:
    print(f'{n = }')
    return n - (int(1 <= n) + int(6 <= n) + max(0, n - 6) // 4)


print(f'res: {count_squareable(4)}')
print(f'res: {count_squareable(5)}')
print(f'res: {count_squareable(40)}')
print(f'res: {count_squareable(20)}')
print(f'res: {count_squareable(10)}')

