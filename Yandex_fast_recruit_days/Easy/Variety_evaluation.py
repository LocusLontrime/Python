# accepted on coderun


def evaluate():
    n, products_group, permutation = get_pars()
    last_occurrences = {}
    minimal_distance = n + 1
    for ind_, product_id_ in enumerate(permutation):
        print(f'product_id_: {product_id_}, pg_: {(pg_ := products_group[product_id_])}')
        if pg_ in last_occurrences.keys():
            distance_ = ind_ - last_occurrences[pg_]
            if distance_ < minimal_distance:                                          # 36.6 98
                minimal_distance = distance_
        last_occurrences[pg_] = ind_
    print(f'{n if minimal_distance == n + 1 else minimal_distance}')


def get_pars():
    n = int(input())
    products_group = {(m := [int(_) for _ in input().split()])[0]: m[1] for _ in range(n)}
    permutation = [int(_) for _ in input().split()]
    return n, products_group, permutation


evaluate()
