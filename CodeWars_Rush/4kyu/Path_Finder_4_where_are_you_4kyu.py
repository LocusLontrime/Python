# accepted on codewars.com
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
direction, j, i = 0, 0, 0


def i_am_here(path):
    global direction, j, i
    ind = 0
    while ind < (l := len(path)):
        match path[ind]:
            case 'R':
                direction += 1 + 1
                ind += 1
            case 'L':
                direction -= 1 + 1
                ind += 1
            case 'r':
                direction += 1
                ind += 1
            case 'l':
                direction -= 1
                ind += 1
        num = ''
        while ind < l and (d := path[ind]).isdigit():
            ind += 1
            num += d
            print(f'num: {num}')
        if num != '':
            j += directions[direction % 4][0] * int(num)
            i += directions[direction % 4][1] * int(num)
            print(f'({j, i})')
    print(f'current dir: {directions[direction]}')
    return [j, i]


p = ['', 'RLrl', 'r5L2l4']

print(i_am_here(p[0]))
print(i_am_here(p[1]))
print(i_am_here(p[2]))

