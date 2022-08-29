# accepted on codewars.com
catalan_numbers = {0: 1}


def balanced_parens(n, k):
    # wrong case
    if k < 0:
        return None

    # dynamic programming memo dictionary
    dp = [[0] * (n + 1) for _ in range(0, 2 * n + 1)]
    dp[0][0] = 1

    # building memo table
    for i in range(0, n * 2):
        for j in range(0, n + 1):
            if j + 1 <= n:
                # print(f'first, i: {i}, j: {j}')
                dp[i + 1][j + 1] += dp[i][j]
            if j > 0:
                # print(f'second, i: {i}, j: {j}')
                dp[i + 1][j - 1] += dp[i][j]

    result = ''

    if k > dp[n * 2][0]:
        return None

    # depth of nested parenthesis
    depth_of_nested = 0

    # constructing the result parenthesis
    for i in range(n * 2 - 1, -1, -1):
        if depth_of_nested + 1 <= n and dp[i][depth_of_nested + 1] >= k:
            result += '('
            depth_of_nested += 1
        else:
            result += ')'
            if depth_of_nested + 1 <= n:
                k -= dp[i][depth_of_nested + 1]
                depth_of_nested -= 1

    return result


print(balanced_parens(10, 3502))


# auxiliary methods for clearing what is happening
def find_pars(n, k):
    for i in range(0, n):
        delta = catalan_numbers[i] * catalan_numbers[n - i - 1]
        if k - delta < 0:
            return i, n - i - 1,
        k -= delta


def catalans_num(k: int) -> dict[int, int]:
    for i in range(1, k + 1):
        catalan_numbers[i] = 2 * (2 * i - 1) * catalan_numbers[i - 1] // (i + 1)
    return catalan_numbers
