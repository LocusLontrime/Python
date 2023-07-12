# accepted on coderun


def max_profit() -> int:
    sellers, buyers = get_pars()
    sellers = sorted(sellers)
    buyers = sorted(buyers, reverse=True)
    profit = 0
    for i in range(min(len(sellers), len(buyers))):
        if (delta := buyers[i] - sellers[i]) > 0:
            profit += delta
        else:
            break
    return profit


def get_pars() -> tuple[list[int], list[int]]:
    input()
    sellers = [int(_) for _ in input().split(' ')]
    buyers = [int(_) for _ in input().split(' ')]
    return sellers, buyers


print(f'profit: {max_profit()}')



