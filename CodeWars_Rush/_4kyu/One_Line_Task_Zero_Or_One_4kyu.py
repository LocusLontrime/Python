import functools
import operator

# zero_or_one=lambda n,s: [1 if sum([sj[i] for sj in s])>=len(s[0])//2 else 0 for i in range(len(s[0]))]
zero_or_one=lambda n,s:[sum(k)>n/2for k in zip(*s)]

n_, s_ = 5, [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1]
]

n__, s__ = 3, [
    [1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0]
]

print(f'res: {zero_or_one(n__, s__)}')
print(f'length: {len("zero_or_one=lambda n,s:[sorted(k)[n//2]for k in zip(*s)]")}')
# a = [1, 0, 0, 1, 1, 1, 0, 1, 1]
# print(f'{...}')
#
# # xor = [a[i]^a[i+1]for i in range(len(a)-1)]
# # print(f'xor of a: {xor}')
#
# res = functools.reduce(operator.xor, a)
# print(f'res: {res}')

