# accepted on leetcode.com


def shortest_common_supersequence(str1: str, str2: str) -> str:
    # strings' lengths:
    n1, n2 = len(str1), len(str2)
    # let us use the same dp technic as we would use in lcs task:
    memo_table = {}
    length = dp(n1 - 1, n2 - 1, str1, str2, memo_table)
    # path recovering:
    node = n1 - 1, n2 - 1
    res = f''
    while True:
        _, node, letter = memo_table[node]
        res = letter + res
        if node[0] == -1:
            res = str2[: node[1] + 1] + res
            break
        elif node[1] == -1:
            res = str1[: node[0] + 1] + res
            break
    return res


def dp(i1: int, i2: int, str1: str, str2: str, memo_table: dict) -> int:
    # base case:
    if i1 == -1:
        return i2 + 1
    if i2 == -1:
        return i1 + 1
    # body of rec:
    if (i1, i2) not in memo_table.keys():
        letter = str1[i1]
        if str1[i1] == str2[i2]:
            res = dp(i1 - 1, i2 - 1, str1, str2, memo_table)
            node_ = i1 - 1, i2 - 1
        else:                                                                     # 36 366 98 989 98989 LL LL
            res = dp(i1 - 1, i2, str1, str2, memo_table)
            node_ = i1 - 1, i2
            if (r := dp(i1, i2 - 1, str1, str2, memo_table)) < res:
                res = r
                node_ = i1, i2 - 1
                letter = str2[i2]
        memo_table[(i1, i2)] = res + 1, node_, letter
    return memo_table[(i1, i2)][0]


test_ex = "abac", "cab"
test_ex_1 = "aaaaaaaa", "aaaaaaaa"

print(f'test ex res -> {shortest_common_supersequence(*test_ex)}')                                   # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {shortest_common_supersequence(*test_ex_1)}')

