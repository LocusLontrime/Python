# accepted on codewars.com
memo_table = {0: 1, 1: 1}


# using Euler's method of finding partitions number: https://en.wikipedia.org/wiki/Partition_(number_theory)
def partitions(n):
    global memo_table  # memoization

    if n not in memo_table.keys():
        memo_table[n] = 0
        curr_minus = 0  # used in recurrent relation
        curr_delta = 0  # at first 2*k - 1 deltas, then k deltas. k from 0 to max possible.
        i = 1  # steps counter
        while True:
            if i % 2 == 0:
                curr_delta = i // 2
            else:
                curr_delta = i

            i += 1
            curr_minus += curr_delta

            if curr_minus > n:  # break condition
                break

            # recurrent relation in cycle
            if i % 4 in [2, 3]:  # condition of sign change
                memo_table[n] += partitions(n - curr_minus)
            else:
                memo_table[n] -= partitions(n - curr_minus)

    return memo_table[n]


print(partitions(989))
