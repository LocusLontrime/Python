import datetime


def count_spec_things():
    counter_of_spec_things = 0

    for years in range(1901, 2000 + 1):
        for months in range(1, 12 + 1):
            date = datetime.date(years, months, 1)
            if date.weekday() == 6:
                counter_of_spec_things += 1

    return counter_of_spec_things


print(count_spec_things())
