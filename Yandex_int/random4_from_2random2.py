import random
from collections import defaultdict as d


results = d(int)
for i in range(1_000_000):
    if (k := random.randint(1, 2)) == 1:
        r = random.randint(1, 2)
    else:
        r = 2 + random.randint(1, 2)
    results[r] += 1
    # print(f'{i}. {k}')
print(f'results: {results}')
