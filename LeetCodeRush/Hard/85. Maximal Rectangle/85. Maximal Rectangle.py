def maximal_rectangle(matrix: list[list[str]]) -> int:
    # linear sizes of matrix given:
    max_j, max_i = len(matrix), len(matrix[0])
    # let us build an array 'heights' and then seek for largest rectangle in histogram:
    heights = [0 for _ in range(max_i)]
    # the core algo:
    max_rectangle_area = 0
    for row in matrix:
        # heights change:
        for i, el in enumerate(row):
            if el == "1":
                heights[i] += 1
            else:
                heights[i] = 0
        # largest rectangle seeking:
        max_rectangle_area = max(max_rectangle_area, largest_rectangle_area(heights))
    # returns res:
    return max_rectangle_area


def largest_rectangle_area(heights: list[int]) -> int:
    # length of heights:
    n = len(heights)
    # let us use stack:
    max_rectangle_area = 0
    stack = []
    for i, h in enumerate(heights):
        # we should pop out all the heights that are less than h from stack:
        i_ = i
        while stack and stack[-1][1] > h:
            _i, _h = stack.pop()
            i_ = min(i_, _i)
            max_rectangle_area = max(max_rectangle_area, (i - _i) * _h)
        if not stack or stack[-1][1] != h:
            stack += [(i_, h)]                                                        # 36 366 98 989 98989
    # we need to proceed the heights remained:
    for i, h in stack:
        max_rectangle_area = max(max_rectangle_area, (n - i) * h)
    # returns res:
    return max_rectangle_area


test_ex = [
    ["1", "0", "1", "0", "0"],
    ["1", "0", "1", "1", "1"],
    ["1", "1", "1", "1", "1"],
    ["1", "0", "0", "1", "0"]
]

test_ex_2 = [
    ["1", "1"]
]

test_ex_3 = [
    ["0", "0", "1", "0"],
    ["0", "0", "1", "0"],
    ["0", "0", "1", "0"],
    ["0", "0", "1", "1"],
    ["0", "1", "1", "1"],
    ["0", "1", "1", "1"],
    ["1", "1", "1", "1"]
]

print(f'test ex res -> {maximal_rectangle(test_ex)}')                                 # 36 366 98 989 98989 LL
print(f'test ex 2 res -> {maximal_rectangle(test_ex_2)}')
print(f'test ex 3 res -> {maximal_rectangle(test_ex_3)}')
