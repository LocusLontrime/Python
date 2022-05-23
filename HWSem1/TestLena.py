num = int(input())
sum = 0
while num > 0:
    sum += num % 10
    num //= 10
print(f'sum = {sum}')
s = 0
for i in range(0, 10):
    s += 10
print(s)
a1 = int(input())
a2 = int(input())
a3 = int(input())
a4 = int(input())
if a1 == a2 or a1 == a3 or a1 == a4 or a2 == a3 or a2 == a4 or a3 == a4:
    print('there is a pair with equal integers')
else:
    print('no such pair exists')


def get_lena(str):
    if str == "Konung of the darkness":
        return "Villain Queen"
    elif str == "2d tyan":
        return "Fuck you, miserable slave!.."
    else:
        return "I am fucking, you are shmulling!!!"


print("Gorshok " + get_lena("2d tyan"))

print("Konung " + get_lena("Konung of the darkness"))
