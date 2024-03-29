def longest_1s_vector(vector: list[int]) -> tuple[int, int]:
    lp = rp = 0
    max_len = 0
    ji = None

    while rp < len(vector):
        if vector[rp] == 1:
            if (ml := rp - lp + 1) > max_len:
                max_len = ml
                ji = lp, rp
            rp += 1
        else:
            lp = rp + 1
            rp = lp

    return ji if ji is not None else 'no seq'


bv = [1]
bv2 = [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1]
bin_vector = [0, 0, 0]

print(f'longest vector of 1s: {longest_1s_vector(bin_vector)}')
