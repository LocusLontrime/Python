import sys

sys.set_int_max_str_digits(1_000_000)
sys.setrecursionlimit(1_000_000)

comb=lambda n,k:((x:=2<<n)+1)**n//x**k%x

# comb=f=lambda n,k:0**k or f(n-1,k-1)*n//k


n, k = 5_000, 2_500

print(f'combs({n, k}) -> {comb(n, k)}')

k_ = 0  # 1

print(f'res: {k_ < 1 and 1}')

# print(f'{(2 ** 1000) ** 1000}')

print(f'{2 >> 1}')
