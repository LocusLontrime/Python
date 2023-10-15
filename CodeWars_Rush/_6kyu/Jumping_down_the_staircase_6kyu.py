# accepted on codewars.com
def get_number_of_ways(steps: int, max_jump_length: int) -> int:
    memo_table = {}
    return rec_core(steps, max_jump_length, memo_table)


def rec_core(steps_rem: int, max_jump_length: int, memo_table: dict[int, int]) -> int:
    # border case:
    if steps_rem == 0:
        return 1
    if steps_rem not in memo_table.keys():
        res = 0
        for jl in range(1, min(steps_rem, max_jump_length) + 1):
            res += rec_core(steps_rem - jl, max_jump_length, memo_table)
        memo_table[steps_rem] = res
    return memo_table[steps_rem]


a, b = 84, 26
a_, b_ = 3, 3
a_x, b_x = 96, 57
print(f'res: {get_number_of_ways(100, 100)}')

