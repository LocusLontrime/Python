import heapq as hq

l = [1, 2, 3, 6, 98]

hq.heapify(l)

l.pop()
l.pop()
l.pop()
l.pop()
l.pop()

print(f'l: {l}')

l.pop()
