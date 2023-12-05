# accepted on codewars.com
pattern = [1, 10, 9, 12, 3, 4]


def thirt(n: int):
    curr_, prev_ = n, 0
    while curr_ != prev_:
        prev_ = curr_
        digits = list(map(int, str(curr_)[::-1]))
        curr_ = sum(digits[k] * pattern[k % len(pattern)] for k in range(len(digits)))
    return curr_


print(f'res: {thirt(1234567)}')  # 89
print(f'res: {thirt(321)}')  # 48

print(f'{str(1 / 1)}')
