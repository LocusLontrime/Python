from abc import ABC, abstractmethod
from datetime import datetime


class EnterData(ABC):
    def _input_int(self, min_variant: int, max_variant: int):
        num: int
        try:
            num = int(input(f'Enter a number in range: {[min_variant, max_variant]}'))
        except ValueError:
            return ValueError(f'This is not a number...')
        except Exception:
            return Exception(f'Something is wrong!')
        if not (min_variant <= num <= max_variant):
            raise Exception(f'You entered an invalid value')
        return num

    def _input_str(self):
        string: str
        try:
            string = input(f'Enter a string: ')
        except Exception:
            return Exception(f'Something is wrong!')
        if not string:
            raise Exception(f'You entered an empty string')
        return string

    def _input_date(self):
        string: str
        date: datetime
        try:
            string = input(f'Enter a string: ')
        except Exception:
            return Exception(f'Something is wrong!')
        if not string:
            raise Exception(f'You entered an empty string')
        try:
            date = datetime.strptime(string, '%Y-%m-%d')
        except ValueError:
            return ValueError(f'You must enter a date!')
        return date



