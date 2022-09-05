rec_seeker_counter: int
memo_table: list[int]
symbols: list[str]


def get_fastest_seq(goal: int) -> int:
    global rec_seeker_counter, memo_table, symbols
    rec_seeker_counter = 0
    memo_table = [-1] * goal
    symbols = [''] * goal

    def rec_seeker(prev_value: int, aim: int):
        global rec_seeker_counter
        rec_seeker_counter += 1

        if prev_value == aim:
            print(f'counter: {rec_seeker_counter}')
            return 0
        elif prev_value > aim:
            return 1000000001

        if memo_table[prev_value] == -1:
            if (l := rec_seeker(prev_value * 3, aim)) < (r := rec_seeker(prev_value + 2, aim)):
                memo_table[prev_value] = l + 1
                symbols[prev_value] = '*3'
            else:
                memo_table[prev_value] = r + 1
                symbols[prev_value] = '+2'

        return memo_table[prev_value]
    return rec_seeker(1, goal)


def get_sequence():
    seq = '1'
    index = 1
    length = len(memo_table)
    while index < length:
        seq += (char := symbols[index])
        if char == '*3':
            index *= 3
        elif char == '+2':
            index += 2

    return seq


print(get_fastest_seq(3667))
print(get_sequence())
