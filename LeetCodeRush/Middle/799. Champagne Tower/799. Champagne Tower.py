# accepted on leetcode.com

# We stack glasses in a pyramid, where the first row has 1 glass, the second row has 2 glasses,
# and so on until the 100th row.  Each glass holds one cup of champagne.

# Then, some champagne is poured into the first glass at the top.  When the topmost glass is full,
# any excess liquid poured will fall equally to the glass immediately to the left and right of it.
# When those glasses become full, any excess champagne will fall equally to the left and right of those glasses, and so on.
# (A glass at the bottom row has its excess champagne fall on the floor.)

# For example, after one cup of champagne is poured, the top most glass is full.
# After two cups of champagne are poured, the two glasses on the second row are half full.
# After three cups of champagne are poured, those two cups become full - there are 3 full glasses total now.
# After four cups of champagne are poured, the third row has the middle glass half full,
# and the two outside glasses are a quarter full, as pictured below.

# Now after pouring some non-negative integer cups of champagne, return how full the jth glass in the ith row is (both i and j are 0-indexed.)


def champagne_tower(poured: int, query_row: int, query_glass: int) -> float:
    # memoization:
    dp = {(0, 0): poured}  # liters of champagne that have been poured in the every glass
    # beginning of recursion:
    v = rec_core(query_row, query_glass, dp)
    # returning the result:
    return v if v < 1 else 1


def rec_core(j: int, i: int, dp: dict):
    # border case:
    if not (0 <= i <= j):
        return 0
    # body of rec:
    if (j, i) not in dp.keys():
        dp[(j, i)] = excess_volume(rec_core(j - 1, i, dp)) / 2 + excess_volume(rec_core(j - 1, i - 1, dp)) / 2  # if exists
    return dp[(j, i)]


def excess_volume(v: float) -> float:
    return v - 1 if v > 1 else 0


test_ex = 7, 3, 2
test_ex_1 = 1, 1, 1
test_ex_2 = 2, 1, 1
test_ex_3 = 100000009, 33, 17

print(f'res[{test_ex}] -> {champagne_tower(*test_ex)}')                               # 36 366 98 989 98989 LL
print(f'res[{test_ex_1}] -> {champagne_tower(*test_ex_1)}')
print(f'res[{test_ex_2}] -> {champagne_tower(*test_ex_2)}')
print(f'res[{test_ex_3}] -> {champagne_tower(*test_ex_3)}')


