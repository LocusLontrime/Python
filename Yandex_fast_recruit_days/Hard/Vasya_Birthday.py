# accepted on coderun
from collections import defaultdict as d


measures = {'kg': 'g', 'l': 'ml', 'tens': 'cnt'}
thousand_measures = {'kg', 'l'}


def get_info():
    dishes, ingrs_prices, ingrs_info = get_pars()
    print(f'dishes: {dishes}')
    print(f'ingrs_prices: {ingrs_prices}')
    print(f'ingrs_info: {ingrs_info}')
    dishes_info = {}
    ingrs_quantity = d(int)
    overall_price = 0
    # main cycle:
    for dish_name_ in dishes.keys():
        c_, dish_ = dishes[dish_name_]
        print(f'dish_name_: {dish_name_}, friends_q_: {c_}')
        proteins, fats, carbohydrates, kcal = 0.0, 0.0, 0.0, 0.0
        for ingr_ in dish_.keys():
            ingr_info_ = ingrs_info[ingr_]
            part_ = (dish_[ingr_][0] / ingr_info_[0])
            proteins += ingr_info_[2] * part_
            fats += ingr_info_[3] * part_
            carbohydrates += ingr_info_[4] * part_
            kcal += ingr_info_[5] * part_
            ingrs_quantity[ingr_] += c_ * dish_[ingr_][0]
        dishes_info[dish_name_] = f'{proteins} {fats} {carbohydrates} {kcal}'
    # price calculations:
    counts = {_: 0 for _ in ingrs_prices.keys()}
    for ingr_ in ingrs_quantity.keys():
        counts[ingr_] = (q := ingrs_quantity[ingr_] // ingrs_prices[ingr_][1] + 1)
        overall_price += q * ingrs_prices[ingr_][0]
    print(f'overall price: {overall_price}')
    for count in counts.keys():
        print(f'{count} {counts[count]}')
    for dish_name_ in dishes_info:
        print(f'{dish_name_} {dishes_info[dish_name_]}')


def translate(q: int, measure: str) -> tuple[int, str]:
    if measure in measures.keys():
        return 1000 * q if measure in thousand_measures else 10 * q, measures[measure]
    return q, measure


def get_pars():
    # dishes and their ingredients:
    n = int(input())
    dishes = {}
    for j in range(n):
        dish_ = {}
        dish_name, c, z = input().split(' ')
        c, z = int(c), int(z)
        dishes[dish_name] = c, dish_
        for i in range(z):
            ingr_name, a, u = input().split(' ')
            a = int(a)
            dishes[dish_name][1][ingr_name] = translate(a, u)
    # ingredients' prices:
    k = int(input())
    ingrs_prices = {}
    for i in range(k):
        t, p, a, u = input().split(' ')
        a, u = translate(int(a), u)
        p = int(p)
        ingrs_prices[t] = p, a, u
    # info:
    m = int(input())
    ingrs_info = {}
    for i in range(m):
        t, a, u, pr, f, ch, fv = input().split(' ')
        a, u = translate(int(a), u)
        pr, f, ch, fv = map(float, [pr, f, ch, fv])  # float(pr), float(f), float(ch), float(fv)
        ingrs_info[t] = a, u, pr, f, ch, fv
    return dishes, ingrs_prices, ingrs_info


get_info()


