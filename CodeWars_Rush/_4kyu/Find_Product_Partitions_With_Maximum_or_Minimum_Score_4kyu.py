# accepted on codewars.com
import math
from collections import defaultdict as d, Counter
from math import sqrt

m_score: int
best_product_permut: list[int] = []
rec_counter: int


def find_spec_prod_part(n: int, com: str):
    global m_score, rec_counter
    rec_counter = 0
    is_max = com == 'max'
    m_score = 98 if is_max else math.inf
    # your code here
    # prod_partition as a list, or return "It is a prime number"
    product_partitions = []
    factors = {2: 2, 3: 3, 5: 1}
    prime_factors = factorize(n)
    # print(f'prime_factors: {prime_factors}')
    rec_seeker(1, 1, 0, sum(prime_factors.values()), n, [1, 1], prime_factors, product_partitions, is_max)
    print(f'product_partitions: {product_partitions}')
    print(f'size: {len(product_partitions)}')
    # print(f'pp data: {[best_product_permut, m_score]}')
    return [best_product_permut[1:][::-1], m_score]


def factorize(n: int) -> d[int, int]:
    temp = n
    prime_factors = d(int)
    for i in range(2, int(sqrt(n)) + 1):
        while temp % i == 0:
            temp = temp // i
            prime_factors[i] += 1
            # print(i)
        if temp == 1:
            break
    if temp > 1:
        prime_factors[temp] += 1
    return prime_factors


def rec_seeker(i: int, pre_key: int, counter: int, max_counter: int, n: int, product_partition: list[int],
               factors: d[int, int], product_partitions, is_max: bool):
    global m_score, best_product_permut, rec_counter
    rec_counter += 1
    # base case:
    # print(f'i, counter: {i, counter}, product_partition: {product_partition}')
    if counter >= max_counter and product_partition[i] >= product_partition[i - 1] and product_partition[1] != n:
        product_partitions.append(pp := product_partition[::1])
        if is_max:
            if (score_ := get_scores(product_partition)) > m_score:
                m_score = score_
                best_product_permut = pp
        else:
            if (score_ := get_scores(product_partition)) < m_score:
                m_score = score_
                best_product_permut = pp
        return
    # body of rec:
    if product_partition[i] > 1 and product_partition[i] >= product_partition[i - 1]:
        rec_seeker(i + 1, 1, counter, max_counter, n, product_partition + [1], factors, product_partitions, is_max)
    for key, val in factors.items():
        if key >= pre_key and val > 0:
            factors[key] -= 1
            product_partition[i] *= key
            rec_seeker(i, key, counter + 1, max_counter, n, product_partition, factors, product_partitions, is_max)
            # backtracking:
            product_partition[i] //= key
            factors[key] += 1


def get_scores(permut: list[int]) -> int:
    c = Counter(permut)
    return sum(k ** v for k, v in c.items() if k != 1) * (len(permut) - 1)


# print(list(permutations([2, 2, 3, 3, 3, 5], r=3)))  # prime: 9674579

k_ = 2 ** 5 * 3 ** 3 * 5 * 7  # * 13 * 17
print(f'k: {k_}')
print(f'res: {find_spec_prod_part(k_, f"max")}')
print(f'rec_counter: {rec_counter}')

