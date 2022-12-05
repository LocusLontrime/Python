def get_ovens(num_of_trays: int, oven_capacities: list[int]):
    results = []

    print(f'num_of_trays: {num_of_trays}, oven_capacities: {oven_capacities}')

    def rec_seeker(order_remained: int, ovens_used: list[int]):
        # border case:
        if order_remained <= 0:
            return [abs(order_remained), ovens_used]

        return rec_seeker(order_remained - 4, ovens_used + [4])
        # rec_seeker(order_remained - 10, ovens_used + [10])

    for i in range(num_of_trays // 10 + 2):
        k = rec_seeker(num_of_trays - i * 10, [])
        k[1] += [10 for i in range(i)]
        results.append(k)

    results = list(sorted(results, key=lambda x: (x[0], len(x[1]))))

    # print(f'results:')
    # for res in results:
    #     print(res)

    return results[0]


# print(f'Best partition: {get_ovens(100, [10, 4])}')
print(get_ovens(10, [10, 4]))  # [10]
print(get_ovens(20, [10, 4]))  # [10, 10]
print(get_ovens(12, [10, 4]))  # [4, 4, 4]
print(get_ovens(29, [10, 4]))  # [10, 10, 10]


