# accepted on coderun
import datetime
import sys
from collections import defaultdict as d


categories = {'KGT': 0, 'COLD': 1, 'OTHER': 2}


class Interval:
    def __init__(self, date_start: datetime.date, date_finish: datetime.date):
        self.start = date_start
        self.finish = date_finish

    def __lt__(self, other):
        return (self.start, self.finish) < (other.start, other.finish)

    # string representation:
    def __str__(self):
        return f'{self.start} {self.finish}'

    def __repr__(self):
        return str(self)


def validate_csv():
    csv = get_pars()
    # fields parsing:
    csv = [_.split(',') for _ in csv]
    products: d[str: list[Interval]] = d(list)
    for id_, date_interval_, category_ in csv:
        interval_ = Interval(*date_interval_.split())
        if category_ == 'NULL':
            for sub_category_ in categories.keys():
                products[(id_, sub_category_)].append(interval_)
        else:
            products[(id_, category_)].append(interval_)
    sorted_keys = sorted(products.keys(), key=lambda x: (x[0], categories[x[1]]))
    for ind_, sorted_key in enumerate(sorted_keys):
        joined_intervals = join_intervals(sorted(products[sorted_key]))
        for interval_ in joined_intervals:
            print(f'{sorted_key[0]},{interval_},{sorted_key[1]}')


def get_pars():
    lines = []
    while (r := input()) != '':
        lines.append(r)
    return lines


def join_intervals(intervals: list[Interval]) -> list[Interval]:
    joined_intervals = []
    left, right = intervals[0].start, intervals[0].finish
    ind_ = 1
    counter = 0
    while True:
        counter += 1
        # joining:
        while ind_ < len(intervals) and (interval := intervals[ind_]).start <= right:
            right = max(right, interval.finish)
            ind_ += 1
        # adding new joined interval to the res:
        joined_intervals.append(Interval(left, right))
        # a step to the right:
        if ind_ >= len(intervals):
            break
        # left border updating:
        left = intervals[ind_].start
        right = intervals[ind_].finish
    return joined_intervals


# intervals check:
intervals_ = [
    Interval(datetime.date.fromisoformat(f'2022-02-15'), datetime.date.fromisoformat(f'2022-02-18')),
    Interval(datetime.date.fromisoformat(f'2022-02-02'), datetime.date.fromisoformat(f'2022-02-05')),
    Interval(datetime.date.fromisoformat(f'2022-02-09'), datetime.date.fromisoformat(f'2022-02-13')),
    Interval(datetime.date.fromisoformat(f'2022-02-07'), datetime.date.fromisoformat(f'2022-02-11')),
    Interval(datetime.date.fromisoformat(f'2022-02-02'), datetime.date.fromisoformat(f'2022-02-04')),
    Interval(datetime.date.fromisoformat(f'2022-02-03'), datetime.date.fromisoformat(f'2022-02-12')),
    Interval(datetime.date.fromisoformat(f'2022-11-03'), datetime.date.fromisoformat(f'2023-02-12')),
    Interval(datetime.date.fromisoformat(f'2023-02-01'), datetime.date.fromisoformat(f'2023-11-03')),
    Interval(datetime.date.fromisoformat(f'2020-09-03'), datetime.date.fromisoformat(f'2020-10-03')),
    Interval(datetime.date.fromisoformat(f'2020-10-18'), datetime.date.fromisoformat(f'2021-08-22'))
]
print(f'joined intervals: {join_intervals(intervals_)}')


validate_csv()




