# accepted on codewars.com
import operator


def compute_ranges(arr: list[int], op, rs: list[list[int]]):
    results = []
    tree = [0 for _ in range(4 * len(arr))]
    build(tree, arr, op, 1, 0, len(arr) - 1)
    for r in rs:
        results.append(op_in_range(tree, op, 1, 0, len(arr) - 1, r[0], r[1] - 1))
    return results


def build(tree, arr, op, v, tl, tr):
    if tl == tr:
        tree[v] = arr[tl]
    else:
        tm = (tl + tr) // 2
        build(tree, arr, op, v * 2, tl, tm)
        build(tree, arr, op, v * 2 + 1, tm + 1, tr)
        tree[v] = op(tree[v * 2], tree[v * 2 + 1])


def op_in_range(tree, op, v, tl, tr, l_, r):
    if l_ > r:
        return None
    if l_ == tl and r == tr:
        return tree[v]
    tm = (tl + tr) // 2
    left, right = op_in_range(tree, op, v * 2, tl, tm, l_, min(r, tm)), op_in_range(tree, op, v * 2 + 1, tm + 1, tr, max(l_, tm + 1), r)
    if left and right:
        return op(left, right)
    if left:
        return left
    return right


arr_ = [1, 4, 7, 2, 9, 1, 98]
ranges = [[1, 2], [1, 6], [2, 5]]

print(f'res: {compute_ranges(arr_, operator.add, ranges)}')
