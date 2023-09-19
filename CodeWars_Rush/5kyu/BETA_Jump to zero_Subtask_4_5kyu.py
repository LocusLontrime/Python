# accepted on codewars.com
import random
import time

results: dict[int, int] = {}


def sum_dig(n: int) -> int:
    return sum(map(int, str(n)))


def jump_to_zero(arr: list[int]) -> int:
    global results
    ans = [0] * len(arr)
    for i in range(len(arr)):
        queue = []
        while arr[i] > 0:
            if arr[i] in results.keys():
                ans[i] += results[arr[i]]
                break
            queue.append((arr[i], ans[i]))
            ans[i] += 1
            arr[i] -= sum_dig(arr[i])
        for n, r in queue:
            results[n] = ans[i] - r
    return ans


nums = [[random.randint(6_000, 7_000) * 10 ** 3 for k in range(1_000)] for _ in range(1_000)]
start = time.time_ns()
for num in nums:
    res = jump_to_zero(num)
    # rint(f'RES({nums}): {res}')
finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')
# print(f'results: {sorted(results.items(), key=lambda x: x[0])}')
