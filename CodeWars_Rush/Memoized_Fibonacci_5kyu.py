# accepted on codewars.com
memo_table = {0: 0, 1: 1}


def fibonacci(n):

    if n not in memo_table.keys():

        memo_table[n] = fibonacci(n - 1) + fibonacci(n - 2)

    return memo_table[n]


def fib_dp(n):

    fib_prev = 0
    fib_curr = 1

    for i in range(n):

        fib_curr = fib_curr + fib_prev
        fib_prev = fib_curr - fib_prev

    return fib_prev


print(fibonacci(800))
print(fib_dp(1000000))
