# accepted on codewars.com
import heapq
import math


def survivor(coins):
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
                return _el - coins[0] - 1 if _el - coins[0] else _el - coins[0]
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
