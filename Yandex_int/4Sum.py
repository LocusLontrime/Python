# n18 from leetcode.com
# accepted on leetcode.com (beats 88% runtime)
from collections import defaultdict as d


def _4sum(arr: list[int], target: int):
    arr_corrected = []
    aux_dict = d(int)
    for el in arr:
        if aux_dict[el] < 4:
            aux_dict[el] += 1
            arr_corrected.append(el)
    print(f'arr_corrected: {arr_corrected}')
    sums_: d[int, list[tuple[int, int]]] = d(list)
    res = set()
    for j in range(len(arr_corrected)):
        for i in range(j + 1, len(arr_corrected)):
            sums_[arr_corrected[j] + arr_corrected[i]].append((j, i))
    for sum_, _indices in sums_.items():
        if target - sum_ in sums_.keys():
            indices_ = sums_[target - sum_]
            for _j, _i in _indices:
                for j_, i_ in indices_:
                    if min(j_, i_) > max(_j, _i):
                        if len({_j, _i}.intersection({j_, i_})) == 0:
                            new_one = tuple(
                                sorted((arr_corrected[_j], arr_corrected[_i], arr_corrected[j_], arr_corrected[i_])))
                            res.add(new_one)
    return res


arr_ = [1, 0, -1, 0, -2, 2]
arr_x = [2, 2, 2, 2, 2]
print(f'4sum: {_4sum(arr_, 0)}')
print(f'4sum: {_4sum(arr_x, 8)}')
