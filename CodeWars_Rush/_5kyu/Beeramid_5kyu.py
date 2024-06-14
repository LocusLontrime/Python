# accepted on codewars.com


def beeramid(bonus: int, price: int) -> int:
    def beeramid_cans(n: int) -> int:
        return n * (n + 1) * (2 * n + 1) // 6

    beer_cans = max(0, bonus) // price
    potential_res = int(pow(3 * beer_cans, 1 / 3))

    return potential_res - (0 if beeramid_cans(potential_res) <= beer_cans else 1)

