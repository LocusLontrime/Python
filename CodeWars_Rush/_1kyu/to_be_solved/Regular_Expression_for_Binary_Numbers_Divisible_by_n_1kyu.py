# accepted on codewars.com
BASE = 2
EMPTY = 'e'


def regex_divisible_by(n: int):
    # base case:
    if n == 1:
        return f'^(0|1)+$'
    fsm, fsm_rev, bridges = build_fsm(n)
    print(f'fsm: {fsm}')
    print(f'fsm_rev: {fsm_rev}')
    print(f'bridges: {bridges}')
    # now let us convert fsm to a regular expression:
    reg_exp = convert_fsm_to_regex(n, fsm, fsm_rev, bridges)
    return reg_exp


def build_fsm(n: int) -> tuple[dict, dict, list[list[str]]]:
    fsm: dict[int, set[int]] = {_: set() for _ in range(n)}
    fsm_rev: dict[int, set[int]] = {_: set() for _ in range(n)}
    bridges = [['' for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for bit_ in range(BASE):
            add_bridge(i, (2 * i + bit_) % n, f'{bit_}', fsm, fsm_rev, bridges)
    # returning res:
    return fsm, fsm_rev, bridges


def add_bridge(from_: int, to_: int, name_: str, fsm: dict[int, set[int]], fsm_rev: dict[int, set[int]], bridges: list[list[str]]):
    if from_ != to_:
        fsm[from_].add(to_)
        fsm_rev[to_].add(from_)
    bridges[from_][to_] = name_


def delete_bridge(from_: int, to_: int, fsm: dict[int, set[int]], fsm_rev: dict[int, set[int]], bridges: list[list[str]]):
    if to_ in fsm[from_]:
        fsm[from_].remove(to_)
    if from_ in fsm_rev[to_]:
        fsm_rev[to_].remove(from_)


def convert_fsm_to_regex(n: int, fsm: dict[int, set[int]], fsm_rev: dict[int, set[int]], bridges: list[list[str]]) -> str:
    for q in range(1, n):  # 0 is not included...
        # print(f'q: {q}')
        eliminate_state(q, fsm, fsm_rev, bridges)
    # print(f'bridges: {bridges}')
    return f'^(?:{bridges[0][0]})+$'


def eliminate_state(state_to_be_eliminated: int, fsm: dict[int, set[int]], fsm_rev: dict[int, set[int]], bridges: list[list[str]]):
    predecessors = set(fsm_rev[state_to_be_eliminated])
    successors = set(fsm[state_to_be_eliminated])
    for q_predecessor in predecessors:
        for q_successor in successors:
            # print(f'...qp, qs: {q_predecessor, q_successor}')
            # pred->succ and succ->pred bridges elimination:
            delete_bridge(q_predecessor, q_successor, fsm, fsm_rev, bridges)
            pre_suc_bridge = bridges[q_predecessor][q_successor]  # d
            pre_state_bridge = bridges[q_predecessor][state_to_be_eliminated]  # a
            state_suc_bridge = bridges[state_to_be_eliminated][q_successor]  # c
            if b := bridges[state_to_be_eliminated][state_to_be_eliminated]:  # b
                # d+ab*c
                if len(b) > 1:
                    aux = f'(?:{b})*'
                else:
                    aux = f'{b}*'
            else:
                # d+ac
                aux = EMPTY
            # bridges update:
            name_ = sup_up_exp(pre_suc_bridge, process_exp(pre_state_bridge, aux, state_suc_bridge))
            # print(f'......name_: {name_}')
            add_bridge(q_predecessor, q_successor, name_, fsm, fsm_rev, bridges)
            delete_bridge(q_predecessor, state_to_be_eliminated, fsm, fsm_rev, bridges)  # a
            delete_bridge(state_to_be_eliminated, q_successor, fsm, fsm_rev, bridges)  # c


def sup_up_exp(*expressions):
    good_ones = [exp for exp in expressions if exp and exp != EMPTY]
    return aggregate(good_ones, '|')


def process_exp(*expressions):
    not_empties = [exp for exp in expressions if exp != EMPTY]
    return aggregate(not_empties, '')


def aggregate(expressions, separator):
    if len(expressions) == 1:
        return expressions[0]
    return separator.join([f'(?:{exp})' if '|' in exp else exp for exp in expressions])


# print(f'fsm, fsm_rev: {build_fsm(3)}')
# print(f'fsm, fsm_rev: {build_fsm(5)}')
# print(f'fsm, fsm_rev: {build_fsm(7)}')
# fsm_, fsm_rev_, bridges_ = build_fsm(7)

print(f'regexp: {(r := regex_divisible_by(3))}')
print(f'size: {len(r)}')


