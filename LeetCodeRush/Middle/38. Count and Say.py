# accepted on leetcode.com


def count_and_say(n: int) -> str:
    cas = f'1'
    for i in range(n - 1):
        cas = rle(cas)
    return cas


def rle(s: str):  # 998
    i = 0
    # string's length:
    n = len(s)
    # the main cycle:
    res = f''
    while i < n:
        temp_i = i
        while i < n - 1 and s[i] == s[i + 1]:
            i += 1
        res += f'{(i - temp_i + 1)}{s[i]}'
        i += 1
    return res


test_ex = 4

print(f'{count_and_say(4)}')

print(f'{rle("sssrle")}')
