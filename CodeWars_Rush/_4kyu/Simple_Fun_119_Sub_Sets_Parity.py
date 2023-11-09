# accepted on codewars.com


def subsets_parity(n: int, k: int):
    return {0: "ODD", 1: "EVEN"}[bool(k & n - k)]


# print(f'combs: {subsets_parity(5, 2)}')
# print(f'combs: {subsets_parity(6, 2)}')
# print(f'combs: {subsets_parity(7, 3)}')
print(f'combs: {subsets_parity(2, 1)}')
print(f'combs: {subsets_parity(98, 89)}')
print(f'combs: {subsets_parity(62, 30)}')

