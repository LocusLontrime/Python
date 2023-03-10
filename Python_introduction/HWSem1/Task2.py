# Пользователь вводит две строки, определить количество вхождений одной строки s2 в другую s1

def count_overlapping_substrings(s1, s2):
    counter = 0
    i = -1
    while True:
        i = s1.find(s2, i + 1)
        if i == -1:
            return counter
        counter += 1


print(count_overlapping_substrings('avarnikabcdefabcdefabc', 'abcdefabc'))  # an example for 1st task

print('avarnikabcdefabcdefabc'.count('abcdefabc'))
