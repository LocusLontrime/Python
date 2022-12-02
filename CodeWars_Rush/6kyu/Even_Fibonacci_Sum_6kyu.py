# accepted on codewars.com
def even_fib(m):
    # initial data:
    prev_fib, curr_fib = 0, 1
    # cycle for calculating sum
    sum_of_even_fibs = 0
    while prev_fib < m:
        print(f'current fib: {prev_fib}')
        if prev_fib % 2 == 0:
            sum_of_even_fibs += prev_fib
        prev_fib, curr_fib = curr_fib, prev_fib + curr_fib
    return sum_of_even_fibs


MARKUSHA_THRESHOLD = 50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ** 30
print(MARKUSHA_THRESHOLD)
# print(even_fib(MARKUSHA_THRESHOLD))
print(even_fib(1000000))






