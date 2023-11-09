# n1840 from leetcode.com
# accepted on leetcode.com (faster than 53%)


def max_height_building(n: int, restrictions: list[list[int]]):
    # sorts buildings restrictions by the second val:
    restrictions.sort()
    # adds the leftmost restriction of zero height:
    if restrictions[0] != [1, 0]:
        restrictions = [[1, 0]] + restrictions
    # traverse from left to right:
    length = len(restrictions)
    for i in range(length - 1):
        if abs(restrictions[i + 1][1] - restrictions[i][1]) > restrictions[i + 1][0] - restrictions[i][0]:
            restrictions[i + 1][1] = min(restrictions[i + 1][1], restrictions[i][1] + restrictions[i + 1][0] - restrictions[i][0])
    # traverse from right to left:
    for i in range(length - 1, 0, -1):
        if abs(restrictions[i - 1][1] - restrictions[i][1]) > restrictions[i][0] - restrictions[i - 1][0]:
            restrictions[i - 1][1] = min(restrictions[i - 1][1], restrictions[i][1] + restrictions[i][0] - restrictions[i - 1][0])
    # defining the max height possible:
    max_height = n - restrictions[-1][0] + restrictions[-1][1]
    for i in range(length - 1):
        max_height = max(max_height, (restrictions[i + 1][1] + restrictions[i][1] + restrictions[i + 1][0] - restrictions[i][0]) // 2)
    return max_height


n_ = 10
restrictions_ = [[5, 3], [2, 5], [7, 4], [10, 3]]

print(f'max height: {max_height_building(n_, restrictions_)}')

