# O(n^2) -> solution is right, but should be of a much better notation... n * log(n) or even n...

def min_earnings(arr: list[int]) -> int:
    n = len(arr)

    memo_table = {}

    def rec_core(num_: int, start_ind_: int) -> tuple[int, str]:

        print(f'{start_ind_ = }')

        # border cases:
        if start_ind_ == n:
            print(f'border case 1: {num_}')
            return num_, f'{num_}'
        if start_ind_ == n - 1:
            print(f'border case 2: {num_, arr[-1]}')
            return max(num_, arr[-1]), f'{num_, arr[-1]}'

        # body of rec:
        if (num_, start_ind_) not in memo_table.keys():

            r1, f1 = rec_core(arr[start_ind_ + 1], start_ind_ + 2)
            r2, f2 = rec_core(arr[start_ind_], start_ind_ + 2)
            r3, f3 = rec_core(num_, start_ind_ + 2)
            r1 += max(num_, arr[start_ind_])
            r2 += max(num_, arr[start_ind_ + 1])
            r3 += max(arr[start_ind_], arr[start_ind_ + 1])

            min_ = min(r1, r2, r3)
            f = f''

            if min_ == r1:
                f = f'|{num_, arr[start_ind_]}|' + f1
            elif min_ == r2:
                f = f'|{num_, arr[start_ind_ + 1]}|' + f2
            else:
                f = f'|{arr[start_ind_], arr[start_ind_ + 1]}|' + f3

            # recurrent relation:
            memo_table[(num_, start_ind_)] = min_, f

        # memoization:
        return memo_table[(num_, start_ind_)]

    res = rec_core(arr[0], 1) if arr else 0

    print(f'memo_len -> {len(memo_table)}')

    return res


test_case = [i for i in range(100)]  # res -> 22
test_case_ = [9, 5, 7, 8, 6, 3, 6, 17, 89, 8, 3, 6, 98]
test_case__ = [9, 5, 7, 8, 6, 13, 2, 7, 5]

test = [98, 9, 5, 7, 8, 6]

print(f'res -> {min_earnings(test)}')
