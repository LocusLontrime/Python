# accepted on leetcode.com

import math


def smallest_sufficient_team(req_skills: list[str], people: list[list[str]]) -> list[int]:
    # let us use bitmasks instead of skills' sets:
    k = 0b1
    skills_masks = {}
    for req_skill in req_skills:
        skills_masks[req_skill] = k
        k <<= 1
    req_skills_mask = sum(v for v in skills_masks.values())
    print(f'{skills_masks = }')
    print(f'{bin(req_skills_mask) = }')
    people_skills_masks = []
    for person in people:
        person_skill_mask = 0
        for skill in person:
            person_skill_mask += skills_masks[skill]
        people_skills_masks += [person_skill_mask]
    print(f'{people_skills_masks = }')
    # now dp starts (border case in dp memo):
    dp_memoization_table = {0: (0, None, None)}
    dp(req_skills_mask, people_skills_masks, dp_memoization_table)
    print(f'{dp_memoization_table = }')
    # shortest team recovering:
    shortest_team = []
    mask = req_skills_mask
    while mask >= 0 and (i := dp_memoization_table[mask][1]) is not None:
        shortest_team += [i]
        mask = dp_memoization_table[mask][2]
    return shortest_team


def dp(mask: int, people_skills_masks: list[int], dp_memoization_table: dict) -> int:
    print(f'{mask = }')
    if mask not in dp_memoization_table.keys():
        res = math.inf
        prev_i = None
        prev_mask = None
        for i, person_skill_mask in enumerate(people_skills_masks):
            new_mask = and_not(mask, person_skill_mask)
            if new_mask != mask:
                r_ = dp(new_mask, people_skills_masks, dp_memoization_table)[0] + 1
                if r_ < res:
                    res = r_
                    prev_i = i
                    prev_mask = new_mask
        dp_memoization_table[mask] = res, prev_i, prev_mask
    return dp_memoization_table[mask]


# for exact covering
def check(n: int, m: int) -> bool:
    return n.bit_count() - m.bit_count() == (n ^ m).bit_count()


# for covering
def and_not(n: int, m: int) -> int:
    res = n & (~m)
    print(f'and_not({bin(n)}, {bin(m)}) -> {bin(res)}')
    return res


# tests:
# x = 0b1
# arr = [x]
# for i in range(9 + 1):
#     arr += [arr[-1] << 1]
#
# print(f'{x = }')
# print(f'{arr = }')
#
# n1 = 0b101101
#
# m1 = 0b010001
# m2 = 0b001101
#
# print(f'{bin(n1 ^ m1) = }')
# print(f'{bin(n1 ^ m2) = }')
#
# print(f'{n1.bit_count(), m1.bit_count(), m2.bit_count() = }')
#
#
# print(f'{check(n1, m1) = }')
# print(f'{check(n1, m2) = }')
#
# print(f'{bin(and_not(n1, m1))}')
# print(f'{bin(and_not(n1, m2))}')

test_ex = (
    ["algorithms", "math", "java", "reactjs", "csharp", "aws"],
    [
        ["algorithms", "math", "java"],
        ["algorithms", "math", "reactjs"],
        ["java", "csharp", "aws"],
        ["reactjs", "csharp"],
        ["csharp", "math"],
        ["aws", "java"]
    ]
)

test_ex_1 = (
    ["java", "nodejs", "reactjs"],
    [
        ["java"],
        ["nodejs"],
        ["nodejs", "reactjs"]
    ]
)

test_ex_2 = (
    ["hdbxcuzyzhliwv", "uvwlzkmzgis", "sdi", "bztg", "ylopoifzkacuwp", "dzsgleocfpl"],
    [
        ["hdbxcuzyzhliwv", "dzsgleocfpl"],  # 0
        ["hdbxcuzyzhliwv", "sdi", "ylopoifzkacuwp", "dzsgleocfpl"],
        ["bztg", "ylopoifzkacuwp"],
        ["bztg", "dzsgleocfpl"],
        ["hdbxcuzyzhliwv", "bztg"],
        ["dzsgleocfpl"],
        ["uvwlzkmzgis"],
        ["dzsgleocfpl"],
        ["hdbxcuzyzhliwv"],
        [],
        ["dzsgleocfpl"],
        ["hdbxcuzyzhliwv"],
        [],
        ["hdbxcuzyzhliwv", "ylopoifzkacuwp"],
        ["sdi"],
        ["bztg", "dzsgleocfpl"],
        ["hdbxcuzyzhliwv", "uvwlzkmzgis", "sdi", "bztg", "ylopoifzkacuwp"],  # 16
        ["hdbxcuzyzhliwv", "sdi"],
        ["hdbxcuzyzhliwv", "ylopoifzkacuwp"],
        ["sdi", "bztg", "ylopoifzkacuwp", "dzsgleocfpl"],
        ["dzsgleocfpl"],
        ["sdi", "ylopoifzkacuwp"],
        ["hdbxcuzyzhliwv", "uvwlzkmzgis", "sdi"],
        [],
        [],
        ["ylopoifzkacuwp"],
        [],
        ["sdi", "bztg"],
        ["bztg", "dzsgleocfpl"],
        ["sdi", "bztg"]
    ]
)

print(f'test ex res -> {smallest_sufficient_team(*test_ex)}')                         # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {smallest_sufficient_team(*test_ex_1)}')
print(f'test_ex_2 res -> {smallest_sufficient_team(*test_ex_2)}')

# print(f'{and_not(0b10, 0b10111)}')
