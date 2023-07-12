# accepted on coderun
weekdays = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}


def do_format():
    n, day = get_pars()
    rec_painter(1, 1, 1, n, day)  # 1, 1 indexation


def rec_painter(y_: int, x_: int, day_: int, days: int, day: int):
    # base cases
    if day_ == days + 1:
        return
    if y_ == 1 and x_ < day:
        print(f'.. ', end='')
        rec_painter(y_, x_ + 1, day_, days, day)
        return
    if x_ == 7:
        print_day(day_, '\n')
        rec_painter(y_ + 1, 1, day_ + 1, days, day)
        return
    print_day(day_, ' ')
    rec_painter(y_, x_ + 1, day_ + 1, days, day)


# .. .. .1 .2 .3 .4 .5
# .6 .7 .8 .9 10 11 12
# 13 14 15 16 17 18 19


def print_day(day_: int, end_symb: str = ''):
    res = (f'.{day_}' if day_ < 10 else f'{day_}') + end_symb
    print(res, end='')


def get_pars():
    n, day = input().split()
    return int(n), weekdays[day]


do_format()



