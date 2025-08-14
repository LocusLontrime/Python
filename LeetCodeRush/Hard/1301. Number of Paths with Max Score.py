# accepted on leetcode.com
MODULO = 10 ** 9 + 7
walk = ((0, -1), (-1, 0), (-1, -1))
MIN_THRESHOLD = -(100 + 100) * 9


def paths_with_max_score(board: list[str]) -> list[int]:
    # linear sizes:
    max_j, max_i = len(board), len(board[0])
    # dp approach:
    dp_memo = [[[MIN_THRESHOLD, 0] for i in range(max_i)] for j in range(max_j)]
    dp_memo[0][0] = [0, 1]
    res = dp(max_j - 1, max_i - 1, board, dp_memo)
    return [0, 0] if res[0] < 0 else res


def dp(j: int, i: int, board: list[str], dp_memo: list[list[list[int]]]) -> list[int]:
    el = board[j][i]
    # body of rec:
    if dp_memo[j][i][0] == MIN_THRESHOLD:
        # left and up movements:
        for dj, di in walk:
            j_, i_ = j + dj, i + di
            # we are within the board's borders:
            if 0 <= j_ and 0 <= i:
                # the next cell is not a wall:
                if board[j_][i_] != "X":
                    val = (0 if el in "S" else int(el))
                    result = dp(j_, i_, board, dp_memo)
                    if result[0] + val > dp_memo[j][i][0]:
                        dp_memo[j][i] = result[0] + val, result[1]
                    elif result[0] + val == dp_memo[j][i][0]:
                        dp_memo[j][i] = result[0] + val, (dp_memo[j][i][1] + result[1]) % MODULO
    return dp_memo[j][i]                                                          # 36 366 98 989 98989 LL LL


test_ex = [
    "E23",
    "2X2",
    "12S"
]

print(f'test ex res -> {paths_with_max_score(test_ex)}')                              # 36 366 98 989 98989 LL LL


