# accepted on coderun
import heapq as hq


def process_queries():
    n, m, q, strings_parsed = get_pars()
    bitmask = [0 for _ in range(n)]
    servers_on = [m for _ in range(n)]
    resets_q = [0 for _ in range(n)]
    metric = [0 for _ in range(n)]
    # heaps:
    max_heap = [(0, _) for _ in range(n)]
    min_heap = [(0, _) for _ in range(n)]
    # main cycle:
    for string_parsed in strings_parsed:
        print(f'{string_parsed}')
        match string_parsed[0]:
            case 'RESET':
                _, i = string_parsed
                i = int(i)
                bitmask[i - 1] = 0
                servers_on[i - 1] = m
                resets_q[i - 1] += 1
                metric[i - 1] = m * resets_q[i - 1]
                # adding to the heaps:
                ra = resets_q[i - 1] * m
                hq.heappush(max_heap, (-ra, i - 1))
                hq.heappush(min_heap, (ra, i - 1))
            case 'DISABLE':
                _, i, j = string_parsed
                i, j = int(i), int(j)
                # now disabling j_th server on i_th data_center:
                bit = 1 << (j - 1)
                print(f'bit_ : {bit}')
                q = bitmask[i - 1] & bit
                print(f'q: {q}')
                if q == 0:
                    bitmask[i - 1] |= bit
                    print(f'bitmask_: {bitmask[i - 1]}')
                    servers_on[i - 1] -= 1
                    # adding to the heaps:
                    ra = resets_q[i - 1] * servers_on[i - 1]
                    metric[i - 1] = ra
                    hq.heappush(max_heap, (-ra, i - 1))
                    hq.heappush(min_heap, (ra, i - 1))
            case 'GETMAX':
                # let us pop out the data centers unchanged from the max heap:
                while -max_heap[0][0] != metric[max_heap[0][1]]:
                    hq.heappop(max_heap)
                print(f'max_heap: {max_heap}')
                print(f'{max_heap[0][1] + 1}')
            case 'GETMIN':
                while min_heap[0][0] != metric[min_heap[0][1]]:
                    hq.heappop(min_heap)
                # let us pop out the data centers unchanged from the max heap:
                print(f'min_heap: {min_heap}')
                print(f'{min_heap[0][1] + 1}')
            case _:
                print('FAFA')
    print(f'bitmasks: {bitmask}')


def get_pars():
    n, m, q = [int(_) for _ in input().split()]
    strings_parsed = [input().split() for _ in range(q)]
    return n, m, q, strings_parsed


process_queries()



















