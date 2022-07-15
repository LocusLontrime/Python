# accepted on codewars.com
memo_table = {0: 1, 1: 1}


def partitions(n):
    global memo_table

    if n not in memo_table.keys():
        memo_table[n] = 0
        curr_minus = 0
        curr_delta = 0
        i = 1
        while True:
            if i % 2 == 0:
                curr_delta = i // 2
            else:
                curr_delta = i

            i += 1

            curr_minus += curr_delta

            if curr_minus > n:
                break

            if i % 4 in [2, 3]:
                memo_table[n] += partitions(n - curr_minus)

            else:
                memo_table[n] -= partitions(n - curr_minus)

    return memo_table[n]


print(partitions(989))
