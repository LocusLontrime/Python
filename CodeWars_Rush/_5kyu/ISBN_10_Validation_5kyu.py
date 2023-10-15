# accepted on codewars.com
MODULO = 11


def valid_ISBN10(isbn: str) -> bool:
    digits = ''.join([str(_) for _ in range(9 + 1)])
    symbol = 'X'

    if len(isbn) != 10:
        return False

    for i, ch in enumerate(isbn):
        if ch not in (digits + (symbol if i == len(isbn) - 1 else '')):
            return False

    if sum([(int(ch) if ch != symbol else 10) * i for i, ch in enumerate(isbn, 1)]) % MODULO != 0:
        return False

    return True




