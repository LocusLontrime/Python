from array import array

f_set = frozenset({'lala', 'fafa'})
bytes_ = bytes([1, 2, 98])  # immutable
bytearray_ = bytearray([1, 2, 98])  # mutable

# bytes_[0] = 98
bytearray_[0] = 98

print(f'{f_set = }')

for i, el in enumerate(f_set):
    print(f'{i}th {el = }')

arr_ = array('i', [1, 2, 98])
print(f'{arr_ = }')
print(f'{arr_.buffer_info() = }')
arr_.extend([98, 989, 98989])
print(f'{arr_ = }')
arr_.append(98)
print(f'{arr_ = }')
print(f'{98 in arr_ = }')
