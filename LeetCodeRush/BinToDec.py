def bin_to_dec(bin_num: int) -> int:

    dec_num = 0
    powered_2 = 1

    while bin_num:

        if bin_num % 10:
            dec_num += powered_2

        powered_2 <<= 1
        bin_num //= 10

    return dec_num


def dec_to_bin(dec_num: int) -> int:
    return dec_num % 2 + 10 * dec_to_bin(dec_num // 2) if dec_num else 0


print(f'dec({10001001}): {bin_to_dec(10001001)}')

print(f'bin({137}): {dec_to_bin(137)}')
