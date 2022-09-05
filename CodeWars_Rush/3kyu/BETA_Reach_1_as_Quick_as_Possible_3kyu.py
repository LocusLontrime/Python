reach_one = lambda k: 0 if k == 1 else reach_one(k // 3) + 1 if k % 3 == 0 else reach_one(k // 2) + 1 if k % 2 == 0 else reach_one(k - 1) + 1

print(reach_one(100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000))
print(reach_one(50))
print(reach_one(45))
print(reach_one(47))
