from math import ceil


def some_sequence2(local_list):
    L = 0
    P = []
    M = [0 for _ in range(len(local_list)+1)]
    for i in range(0,len(local_list)):
        hi = L
        while lo <= hi: 
            mid = ceil((lo+hi)/2)
            if local_list[M[mid]] < local_list[i]:
                lo = mid + 1
            else:
                hi = mid - 1
        newL = lo

        P.append(M[newL - 1])
        M[newL] = i
        if newL > L:
            L = newL

    S = []
    k = M[L]
    for _ in range(L, 0,-1):
        S.append(local_list[k])
        k = P[k]
    S.reverse()
    return S


print(some_sequence2([9, 8, 7, 8, 9, 10, 1, 1, 1, 1, 1, 5, 2, 1, 3, 4, 6, 1, 2, 2, 7, 98, 1, 2, 99]))
