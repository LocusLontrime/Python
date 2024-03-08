# accepted on codewars (on C++)
MAX_CONTROL = 10

counter: int


def solve(input_: list[int]):
    global MAX_CONTROL, counter

    counter = 0

    size: int = len(input_)

    result, evens = size, 0

    nums = [0 for _ in range(100001)]

    def add(j: int):
        # print(f'......add......')
        nonlocal evens
        global counter
        counter += 1
        nums[input_[j]] += 1
        if nums[input_[j]] > 1:
            evens += -1 if nums[input_[j]] % 2 else 1
        return 0 if evens else 1

    def minus(j: int):
        # print(f'......minus......')
        nonlocal evens
        global counter
        counter += 1
        nums[input_[j]] -= 1
        if nums[input_[j]] > 0:
            evens += -1 if nums[input_[j]] % 2 else 1
        return 0 if evens else 1

    print(f"now in cycle...")

    right, left = 0, 0
    iControl = 0
    while iControl < MAX_CONTROL:
        old = result

        print(f'lb, rb: {left, right}')

        if right < size:
            add(right)
            right += 1
        if right < size:
            result += add(right)
            right += 1

        # print(f'...interim1 lb, rb: {left, right}')

        while right < size:
            add_ = add(right)
            right += 1
            minus_ = minus(left)
            left += 1
            result += add_ + minus_

        # print(f'...interim2 lb, rb: {left, right}')

        if left > 0:
            left -= 1
            add(left)
        if left > 0:
            left -= 1
            result += add(left)

        # print(f'...interim3 lb, rb: {left, right}')

        while left > 0:
            left -= 1
            add_ = add(left)
            right -= 1
            minus_ = minus(right)
            result += add_ + minus_

        # print(f'...interim4 lb, rb: {left, right}')

        if old == result:
            iControl += 1
            print("......................................................................................")
        else:
            iControl = 0

    return result


array_ = [2, 2, 2, 3]  # 7
array_1 = [2, 5, 2, 3, 6, 7, 8, 23, 23, 13, 65, 31, 3, 4, 3]  # 53
array_2 = [6, 1, 7, 4, 6, 7, 1, 4, 7, 1, 4, 6, 6, 7, 4, 1, 6, 4, 7, 1, 4, 5, 3, 2, 1, 6, 9]  # 114
array_3 = [1, 3, 1]
array_4 = [2, 1, 1, 1]
array_x = [2 if i % 2 else 1 for i in range(10_000)]  # 10_000 els

array_n_100000 = []  # ans: 8492097 (tests performance, many //####''frequently-repeating numbers)

with open("C:\\Users\\langr\\PycharmProjects\\AmberCode\\CodeWars_Rush\\_2kyu\\to_be_solved\\Numbers.txt") as f:
    for line in f:
        array_n_100000 += [int(x) for x in line.split(', ')]

print(f'res: {solve(array_x)}')

print(f'{counter = }')
