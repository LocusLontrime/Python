# accepted on leetcode.com

# You are given an array of k linked - lists lists, each linked - list is sorted in ascending order.

# Merge all the linked - lists into one sorted linked - list and  return it.

# Example 1:
# Input: lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
# Output: [1, 1, 2, 3, 4, 4, 5, 6]
# Explanation: The linked - lists are:
# [
#     1->4->5,
#     1->3->4,
#     2->6
# ]
# merging them into one sorted linked list:
# 1->1->2->3->4->4->5->6

# Example 2:
# Input: lists = []
# Output: []

# Example 3:
# Input: lists = [[]]
# Output: []

# Constraints:
# k == lists.length
# 0 <= k <= 104
# 0 <= lists[i].length <= 500
# -104 <= lists[i][j] <= 104
# lists[i] is sorted in ascending order.
# The sum of lists[i].length will not exceed 10 ** 4.

# Definition for singly-linked list.
import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_lists(lists: list[ListNode] | None) -> ListNode | None:
    # Linked Lists quantity:
    n = len(lists)
    values = []
    heapq.heapify(values)
    indices = [0 for _ in range(n)]
    for i in range(n):
        if lists[i] is not None:
            heapq.heappush(values, (lists[i].val, i))
            lists[i] = lists[i].next
    # result linked list:
    res = None
    curr_node = None
    while values:
        # min el:
        min_val, min_i = heapq.heappop(values)
        if res is None:
            res = ListNode(min_val)
            curr_node = res                                                           # 36 366 98 989 98989 LL
        else:
            curr_node.next = ListNode(min_val)
            curr_node = curr_node.next
        if lists[min_i] is not None:
            heapq.heappush(values, (lists[min_i].val, min_i))
            lists[min_i] = lists[min_i].next
    return res





























































