# approx value
THRESHOLD = 100000


def find(n):

    initial_array = [0, 1, 2, 2]

    # base cases
    if n <= 3:
        return initial_array[n]

    array_sum = 5
    array_len = 4

    for i in range(3, n+1):

        array_sum += i * initial_array[i]

        if array_sum >= n:
            x = (array_sum - n) // i
            return array_len + initial_array[i] - (x+1)

        array_len += initial_array[i]

        # sequence members needed
        if array_len < THRESHOLD:
            initial_array += [i] * initial_array[i]


print(find(98))
