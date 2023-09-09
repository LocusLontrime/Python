# accepted on codewars.com
def nth_num_containing_ones(n: int):
    counter_ones = 0
    power = 0
    nums_per_pow = []
    rem = n - 1
    while counter_ones <= n:
        power += 1
        counter_ones = 10 ** (power - 1) + counter_ones * 9
        nums_per_pow.append(counter_ones)
    number = ''
    for pow_ in range(power - 1, 0, -1):
        if rem >= (k := nums_per_pow[:-1][pow_ - 1]):
            rem -= k
            if rem >= (n1 := 10 ** pow_):
                number += f'{2 + (n2 := (rem - n1) // k)}'
                rem -= n1 + n2 * k
                if rem == 0:
                    number += f'0'
            else:
                number += f'1' + f'0' * (pow_ - len(str(rem))) + f'{rem}'
                break
        else:
            number += f'0'
    return int(number) + (1 if '1' not in number and number[-1] == '0' else 0)


n_ = 893668976123456789000001936189779797957467689799191931665999791234567890987654321278999999999999999999999999999999999999999999999999999999999
print(f'nth_num_containing_ones: {nth_num_containing_ones(n_)}')
