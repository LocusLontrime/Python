import math
golden_ratio = (1.0 + math.sqrt(5)) / 2
coefficient = 1.0 / (1.0 - math.pow(math.e, - golden_ratio))  # ideal coefficient for comb_sort


def comb_sort(array: list[int]):
    global coefficient

    def swap(i1: int, i2: int):
        array[i1], array[i2] = array[i2], array[i1]

    distance = length = len(array)  # distance between two elements being compared
    permutations_counter = 2  # minimal value higher than 1, auxiliary parameter for while cycle functioning

    while permutations_counter > 1:
        # counter of permutation
        counter = 0
        # bubble optimization step:
        distance = int(distance / coefficient)
        # while distance reaches values less than 1 the algorithm proceed to the second phase ->
        # babble sorting until all the array's elements has been sorted (counter equals zero):
        if distance < 1:
            distance = 1
        for i in range(0, length - distance):
            if array[i] > array[i + distance]:
                swap(i, i + distance)
                counter += 1
        # while swaps in bubble phase happen we stay in cycle, if not -> we should break:
        if distance == 1:
            permutations_counter = counter + 1


arr = [111, 1, 0, 1, 1, 99, -111, -989, -9, 9, 9, 0, 1, 11, 111, 11111, 89, 98, 98, 989, 98]
comb_sort(arr)
print(arr)
