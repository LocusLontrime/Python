# Task n3 from leetcode.com
# accepted on leetcode.com
def longest_substring_length(s: str):
    sliding_symbols = set()
    li, ri = 0, 0
    longest_substring_l = 0
    longest_substring = ''
    while ri < len(s):
        if s[ri] not in sliding_symbols:
            sliding_symbols.add(s[ri])
            ri += 1
            if ri - li > longest_substring_l:
                longest_substring_l = ri - li
                longest_substring = f'{sliding_symbols}'
        else:
            sliding_symbols.remove(s[li])
            li += 1
    print(f'longest_substring: {longest_substring}')
    return longest_substring_l


print(f'longest_substring_l: {longest_substring_length(f"pwwkew")}')



