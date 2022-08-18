import math

k = 5.0
m: int = 5  # int float str bool

res: int
res = 98

print(k)
print(res)

print(int('98'))
print(float('989.9898'))

k = 0

if k:
    print('lalala')

# list_of_nums = []
#
# for i in range(0, 10):
#     list_of_nums.append(i)
#
# if list_of_nums:
#     print(len(list_of_nums))
# else:
#     print('dick!')

print('for starts:')
for i in range(100):
    print(i)

list_of_numbers = [1, 3, 6, 7, 9]

print('2nd for starts:')
for el in list_of_numbers:
    print(el)






print('3d for starts:')
for i in range(len(list_of_numbers)):
    print(list_of_numbers[i])


array = []

array.append(1)
array.append(2)

print(array)

static_array = [0] * 10

print(static_array)

static_array[3] = 698

print(static_array)

print(array + static_array)

print('Kostia ' * 100)

new_list = [i for i in [1, 3, 5, 6, 7, 8, 9, 10, 11] if i % 2 == 0 or i % 3 == 0]

print(new_list)

print(sum(new_list))

print(1111111111111111111111111111111111111111111111111111111111111119999999999999999999999999999999999999 ** 2)


def method(x: int) -> int:
    return x ** x


print(method(1001))

ans = []

for i in range(1000000):
    if i % 2 == 0:
        ans.append(i)

# print(ans)

print(math.factorial(1000000))
