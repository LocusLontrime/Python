n_str, m_str = f'87', f'100'

len_disp = min(len(n_str), len(m_str))

n = int(n_str)
m = int(m_str)

if n > m:
    n, m = m, n

i = 0

for h in range(n):
    pal_ = f'{h:0{len_disp}}'[::-1]
    print(f'num: {h}, pal_: {pal_}')
    if int(pal_) < m:
        i += 1

print(i)


def i_am_brute(n: int, m: int):  # time palindromes easy version
    min_, max_ = min(n - 1, m - 1), max(n - 1, m - 1)
    counter_pals, power_of_ten, l_ = 0, 10, 1
    for num in range(min_ + 1):
        if num == power_of_ten:
            power_of_ten *= 10
            l_ += 1
        pal_ = str(num)[::-1] + '0' * (len(str(max_)) - l_)
        print(f'pal_: {pal_}')
        if int(pal_) <= max_:
            counter_pals += 1
    return counter_pals


print(f'{i_am_brute(int(n_str), int(m_str))}')

