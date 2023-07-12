# accepted on coderun
import math
from collections import defaultdict as d


minimal_cost: float
best_coupons: list[int]


def min_cost():
    global minimal_cost, best_coupons
    minimal_cost = math.inf
    n, m, k, costs, coupons_available, discounts = get_pars()
    cpr = shape_coupons_products_relation(coupons_available)
    comb_cost(0, 0, k, m, costs, coupons_available, discounts, set(), cpr)
    res = ' '.join([str(_) for _ in best_coupons])
    print(f'{len(best_coupons)}\n{res}')


def shape_coupons_products_relation(coupons_available) -> d[int, set[int]]:
    cpr = d(set)
    for ind_, coupons_ in enumerate(coupons_available):
        for coupon_ in coupons_:
            cpr[coupon_ - 1].add(ind_)
    return cpr


def comb_cost(k_: int, ind_: int, k: int, m: int, costs, coupons_available, discounts, coupons_applied, cpr):
    global minimal_cost, best_coupons
    # base case:
    if k_ == k:
        if (s := sum(costs)) < minimal_cost:
            minimal_cost = s
            best_coupons = coupons_applied
        return
    # body of recursion:
    for m_ in range(ind_, m):
        if m_ + 1 not in coupons_applied:
            for i_ in cpr[m_]:
                costs[i_] *= (100 - discounts[m_]) / 100
            # recurrent relation:
            comb_cost(k_ + 1, m_ + 1, k, m, costs, coupons_available, discounts, coupons_applied | {m_ + 1}, cpr)
            # backtracking:
            for i_ in cpr[m_]:
                costs[i_] *= 100 / (100 - discounts[m_])


def get_pars():
    n, m, k = map(int, input().split())
    costs = [int(_) for _ in input().split()]
    coupons_available = [[int(_) for _ in input().split()][1:] for _ in range(n)]
    discounts = [int(_) for _ in input().split()]
    return n, m, k, costs, coupons_available, discounts


# def dp(ind_: int, m_: int, k_: int, n: int, costs: list[int | float], coupons_available: list[list[int]],
#        discounts: list[int], discounts_used: set[int]) -> float:
#     print(f'k_: {k_}, ind_: {ind_}, m_: {m_}, n: {n}')
#     # border case:
#     if k_ < 0:
#         return math.inf
#     if ind_ == n:
#         print(f'costs: {costs}, sum_: {sum(costs)}, set_: {discounts_used}')
#         return 0
#     if m_ == len(coupons_available[ind_]):
#         print(f'costs[ind_]: {costs[ind_]}')
#         return dp(ind_ + 1, 0, k_, n, costs, coupons_available, discounts, discounts_used) + costs[ind_]
#     # body of recursion:
#     d_ind_ = coupons_available[ind_][m_]
#     d_ = discounts[d_ind_]
#     res = math.inf
#     if d_ind_ + 1 not in discounts_used:
#         costs[ind_] *= (100 - d_) / 100
#         res = dp(ind_, m_ + 1, k_ - 1, n, costs, coupons_available, discounts, discounts_used | {d_ind_ + 1})
#         # backtracking:
#         costs[ind_] *= 100 / (100 - d_)
#     res = min(
#         res,
#         dp(ind_, m_ + 1, k_, n, costs, coupons_available, discounts, discounts_used)
#     )
#     return res
















