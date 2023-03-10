# Найти НОК двух чисел

def gcd(a: int, b: int):  # Euclidian algo of finding the greatest common divisor
    minimum = min(a, b)
    maximum = max(a, b)
    while True:
        rem = maximum % minimum
        # print(f'max = {maximum}, min = {minimum}') -->> aux
        if rem == 0:
            return minimum
        maximum = max(rem, minimum)
        minimum = min(rem, minimum)


def lcm(a: int, b: int):  # least common multiple
    return a * b // gcd(a, b)


print(gcd(33, 55))
print(gcd(3, 5))
print(gcd(45, 15))

print(lcm(33, 55))
print(lcm(3, 5))
print(lcm(45, 15))

# print(lcm("", ""))

