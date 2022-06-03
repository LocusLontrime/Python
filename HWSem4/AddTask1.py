# Давайте представим, что ваша компания только что наняла вашего друга из колледжа и заплатила вам реферальный бонус. Потрясающе!
# Чтобы отпраздновать, вы берете свою команду в очень странный бар по соседству и используете реферальный бонус, чтобы купить и
# построить самую большую трехмерную пирамиду из пивных банок, которую вы можете.
# Пирамида пивных банок будет квадратировать количество банок на каждом уровне - 1 банка на верхнем уровне, 4 на втором, 9 на следующем, 16, 25...
# Определите функцию beeramid, чтобы вернуть количество полных уровней пирамиды пивных банок, которую вы можете сделать, учитывая параметры:
# реферальный бонус и цена пивной банки.
# Например: beeramid(1500, 2)# 12
# beeramid(5000, 3)# 16

def get_levels(ref_money: int, one_can_cost: int) -> int:
    beer_cans_quantity = ref_money // one_can_cost
    print(f'beer_cans_quantity = {beer_cans_quantity}')
    levels_done = []
    counter = 0

    # it counts levels until the building of new full-level is possible
    while True:
        beer_cans_quantity -= (counter + 1) ** 2  # if the building of the next level is possible then we increase the counter
        if beer_cans_quantity < 0:  # the break condition
            break
        else:
            counter += 1  # count's increasing
            levels_done.append(counter ** 2)  # adding the cans' quantity for the current level
    print(f'levels done: {levels_done}')
    return counter


print(get_levels(1500, 2))
print(get_levels(5000, 3))
print(get_levels(1000, 1000))
print(get_levels(30, 2))
