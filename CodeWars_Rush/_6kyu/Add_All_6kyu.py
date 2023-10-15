# accepted on codewars.com
import heapq as hq


def add_all(lst: list[int]):
    hq.heapify(lst)
    res = 0
    while len(lst) > 1:
        a = hq.heappop(lst)
        b = hq.heappop(lst)
        res += a + b
        hq.heappush(lst, a + b)
    return res


arr_ = [1, 2, 3, 4, 5]
print(f'add_all({arr_}): {add_all(arr_)}')
