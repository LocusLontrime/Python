import math
import logging


FORMAT = '%(asctime)s %(name)s - %(lineno)s line(s) - %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, filename='logs.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# function to be logged:
def is_prime(number):
    if not isinstance(number, int):
        logging.error(f'invalid type: {type(number)}, not of an integer type...')
        raise TypeError(f'the number value should be of an integer type')
    elif number < 0 or number > 100_000:
        logging.error(f'the number {number} is out of range: [{2}, {100_000}]')
        raise ValueError(f'the number is negative or too large (>100000)')
    # base cases:
    elif number in [0, 1]:
        logging.error(f'{0} and {1} are nor primes!')
        raise ValueError(f'0 and 1 are not prime numbers...')
    # main cycle-check:
    for i in range(2, int(math.sqrt(number))):
        if number % i == 0:
            logging.info(f'{number} is compound')
            return False
    logging.info(f'{number} is prime')
    return True


# test:
for i_ in [-1, 0, 1, 2, 3.14, 7, 314, 100_000, 100_000_007]:
    try:
        is_prime(i_)
    except TypeError:
        ...
    except ValueError:
        ...
    finally:
        ...
