# accepted on codewars.com


def self_converge(n: int) -> int:
    return rec_core(n, 0, set())


def rec_core(n: int, steps: int, visited: set[int]):
    print(f'{n = } | {visited = }')
    return (steps + 1 if (new_n := kaprekar_routine(n)) in visited else rec_core(new_n, steps + 1, visited | {new_n})) if n else -1


def kaprekar_routine(n: int) -> int:
    digs = str(n)
    asc_digs, desc_digs = sorted(digs), sorted(digs, reverse=True)
    print(f'...{asc_digs, desc_digs = }')
    delta = str(int(''.join(desc_digs) + '0' * (len(digs) - len(desc_digs))) - int(''.join(asc_digs)))
    delta = int(''.join(delta) + '0' * (len(digs) - len(delta)))
    return delta


n_ = 1234  # -> 4
n_x = 992299229  # -> 22
n_z = 2111  # -> 6
n_extra = 7  # -> -1

print(f'res: {self_converge(n_extra)}')

# print(f'{sorted(f"916748289")}')

