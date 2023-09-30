import math


def split_rect(a: int, b: int, k: int, m: int) -> tuple[int, int] or int:
    d = k ** 2 - 4 * (m - k - 1)
    # print(f'd: {d}')
    if d < 0 or int(math.sqrt(d)) ** 2 != d:
        return -1
    hs = (k - int(math.sqrt(d))) // 2
    vs = k - hs
    if 0 <= hs < a and 0 <= vs < b:
        return hs, vs
    hs = (k + int(math.sqrt(d))) // 2
    vs = k - hs
    return (hs, vs) if 0 <= hs < a and 0 <= vs < b else -1


a_, b_, k_, m_ = 3, 5, 5, 12  # 1, 2, 2, 3  # 2, 2, 1, 2
print(f'split rect: {split_rect(a_, b_, k_, m_)}')

