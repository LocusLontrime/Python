# accepted on codewars.com
dig_repr_dict = {str(digit) : digit for digit in range(10)}
dig_repr_dict_inv = {digit : str(digit) for digit in range(10)}

def sum_strings(x, y): # 98
    j, i = 0, 0
    while j < len(x) and x[j] == '0': j += 1
    while i < len(y) and y[i] == '0': i += 1
    x_, y_, temporal = x[j:], y[i:], 0
    x_, y_  = (y_, x_) if len(y_) > len(x_) else (x_, y_)
    sum_of_x_and_y = ''
    for i in range(len(x_)):
        ind = dig_repr_dict[x_[len(x_) - i - 1]] + (dig_repr_dict[y_[len(y_) - i - 1]] if len(y_) - i - 1 >= 0 else 0) + temporal
        digit, temporal = dig_repr_dict_inv[ind % 10], 1 if ind > 9 else 0
        sum_of_x_and_y += str(digit)
    if temporal > 0: sum_of_x_and_y += '1'
    return sum_of_x_and_y[::-1] if sum_of_x_and_y != '' else '0'


