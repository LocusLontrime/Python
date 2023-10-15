# accepted on codewars.com
constants = [60, 60, 24, 365]
names = ['second', 'minute', 'hour', 'day', 'year']


def format_duration(seconds):
    if seconds == 0:
        return 'now'

    answer = []
    for iteration in range(0, len(constants)):
        rem = seconds % constants[iteration]
        seconds //= constants[iteration]
        if rem > 0:
            answer.append(f"{str(rem)} {names[iteration]}{'s' if rem > 1 else ''}")
    if seconds > 0:
        answer.append(f"{str(seconds)} {names[len(names) - 1]}{('s' if seconds > 1 else '')}")

    readable_str = ''
    j = len(answer)

    if j > 2:
        for i in range(len(answer) - 1, -1, -1):
            if i > 1:
                readable_str += f'{answer[i]}, '
            elif i == 1:
                readable_str += f'{answer[i]} and '
            else:
                readable_str += f'{answer[i]}'
    elif j == 2:
        readable_str += f'{answer[1]} and {answer[0]}'
    elif j == 1:
        readable_str += f'{answer[0]}'

    return readable_str


print(format_duration(3602))
print(format_duration(3662))

print(format_duration(60 * 60 * 24 * 365 + 1))
