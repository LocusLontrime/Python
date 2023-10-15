# accepted on codewars.com
def mystery(num):
    print(f'num: {num}')
    if num == 0:
        return 0
    # calculating the number of bits in n:
    bits, bits_num = get_bits(num)

    def recursive_seeker(n, m):
        if n < 1 or m > (rightmost_val := 2 ** n - 1):
            return -1
        elif n == 1:
            return ['0', '1'][m]
        else:
            if m <= rightmost_val // 2:
                return '0' + recursive_seeker(n - 1, m)
            else:
                return '1' + recursive_seeker(n - 1, rightmost_val - m)

    val = recursive_seeker(bits_num, num)
    return int(val, 2)


def mystery_inv(num):
    # calculating the number of bits in n:
    bits, bits_num = get_bits(num)

    ans = 0
    counter = 0
    for i in range(len(bits) - 1, -1, -1):
        if bits[i] == '1':
            counter += 1
            delta = 2 ** (i + 1) - 1
            ans += (delta if counter % 2 == 1 else -delta)

    return ans


# aux method:
def get_bits(num):
    bits_num = 0
    bits, k = '', num
    while k > 0:
        bits += str(k % 2)
        k //= 2
        bits_num += 1
    return bits, bits_num


def name_of_mystery():
    return 'Gray code'


print(mystery(19))  # 26
print(mystery(9))  # 13
print(mystery(6))  # 5

print(f'inv:')
print(mystery_inv(26))  # 19
print(mystery_inv(13))  # 9
print(mystery_inv(5))  # 6
print(mystery_inv(0))



