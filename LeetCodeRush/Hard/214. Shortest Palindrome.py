# accepted on leetcode.com

# You are given a string s.You can convert s to a palindrome by adding characters in front of it.

# Return the shortest palindrome you can find by performing this transformation.

# Example 1:
# Input: s = "aacecaaa"
# Output: "aaacecaaa"

# Example 2:
# Input: s = "abcd"
# Output: "dcbabcd"

# Constraints:
# 0 <= s.length <= 5 * 104
# s consists of lowercase English letters only.

MODULO = 10 ** 9 + 7  # the big prime chosen to exclude collisions...
BASE = 26  # depends on the power of the alphabet used, in the English alphabet there are only 26 letters...
ORD_a = 97


def shortest_palindrome(s: str) -> str:
    print(f'{s = }')
    # str's length:
    n = len(s)
    # let us use the rolling hash technic:
    powers = [1] * (n // 2 + 1)
    for i in range(n // 2):
        powers[i + 1] = (powers[i] * BASE) % MODULO
    # n should be >= 2
    if n < 2:
        return s
    rlh1, rlh2 = ord(s[0]) - ORD_a, ord(s[1]) - ORD_a
    print(f'{rlh1 = }')
    print(f'{rlh2 = }')
    # now we should move to the left by 1 element:
    core_length = 2
    shortest_pal_core_length = 2 if rlh1 == rlh2 else 1
    while core_length < n:
        print(f'{core_length = }')
        print(f'before -> {rlh1, rlh2 = }')
        if core_length % 2 == 0:
            # we should leave slw1 the same and slw2 -> slw2[1:] + [el]:
            rlh1 = rlh1
            # slw2[1:]
            rlh2 = (rlh2 - powers[core_length // 2 - 1] * (ord(s[core_length // 2]) - ORD_a)) % MODULO
            # slw[1:] + [el]
            rlh2 = (rlh2 * BASE + (ord(s[core_length]) - ORD_a)) % MODULO
        else:
            # we should slw1 -> slw1 + [el] and slw2 -> slw2 + [el]:
            rlh1 = (rlh1 + powers[core_length // 2] * (ord(s[core_length // 2]) - ORD_a)) % MODULO
            rlh2 = (rlh2 * BASE + (ord(s[core_length]) - ORD_a)) % MODULO
        print(f'after -> {rlh1, rlh2 = }')
        # step up:
        core_length += 1
        # rolling hashes equality check:
        if rlh1 == rlh2:
            shortest_pal_core_length = core_length
    print(f'{shortest_pal_core_length = }')
    shortest_pal = (
            s[shortest_pal_core_length // 2 + 1:][::-1] +
            s[shortest_pal_core_length // 2] +
            s[shortest_pal_core_length // 2 + 1:]
    ) if shortest_pal_core_length % 2 else (
            s[shortest_pal_core_length // 2:][::-1] +
            s[shortest_pal_core_length // 2:]
    )
    return shortest_pal


test_ex = "abcdcba"
test_ex_1 = "aacecaaa"
print(f'{shortest_palindrome(test_ex)}')
print(f'{shortest_palindrome(test_ex_1)}')

print(f'{ord("a")}')
