# accepted on coderun
import sys


def pallets_to_send():
    n, parents, delivery_ids = get_pars()
    for pallet_id_ in range(n):
        validator(pallet_id_, parents, delivery_ids)
    del delivery_ids
    parents = [str(ind_ + 1) for ind_, _ in enumerate(parents) if not _]
    print(f'{len(parents)}')
    print(f'{" ".join(parents)}')


def validator(id_: int, parents: list[int], delivery_ids: list[int]) -> None:
    # bubble's popping up:
    ind_ = id_
    if not delivery_ids[ind_]:
        while (pid := parents[ind_]) != -1:
            parents[ind_] = -1
            if pid - 1 >= 0:
                ind_ = pid - 1
            else:
                break


def get_pars():
    n = int(input())
    delivery_ids = [int(_) for _ in input().split()]
    parents = [int(_) for _ in input().split()]
    k = int(input())
    if k > 0:
        invalid_ids = {int(_) for _ in input().split()}
        for _ in range(n):
            if delivery_ids[_] in invalid_ids:
                delivery_ids[_] = 0
        del invalid_ids
    return n, parents, delivery_ids


def main():
    pallets_to_send()


if __name__ == '__main__':
    main()










































                                                                                      # 36.6 98









