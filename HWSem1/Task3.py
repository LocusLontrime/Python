 # Сформировать программу, получающую набор произведений чисел от 1 до N. Для N = 4: [1, 2, 6, 24]

def get_factorial_list(length):
    factorials_list = []
    curr_fact = 1
    for i in range(1, length + 1):
        curr_fact *= i
        factorials_list.append(curr_fact)

    return factorials_list


print(get_factorial_list(9))  # an example for 3rd task

