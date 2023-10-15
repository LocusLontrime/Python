# accepted on codewars.com
import time  # 36 366 98 989 98989


first_10000_primes = None
primes_set = None
precalculated_min_divs = None
memoized_ant_arrs = None


def prime_ant(n: int):
    global first_10000_primes, primes_set, precalculated_min_divs, memoized_ant_arrs

    if first_10000_primes is None:
        primes_set = get_primes(70000)
        first_10000_primes = list(sorted(primes_set))
        pre_calc_min_divs(70000)
        memoized_ant_arrs = {0: (0, [2])}

    if n in memoized_ant_arrs.keys():
        return memoized_ant_arrs[n]

    print(f'mem: {(b := list(sorted(memoized_ant_arrs.keys(), reverse=True)))}')

    for key in b:
        if key <= n:
            numbers = memoized_ant_arrs[key][1][:]
            steps = key
            ant_curr_pos_ind = memoized_ant_arrs[key][0]
            print(f'steps: {steps}, ant pos: {ant_curr_pos_ind}')
            break

    while steps < n:
        m = numbers[ant_curr_pos_ind]
        if m in primes_set:  # first_10000_primes:
            ant_curr_pos_ind += 1
            if ant_curr_pos_ind >= len(numbers):
                numbers.append(ant_curr_pos_ind + 2)  # for 1th-index it will be 3
        else:
            min_div = precalculated_min_divs[m]
            numbers[ant_curr_pos_ind] //= min_div
            ant_curr_pos_ind -= 1
            numbers[ant_curr_pos_ind] += min_div
        steps += 1

    memoized_ant_arrs[n] = (ant_curr_pos_ind, numbers[:])

    return numbers[:ant_curr_pos_ind + 1]


def pre_calc_min_divs(max_num: int):
    global precalculated_min_divs, primes_set
    precalculated_min_divs = dict()

    for num in range(4, max_num):
        if num not in primes_set:
            precalculated_min_divs[num] = get_min_divisor(num)


def get_min_divisor(number: int):
    global first_10000_primes
    for prime in first_10000_primes:
        if number % prime == 0:
            return prime


# Eratosthenes' sieve
def get_primes(n):
    """
    param n: max number to which we should build the primes list
    return: list of primes before or equal to n
    """
    # filling the list from 0 to n
    a = []
    for i in range(n + 1):
        a.append(i)
    # 1 is a prime number
    a[1] = 0
    # we begin from 3-rd element
    i = 2
    while i <= n:
        # if the cell value has not yet been nullified -> it keeps the prime number
        if a[i] != 0:
            # the first multiple will be two times larger
            j = i + i
            while j <= n:
                # not a prime -> exchange it with 0
                a[j] = 0
                # proceed to the next number (n % i == 0)
                # it has the value that is larger by i
                j = j + i
        i += 1
    # list to set, all nulls except 1 got removed
    a = set(a)
    # here we delete the last null
    a.remove(0)
    return a


start = time.time_ns()
l = prime_ant(2 * 1000000)
# l1 = prime_ant(1925128)
l2 = prime_ant(1343489)
l3 = prime_ant(1425417)
l4 = prime_ant(1105935)

# print(l)
print(f'size: {len(l)}')
end = time.time_ns()

print(f'Time elapsed: {(end - start) // 10 ** 6} milliseconds')


for ind in range(1, 7 + 1):
    print(f'for numbers like: {(k := 10 ** ind)} the primes bound will be: {0.13 * k ** 0.9}')

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
print(arr[:])
print(arr)
