import math
import unittest


def is_prime(number) -> bool:
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


class TestFunc(unittest.TestCase):
    def test_is_prime(self):
        self.assertEqual(is_prime(7), True)  # 'Prime number'
        self.assertEqual(is_prime(314), False)  # 'Compound number'
        self.assertEqual(is_prime(2), True)  # 'Prime number'

    def test_type(self):
        self.assertRaises(TypeError, is_prime, 3.14)
        self.assertRaises(TypeError, is_prime, '3.14')

    def test_value(self):
        with self.assertRaises(ValueError):
            is_prime(1)
            is_prime(-100)
            is_prime(100_000_007)


if __name__ == '__main__':
    unittest.main()





