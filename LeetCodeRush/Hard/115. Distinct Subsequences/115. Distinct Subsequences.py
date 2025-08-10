# accepted om leetcode.com

# Given strings s and t, return the number of distinct subsequences of s which equals t.

# The test cases are generated so that the answer fits on a 32 - bit signed integer.

# Example 1:
# Input: s = "rabbbit", t = "rabbit"
# Output: 3
# Explanation: As shown below, there are 3 ways you can generate "rabbit" from s.

# rabbbit
# rabbbit
# rabbbit

# Example 2:
# Input: s = "babgbag", t = "bag"
# Output: 5
# Explanation:
# As shown below, there are 5 ways you can generate "bag" from s.

# babgbag
# babgbag
# babgbag
# babgbag
# babgbag

# Constraints:
# 1 <= s.length, t.length <= 1000
# s and t consist of English letters.

def num_distinct(s: str, t: str) -> int:
    # let us use dp:
    memo_table = {}
    return dp(len(s) - 1, len(t) - 1, s, t, memo_table)


def dp(j: int, i: int, s: str, t: str, memo_table: dict) -> int:
    # border cases:
    if i == -1:
        return 1
    if (j, i) not in memo_table.keys():
        memo_table[(j, i)] = 0
        for j_ in range(max(0, i - 1), j + 1):
            if s[j_] == t[i]:
                memo_table[(j, i)] += dp(j_ - 1, i - 1, s, t, memo_table)
    return memo_table[(j, i)]


test_ex = "rabbbit", "rabbit"
test_ex_1 = "babgbag", "bag"
test_ex_2 = "b", "b"

print(f'test ex res -> {num_distinct(*test_ex)}')                                     # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {num_distinct(*test_ex_1)}')
print(f'test ex res -> {num_distinct(*test_ex_2)}')

