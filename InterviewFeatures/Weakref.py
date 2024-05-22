import weakref


class A:
    pass


def callback(ref):
    pass


a = A()
b = weakref.ref(a)
c = weakref.ref(a, callback)
print(f'{c is b, b is a.__weakref__}')
print(f'{weakref.getweakrefs(a)}')

# a = [...]
# b = ()

# print(f'{a} | {b}')

a = [1, 2, 3, 4, 5]
a.append(a)
a.append(98)

print(f'{a = }')
print(f'{a[5]}')


