# accepted on codewars.com
def last_digit(array: list[int]):
    curr_value = 1
    for i in range(len(array) - 1, -1, -1):
        curr_value = array[i] ** (curr_value if curr_value < 4 else curr_value % 4 + 4)
    return curr_value % 10


print(f'{last_digit([13, 30, 21])}')
