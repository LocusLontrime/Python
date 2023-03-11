extended_digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def convert_to_base_of(num: int, base: int) -> str:
    """convert a decimal number to any base system"""
    return '' if num == 0 else convert_to_base_of(num // base, base) + extended_digits[num % base]


print(f'converted num: {convert_to_base_of(11, 2)}, right res: {bin(11)}')
print(f'converted num: {convert_to_base_of(111, 8)}, right res: {oct(111)}')
print(f'converted num: {convert_to_base_of(1117, 16)}, right res: {hex(1117)}')
print(f'converted num: {convert_to_base_of(111797, 32)}')
