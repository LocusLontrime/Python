# accepted on codewars.com
import heapq as hq
from collections import defaultdict as d


def consecutive_nums(lst: list[int], k: int) -> bool:
    # border case:
    gq, rem = divmod(len(lst), k)  # groups' quantity:
    if rem != 0:
        return False
    # dictionary:
    occurrences = d(int)
    for el in lst:
        occurrences[el] += 1
    # heapifying:
    els = list(occurrences.items())
    hq.heapify(els)
    # main cycle:
    for j in range(gq):
        temp_list = []
        s_ = 0
        el: int
        for i in range(k):
            if not els:
                return False
            el, q = hq.heappop(els)
            s_ += el
            if q > 1:
                temp_list.append((el, q - 1))
        if s_ != consecutive_sum(el, k):
            return False
        for el, q in temp_list:
            hq.heappush(els, (el, q))
    return True


def consecutive_sum(n: int, k: int):
    return (n * (n + 1) - (n - k) * (n - k + 1)) // 2


arr = [1, 2, 3, 4, 5]  # [1, 2, 3, 6, 2, 3, 4, 7, 8]
k_ = 4  # 3
print(f'consecutive_nums: {consecutive_nums(arr, k_)}')







