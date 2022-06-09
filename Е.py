import math
from itertools import combinations_with_replacement as combinations


def genP(n):
    return n*(3*n-1)//2


def isP(n):
    return ((math.sqrt(24*n+1)+1)/2).is_integer()


def is_D_number(a,b):
    return isP(a+b) and isP(abs(a-b)) and a!=b




MAX_NUM = 100

list1 = [genP(i) for i in range(1,MAX_NUM)]


print('=======================================')
list2 = set(abs(a - b) for a, b in combinations(list1, 2) if is_D_number(a,b))

print(list(list2))
print(min(list2))
