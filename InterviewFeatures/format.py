_70bit = 2 ** 70
print(f'{_70bit = }')


def format_num(num: int, group_len: int, split_ch: str) -> str:
    str_num, num_len = str(num), len(str(num))
    rem = num_len % group_len
    return f"{split_ch.join([el for i in range(-group_len, num_len - rem, group_len) if (el := str_num[max(0, rem + i): rem + i + group_len])])}"


print(format_num(_70bit, 3, ' '))
