# accepted on codewars.com
def solve(arr):
    min_, max_ = min(arr), max(arr)
    pre_max = max([n for n in arr if n != max_])
    if arr.index(min_) == 0 and arr.index(max_) == 1:
        return "RD"
    if arr.index(min_) == 1 and arr.index(max_) == 0:
        return "RA"
    return ("A" if arr.index(min_) == 0 else "RA") if arr.index(max_) > arr.index(pre_max) else ("D" if arr.index(max_) == 0 else "RD")




