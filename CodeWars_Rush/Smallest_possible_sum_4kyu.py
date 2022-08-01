# accepted on codewars.com
def solution(a):
    # smallest possible sum of all numbers in Array
    length = len(a)
    elements = set(a)

    # cycling through the elements
    while len(elements) != 1:
        max_element = max(elements)
        elements.remove(max_element)
        elements.add(max_element - max(elements))

    # all elements are now the same
    return elements.pop() * length


print(solution([6, 9, 21]))

