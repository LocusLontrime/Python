# accepted on codewars.com
def calc_special(trailing_digit, base):
    digit, aux = trailing_digit, 0
    parasitic_one = get_based_dig(trailing_digit)
    while True:
        curr_multiplication = digit * trailing_digit + aux
        digit = curr_multiplication % base
        aux = curr_multiplication // base
        parasitic_one = get_based_dig(digit) + parasitic_one
        if digit == 1 and aux == 0:
            break
    return parasitic_one


def get_based_dig(digit: int) -> str:
    return str(digit) if digit < 10 else chr(int(ord('A') + digit - 10))


print(chr(ord('A') + 10))
print(f'calc: {calc_special(3, 36)}')

