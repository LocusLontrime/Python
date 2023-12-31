# accepted on codewars.com
import math


def cakes(recipe: dict[str, int], available: dict[str, int]) -> int:
    min_possible = math.inf
    for k, v in recipe.items():
        if k not in available.keys():
            return 0
        min_possible = min(min_possible, available[k] // v)
    return min_possible


# recipe_ = {"apples": 3, "flour": 300, "sugar": 150, "milk": 100, "oil": 100}
# available_ = {"sugar": 500, "flour": 2000, "milk": 2000}

recipe_ = {"flour": 500, "sugar": 200, "eggs": 1}
available_ = {"flour": 1200, "sugar": 1200, "eggs": 5, "milk": 200}

res = cakes(recipe_, available_)
print(f'available items to bake: {cakes(recipe_, available_)}')


