import heapq
import time
import math


# TODO: implement """Round Robin by Bocker & Liptak"""!!!
def min_price(coins):
    coins = list(sorted(coins))
    print(f'{coins}')
    gcd = math.gcd(*coins)
    print(f'gcd: {gcd}')
    if gcd != 1:
        return -1
    visited = set()
    queue = [0]
    heapq.heapify(queue)
    counter = 0
    prev = 0
    i = 0
    while queue:
        _el = heapq.heappop(queue)
        if _el == prev + 1:
            counter += 1
            if counter == coins[0]:
                print(f'{i + 1} iters made...')
                return _el - coins[0]
        else:
            counter = 0
        # print(f'{i}th iteration -> el: {_el}')
        for coin_ in coins:
            if (el_ := _el + coin_) not in visited:
                heapq.heappush(queue, el_)
                visited.add(el_)
        # time.sleep(0.25)
        i += 1
        prev = _el


# needs to think hard about it
start = time.time_ns()
res = min_price([453, 637, 94, 704, 253, 917, 35, 125, 747])  # 3, 5 | 7430, 9881, 12667 | 54663, 70427, 78958, 17924, 50796, 97105, 82858 | 922, 736, 602, 706, 652
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
print(f'res: {res}')

# 453, 637, 94, 704, 253, 917, 35, 125, 747

