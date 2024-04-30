# accepted on codewars.com
def golomb(given, n):
    els_ = []
    temp_n = n
    si = 0
    # 0-case processing:
    if (g1 := next(giter := iter(given))) == 0:
        g2 = next(giter)
        if g2 == 1:
            g3 = next(giter)
            els_ += (addition := [g2, g3, g2, g1] + [g2 for _ in range(g3 - 2)])[: min(temp_n, len(addition))]
            if temp_n <= len(addition):
                return els_
            temp_n -= len(addition)
            si = 3
        else:
            els_ += (addition := [g2, g2] + [g1 for _ in range(g2)] + [g2 for _ in range(g2 - 2)])[: min(temp_n, len(addition))]
            if temp_n <= len(addition):
                return els_
            temp_n -= len(addition)
            si = 2
    # usual part:
    for i, _el in enumerate(giter if si else given, si):                              # 36 366 98 989 98989 LL
        if len(els_) <= i:
            els_ += [_el for _ in range(min(_el, temp_n))]
            if _el >= temp_n:
                break
            temp_n -= _el
        else:
            els_ += [_el for _ in range(min(els_[i], temp_n))]
            if els_[i] >= temp_n:
                break
            temp_n -= els_[i]
    # returns result:
    return els_


class Iterable:
    def __init__(self, fn): self.fn = fn

    def __iter__(self): return self.fn()


iterable = lambda *fns: Iterable(lambda: (reduce(lambda z, fn: lambda v: fn(z(v)), fns)(i) for i in count(0)))

id_ = lambda x: x
plus = lambda v: lambda w: v + w
times = lambda v: lambda w: v * w
exp = lambda v: lambda w: v ** w
triangle = lambda x: x * (x + 1) // 2
square = lambda x: x * x

given_x = iterable(plus(1))
given_e = iterable(exp(2))
given_id = iterable(id_)

given_ = [1, 2, 4, 8, 16]

print(f'res: {golomb(given_id, 9)}')
