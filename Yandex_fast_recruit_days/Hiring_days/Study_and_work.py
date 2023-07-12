def find_last_day(x: int, k: int, times: list[int]) -> int:
    # sorts the starting days of lectures:
    times_sorted = sorted(set(times))
    length = len(times_sorted)
    print(f'times sorted: {times_sorted}')
    left_border_ = 0
    index_ = 0
    lectures_begun_already = dict()
    days_on_lectures_gone = 0
    step = 0
    # core cycle:
    while True:
        right_border_ = left_border_ + x - 1
        print(f'{step}th STEP.................................................')
        print(f'lb, rb: {(left_border_, right_border_)}')
        while index_ < length and (el := times_sorted[index_]) <= right_border_:
            if (el_ := el % x) not in lectures_begun_already.keys():
                print(f'{el} added...')
                lectures_begun_already[el_] = step, el
            index_ += 1
        print(f'lectures begun already: {lectures_begun_already}')
        # k check:
        if days_on_lectures_gone + len(lectures_begun_already) >= k:
            elements_q = k - days_on_lectures_gone
            print(f'elements_q: {elements_q}')
            key = sorted(lectures_begun_already.keys())[elements_q - 1]
            print(f'key: {key}')
            return lectures_begun_already[key][1] + (step - lectures_begun_already[key][0]) * x
        days_on_lectures_gone += len(lectures_begun_already)
        left_border_ += x
        step += 1
        print(f'days on lectures gone: {days_on_lectures_gone}')


print(f'day: {find_last_day(7, 12, [5, 22, 17, 13, 8])}')
print(f'day: {find_last_day(5, 10, [1, 2, 3, 4, 5, 6])}')








