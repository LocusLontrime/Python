MAX_NUM = 100_000 + 1


def length_of_lis(nums: list[int], k: int) -> int:  # 36 366 98 989

    seg_tree = SegmentTreeBottomUp(MAX_NUM)

    for i, num in enumerate(nums):
        # minimal value which can we start the range with:
        lower_bound = max(num - k, 0)
        # the upper border for the range query is 'i - 1':
        print(f'{i} -> {num}, lower_bound (included): {lower_bound}, upper bound (included): {num - 1}')
        longest_k_incr_subsec = 1 + seg_tree.get_max(lower_bound, num)
        print(f'...{longest_k_incr_subsec = }')
        # now let us update the dp value at the position 'num':
        seg_tree.update(num, longest_k_incr_subsec)

    return seg_tree.get_max(0, MAX_NUM - 1)


def compress_data(nums: list[int]) -> list[int]:
    ...


class SegmentTreeBottomUp:  # approx 3 times faster than usual SegTree
    def __init__(self, n):
        # exact seg_tree size defining:
        p = 1
        while p < n:
            p *= 2
        s_tree_l = 2 * p

        self.tree = [0 for _ in range(s_tree_l)]
        self.n = n

    def update(self, pos: int, new_val: int) -> None:
        pos += self.n
        self.tree[pos] = new_val
        pos >>= 1

        while pos:
            self.tree[pos] = max(self.tree[pos << 1], self.tree[(pos << 1) | 1])
            pos >>= 1

    def get_max(self, left: int, right: int) -> int:  # [l, r)]
        left += self.n
        right += self.n
        res = 0

        while left < right:
            if left & 1:
                res = max(res, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                res = max(res, self.tree[right])
            left >>= 1
            right >>= 1

        return res


class SegmentTree:
    def __init__(self, n):

        # exact seg_tree size defining:
        p = 1
        while p < n:
            p *= 2
        s_tree_l = 2 * p

        self.tree = [(0, 0) for _ in range(s_tree_l)]
        self.n = n

    @staticmethod
    def combine(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
        if t1[0] > t2[0]:
            return t1
        if t2[0] > t1[0]:
            return t2
        return t1[0], t1[1] + t2[1]

    def get_max(self, ql: int, qr: int) -> tuple[int, int]:
        # covering...
        def get_max_(vert_ind: int, left_: int, right_: int, ql_: int, qr_: int) -> tuple[int, int]:
            # core:
            # print(f'left_, right_: {left_, right_}, ql_, qr_: {ql_, qr_}')
            # border cases:
            if ql_ > qr_:
                return -1, 0
            if (left_, right_) == (ql_, qr_):
                return self.tree[vert_ind]
            # recurrent relation:
            middle = (left_ + right_) // 2
            i_ = vert_ind << 1
            return self.combine(
                get_max_(i_, left_, middle, ql_, min(qr_, middle)),
                get_max_(i_ + 1, middle + 1, right_, max(ql_, middle + 1), qr_)
            )

        return get_max_(1, 0, self.n - 1, ql, qr)

    def update(self, pos: int, new_val: int):
        # covering...
        def update_(vert_ind: int, left_: int, right_: int):
            # core:
            if left_ == right_:
                self.tree[vert_ind] = new_val, 1
            else:
                middle = (left_ + right_) // 2
                if pos <= middle:
                    update_(vert_ind * 2, left_, middle)
                else:
                    update_(vert_ind * 2 + 1, middle + 1, right_)
                self.tree[vert_ind] = self.combine(
                    self.tree[vert_ind * 2],
                    self.tree[vert_ind * 2 + 1]
                )

        update_(1, 0, self.n - 1)


# seg_tree_ = SegmentTree(10)
#
# seg_tree_.update(0, 10)
#
# seg_tree_.update(1, 11)
# seg_tree_.update(2, 2)
# seg_tree_.update(3, 3)
# seg_tree_.update(4, 1)
# seg_tree_.update(5, 2)
# seg_tree_.update(6, 3)
# seg_tree_.update(7, 5)
# seg_tree_.update(8, 98989)
# seg_tree_.update(9, 98)
#
# print(f'Tree: {seg_tree_.tree}')
#
# print(f'Max: {seg_tree_.get_max(6, 8)}')

nums_ = [4, 2, 1, 4, 3, 4, 5, 8, 15]
k_ = 3

nums_1 = [7, 4, 5, 1, 8, 12, 4, 7]
k_1 = 5

nums_2 = [1, 5]
k_2 = 1

nums_3 = [1, 3, 3, 4]
k_3 = 1

nums_4 = [1, 100, 500, 100000, 100000]
k_4 = 100000

print(f'Length of k-LIS: {length_of_lis(nums_1, k_1)}')


print(f'{(1001 << 1) | 1}')
