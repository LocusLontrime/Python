import math


def is_prime(number):
    """
    checks a number for simplicity
    :param number: integer value, should be larger than 1 and less than 100_000
    :return: boolean value (is the number prime or not)
    >>> is_prime(314)
    False
    >>> is_prime(7)
    True
    >>> is_prime(3.14)
    Traceback (most recent call last):
    ...
    TypeError: the number value should be of an integer type
    >>> is_prime(1)
    Traceback (most recent call last):
    ...
    ValueError: 0 and 1 are not prime numbers...
    >>> is_prime(-100)
    Traceback (most recent call last):
    ...
    ValueError: the number is negative or too large (>100000)
    >>> is_prime(100_000_007)
    Traceback (most recent call last):
    ...
    ValueError: the number is negative or too large (>100000)
    """

    if not isinstance(number, int):
        raise TypeError(f'the number value should be of an integer type')
    elif number < 0 or number > 100_000:
        raise ValueError(f'the number is negative or too large (>100000)')
    # base cases:
    elif number in [0, 1]:
        raise ValueError(f'0 and 1 are not prime numbers...')
    # main cycle-check:
    for i in range(2, int(math.sqrt(number))):
        if number % i == 0:
            return False
    return True


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

