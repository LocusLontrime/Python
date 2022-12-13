# accepted on codewars.com
results = None


def power_sum_dig_term(n: int) -> list[int]:
    # n-th term of the sequence, each term is a power of the sum of its digits
    if results is None:
        get_list()
    return results[n - 1]


def get_list():
    global results
    results = []
    boundary_num = 500
    boundary_length = 100
    candidates = [(x, x ** y) for x in range(2, boundary_num + 1) for y in range(2, boundary_num + 1) if
                  x ** y < 10 ** (boundary_length + 1)]
    for candidate in candidates:
        if digits_sum(candidate[1]) == candidate[0]:
            results.append(candidate[1])
    # print(f'candidates: {candidates}')
    results = list(sorted(results))
    print(f'length of results: {len(results)}')


def digits_sum(number: int, dig_sum=0) -> int:
    return digits_sum(number // 10, number % 10 + dig_sum)if number > 0 else dig_sum


print(f'power_sum_dig_term: {power_sum_dig_term(5)}')  # 5832
print(f'digits_sum: {digits_sum(112345)}')
