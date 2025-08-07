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
            stack += [(i_, h)]
    # we need to proceed the heights remained:
    for i, h in stack:
        max_rectangle_area = max(max_rectangle_area, (n - i) * h)
    # returns res:
    return max_rectangle_area  # 36 366 98 989 98989 LL


test_ex = [2, 1, 5, 6, 2, 3]

print(f'test ex res -> {largest_rectangle_area(test_ex)}')                            # 36 366 98 989 98989

