a = 123  # Инициализация переменных динамическим образом
b = 123.123
c = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
s = 'Elen""""a'
ss = "Mister ''''Rus"

print(a)
print(b)
print(c)
print(s)
print(ss)

print(a, b, c, s, ss)

print(f'{a} - {b} - {c} - {s} - {ss}')  # Форматирование строки

print("Enter two value:")

f1 = int(input())
f2 = input()

print(f'the first number gained: {f1} and the second one: {f2}')
print(f'type of 1st number: {type(f1)} and type of 2nd one: {type(f2)}')

elements = [1, 2, 3, 4, 5]

print(f'elements: {elements}')

for element in elements:
    print(element, end=' ')

print()

for i in range(0, 10):
    print(i, end=' ')
