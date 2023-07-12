# accepted on coderun
import sys


def search():
    t = int(sys.stdin.readline())
    res = []
    for i in range(t):
        res.append(str(dp()))
    sys.stdout.write("\n".join(res) + "\n")


def dp():
    # parsing:
    n, k, array = get_pars()

    ans = max(array)
    if ans <= 0:
        return ans

    # building dp arrays:
    dyn_prog_left = [[0 for _ in range(k + 2)] for _ in range(n + 2)]
    dyn_prog_right = [[0 for _ in range(k + 2)] for _ in range(n + 2)]

    # dynamic programming phases:
    for i in range(1, n + 1):
        for j in range(k + 1):
            dyn_prog_left[i][j] = max(0, dyn_prog_left[i - 1][j] + array[i - 1])
            if j:
                dyn_prog_left[i][j] = max(dyn_prog_left[i][j], dyn_prog_left[i - 1][j - 1])
            ans = max(ans, dyn_prog_left[i][j])

    for i in range(1, n + 1):
        for j in range(k + 1):
            dyn_prog_left[i][j] = dyn_prog_left[i - 1][j] + array[i - 1]
            if j:
                dyn_prog_left[i][j] = max(dyn_prog_left[i][j], dyn_prog_left[i - 1][j - 1])

    for i in range(n, 0, -1):
        for j in range(k + 1):
            dyn_prog_right[i][j] = dyn_prog_right[i + 1][j] + array[i - 1]
            if j:
                dyn_prog_right[i][j] = max(dyn_prog_right[i][j], dyn_prog_right[i + 1][j - 1])

    for i in range(1, n + 1):
        for j in range(k + 1):
            if i != 1:
                dyn_prog_left[i][j] = max(dyn_prog_left[i][j], dyn_prog_left[i - 1][j])
            if j:
                dyn_prog_left[i][j] = max(dyn_prog_left[i][j], dyn_prog_left[i][j - 1])

    for i in range(n, 0, -1):
        for j in range(k + 1):
            if i != n:
                dyn_prog_right[i][j] = max(dyn_prog_right[i][j], dyn_prog_right[i + 1][j])
            if j:
                dyn_prog_right[i][j] = max(dyn_prog_right[i][j], dyn_prog_right[i][j - 1])

    for i in range(1, n):
        for j in range(k + 1):
            ans = max(ans, dyn_prog_left[i][j] + dyn_prog_right[i + 1][k - j])

    return ans


def get_pars():
    n, k = map(int, sys.stdin.readline().split())
    array = list(map(int, sys.stdin.readline().split()))
    return n, k, array

