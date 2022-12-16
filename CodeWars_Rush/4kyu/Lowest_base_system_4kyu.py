def get_min_base(number):
    print(f'number: {number}')
    for base in range(2, number):
        if base % 10 ** 6 == 0:
            print(f'base: {base}')
        rem = number
        while rem > 1 and (rem - 1) % base == 0:
            rem = (rem - 1) // base
        if rem == 1:
            return base


print(get_min_base(1001001))
print(get_min_base(35507849176589241353065885))
print(get_min_base(667709331509987365499916))

