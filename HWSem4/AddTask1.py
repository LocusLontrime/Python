def get_levels(ref_money: int, one_can_cost: int) -> int:
    beer_cans_quantity = ref_money // one_can_cost
    print(f'beer_cans_quantity = {beer_cans_quantity}')
    levels_done = []
    counter = 0
    while True:
        beer_cans_quantity -= (counter + 1) ** 2
        if beer_cans_quantity < 0:
            break
        else:
            counter += 1
            levels_done.append(counter ** 2)
    print(f'levels done: {levels_done}')
    return counter


print(get_levels(1500, 2))
print(get_levels(5000, 3))
print(get_levels(1000, 1000))
print(get_levels(30, 2))
