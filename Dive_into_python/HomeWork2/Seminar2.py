import decimal
import math

from _decimal import getcontext

DEC = 10


def convert_to_base_of(num: int, base: int) -> int:
    """convert a decimal number to any base system"""
    return 0 if num == 0 else convert_to_base_of(num // base, base) * DEC + num % base


print(f'converted num: {convert_to_base_of(11, 2)}, right res: {bin(11)}')
print(f'converted num: {convert_to_base_of(111, 8)}, right res: {oct(111)}')
# print(f'converted num: {convert_to_base_of(1117, 16)}, right res: {hex(1117)}')

# BAD CODE...
# print(f'hash: {hash([98, 989])}')

getcontext().prec = 43
d = decimal.Decimal(112)
if d > 10000 or d <= 0:
    raise ValueError(f'OOF!!!')
pi = decimal.Decimal(math.pi)

circumference = pi * d
area = circumference * d / 4
print(f'circumference, area: {circumference, area}')

a, b, c = 2, 2, 3
sqrt = (b ** 2 - 4 * a * c) ** 0.5
x1, x2 = (-b + sqrt) / (2 * a), (-b - sqrt) / (2 * a)
print(f'{x1=}, {x2=}')

