from collections import defaultdict as d


def is_anagram(s: str, t: str) -> bool:
    # building dicts:
    d1, d2 = d(int), d(int)
    for ch in s:
        d1[ch] += 1
    for ch in t:
        d2[ch] += 1
    # comparison of two dicts:
    return d1 == d2


s_ = "anagram"
t_ = "nagaram"

print(f'res: {is_anagram(s_, t_)}')
