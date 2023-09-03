def longest_unique_chars_substring(string: str):
    lp, rp = 0, 0
    sau = set()
    seq_ = ''
    res: str
    max_length = 0
    # two-pointers core:
    while lp < len(string):
        if rp < len(string):
            sau.add(el := string[rp])
            if (l_ := len(sau)) == rp - lp + 1:
                seq_ += el
                if l_ > max_length:
                    max_length = l_
                    res = seq_
                rp += 1
                continue
        # indices reboot:
        lp += 1
        rp = lp
        sau = set()
        seq_ = ''
    return res


arr_ = 'abcabcbbddeevbndiiryhnfmskiiuuwhdjfjk'

print(f'res: {longest_unique_chars_substring(arr_)}')

