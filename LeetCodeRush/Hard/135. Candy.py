# accepted on leetcode.com

# There are n children standing in a line.Each child is assigned a rating value given in the integer array ratings.

# You are giving candies to these children subjected to the following requirements:

# Each child must have at least one candy.
# Children with a higher rating get more candies than their neighbors.

# Return the minimum number of candies you need to have to distribute the candies to the children.

# Example 1:
# Input: ratings = [1, 0, 2]
# Output: 5
# Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.

# Example 2:
# Input: ratings = [1, 2, 2]
# Output: 4
# Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively.
# The third child gets 1 candy because it satisfies the above two conditions.

# Constraints:
# n == ratings.length
# 1 <= n <= 2 * 10 ** 4
# 0 <= ratings[i] <= 2 * 10 ** 4

import heapq


def candy(ratings: list[int]) -> int:
    heap = []
    heapq.heapify(heap)
    heapq.heappop(heap)
    heapq.heappush()
    # array's length:
    n = len(ratings)
    candies = [1] * n
    # at first, we should make left -> right traversal:
    for i in range(n - 1):
        if ratings[i] < ratings[i + 1]:
            candies[i + 1] = candies[i] + 1
    print(f'{candies = }')
    # secondly, we should make right -> left traversal:
    for i in range(n - 1, 0, -1):
        if ratings[i] < ratings[i - 1]:
            candies[i - 1] = max(candies[i - 1], candies[i] + 1)
    print(f'-> {candies = }')
    # lastly, we return the sum of candies that is also the min sum possible:
    return sum(candies)


test_ex = [100, 80, 70, 60, 70, 80, 90, 100, 90, 80, 70, 60, 60]
test_ex_1 = [6, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 1, 0]
test_ex_2 = [20000, 20000, 16001, 16001, 16002, 16002, 16003, 16003, 16004, 16004, 16005, 16005, 16006, 16006, 16007,
             16007, 16008, 16008, 16009, 16009, 16010, 16010, 16011, 16011, 16012, 16012, 16013, 16013, 16014, 16014,
             16015, 16015, 16016, 16016, 16017, 16017, 16018, 16018, 16019, 16019, 16020, 16020, 16021, 16021, 16022,
             16022, 16023, 16023, 16024, 16024]

print(f'test ex res -> {candy(test_ex)}')                                             # 36 366 98 989 98989 LL
