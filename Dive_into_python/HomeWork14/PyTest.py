import math

import pytest


# function to be tested:
def is_prime(number):
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


def test_is_prime():
    assert not is_prime(314), 'this number is not a prime!'
    assert is_prime(7), 'the number is prime!'


def test_type():
    with pytest.raises(TypeError):
        is_prime(3.14)


def test_one():
    with pytest.raises(ValueError):
        is_prime(1)


def test_too_low():
    with pytest.raises(ValueError):
        is_prime(-100)


def test_too_large():
    with pytest.raises(ValueError):
        is_prime(100_000_007)


if __name__ == '__main__':
    pytest.main()



