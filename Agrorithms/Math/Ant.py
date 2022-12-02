import time


def prime_ant(n):
    def eratosthenes(el):
        el = int(el ** 0.745) + 2
        sieve = list(range(el))
        sieve_length = len(sieve)
        sieve[1] = 0
        for i in sieve:
            if i > 1:
                for j in range(i + i, sieve_length, i):
                    sieve[j] = 0
        sieve1 = [x for x in set(sieve) if x != 0]
        return set(sieve1)

    def smallest_divisor(num):
        if num % 2 == 0:
            return 2
        else:
            for i in range(3, int(num ** 0.5) + 1, 2):
                if num % i == 0:
                    return i

    primes = eratosthenes(n + 1)
    numbers = [el for el in range(2, int(n ** 0.75) + 3)]
    position = 0
    memo = dict()

    for move in range(n):
        if numbers[position] in primes:
            position += 1
        else:
            if memo.get(numbers[position]):
                q = memo[numbers[position]]
            else:
                q = smallest_divisor(numbers[position])
                memo[numbers[position]] = q
            numbers[position] = int(numbers[position] / q)
            numbers[position - 1] = numbers[position - 1] + q
            position -= 1

    return numbers[:position + 1]


start = time.time_ns()
print(l := prime_ant(1000000))
print(f'size: {len(l)}')
end = time.time_ns()

print(f'Time elapsed: {(end - start) // 10 ** 6} milliseconds')

