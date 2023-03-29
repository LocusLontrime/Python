import datetime

__all__ = ['date_check', 'terminal_run']


def terminal_run():
    user_date = input(f'Please, enter a date')
    print(f'res: {date_check(user_date)}')


def date_check(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, '%Y.%m.%d')
        return True
    except Exception as e:
        return False


def leap_year_check(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


if __name__ == '__main__':
    # print(f'{date_check("2018.06.29")}')
    # print(f'{date_check("2018.06.29s")}')

    terminal_run()


