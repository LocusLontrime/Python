def min_hamming_str(bin_str1: str, bin_str2: str, length: int) -> str:
    hamming_distance_from_bin_str_1 = 0
    hamming_distance_from_bin_str_2 = 0

    result_bin_str = ''

    for i in range(length):
        if bin_str1[i] != bin_str2:
            if hamming_distance_from_bin_str_1 <= hamming_distance_from_bin_str_2:
                result_bin_str += bin_str1[i]
                hamming_distance_from_bin_str_1 += 1
            else:
                result_bin_str += bin_str2[i]
                hamming_distance_from_bin_str_2 += 1
        else:
            result_bin_str += bin_str1[i]

    return result_bin_str


print(min_hamming_str("01000", "00110", 5))
print(min_hamming_str("00000", "11111", 5))
print(min_hamming_str("00001", "00111", 5))

