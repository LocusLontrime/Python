# accepted on codewars.com
reach_one=s=__import__('functools').lru_cache(lambda k:0if k<=1else min(k%2+s(k//2),k%3+s(k//3))+1)


def reach_one_fast(k: int):
    if k <= 1:
        return 0

    return min(k % 2 + reach_one_fast(k // 2), k % 3 + reach_one_fast(k // 3)) + 1


# print(reach_one_fast(10 ** 90 - 1))
print(reach_one(47))
print(reach_one(48))
print(reach_one(49))
print(reach_one(50))
print(reach_one(32))
print(reach_one(33))
print(reach_one(556))
print(reach_one(10 ** 150))
print(len("reach_one=s=__import__('functools').lru_cache(lambda k:0if k<=1else min(k%2+s(k//2),k%3+s(k//3))+1)"))  # 99 symbols

# print(reach_one(47))
# print(reach_one(32))
