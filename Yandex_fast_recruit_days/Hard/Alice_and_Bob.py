# accepted on coderun
import random
import sys
import math
import time

# distinct numbers quantity in any subarray
MAX: int  # 36.6 98


# BIT-tree implementation
def update(index, value, bits_, n):
    """updating the bit array (Binary indexed tree)"""
    while index <= n:
        bits_[index] += value
        index += index & -index


def range_update(left_b, right_b, val, bits_, n):
    update(left_b, val, bits_, n)
    update(right_b + 1, -val, bits_, n)


def query(idx, bits_) -> int:
    """querying the bit array"""
    sum_ = 0
    while idx:
        sum_ += bits_[idx]
        idx -= idx & -idx
    return sum_


def lower_bound(s, bits):
    """defines the index of an array from which the sum became larger than s"""
    k = 0
    n = len(bits)
    for i in range(int(math.log2(n)), -1, -1):
        if k + (1 << i) < n and bits[k + (1 << i)] <= s:
            k += (1 << i)
            s -= bits[k]
    return k


def encode(m: int, text: list[int]) -> list[int]:
    # an optimized edition...
    new_text = [0 for _ in range(len(text))]
    elements_occurrences: set[int] = set()
    # initialising a bit arrays:
    bits = [0] * ((n := len(text)) + 1)  # holds the rightmost index of any number
    single_bits = [0] * (m + 1)
    # array for holding the last element's occurrences:
    last_visit = [-1] * (m + 1)
    # answer for each query -->> (subarray [l, r] distinct elements quantity):
    # the first running through the array:
    for ind_ in range(len(text)):
        # working with fenwick tree"
        # If last visit is not -1 -->> update -1 at the
        # index equal to last_visit[arr[i]]
        if (lv := last_visit[el_ := text[ind_]]) != -1:
            update(lv + 1, -1, bits, n)
        # Setting last_visit[arr[i]] as i andupdating the bit array accordingly:
        temporal = lv
        last_visit[el_] = ind_
        update(ind_ + 1, 1, bits, n)
        # inserting an element to the tree:
        if el_ not in elements_occurrences:
            # appending an element:
            update(el_, 1, single_bits, m)
            # defining the index of el in the array of permutations (m):
            d_ = len(elements_occurrences) - query(el_, single_bits) + 1
            # appending decoded symbol to the new text:
            new_text[ind_] = el_ + d_
            # adding elements to the set:
            elements_occurrences.add(el_)
        else:
            # If 'i' is equal to right of any query -->> we define the encoded symbol:
            # encoding, caring of the repeated elements, beginning from the second occurrence:
            new_text[ind_] = query(ind_ + 1, bits) - query(temporal, bits)
    # returning the encoded message -->> the new text:
    return new_text


def decode(m: int, encoded_text: list[int]) -> list[int]:
    # an optimized edition...
    old_text = [0 for _ in range(len(encoded_text))]
    elements_occurred: set[int] = set()
    # initialising a bit array 1 and 2:
    bits = [0] * ((n := len(old_text)) + 1)  # holds the rightmost index of any number
    single_bits = [0] * (m + 1)
    for bit_ind_ in range(1, m + 1):
        single_bits[bit_ind_] = bit_ind_ & -bit_ind_
    # array for holding the last element's occurrences:                                # 36.6 98
    last_visit = [-1] * (m + 1)
    # answer for each query -->> (subarray [l, r] distinct elements quantity):
    # the first running through the array:
    for ind_ in range(len(encoded_text)):
        # inserting an element to the tree:
        if (el_ := encoded_text[ind_]) > len(elements_occurred):
            # defining the index of el in the array of permutations (m):
            bit_ind_ = el_ - len(elements_occurred)
            # appending decoded symbol to the new text:
            _el = old_text[ind_] = lower_bound(bit_ind_, single_bits)
            # shaping the decoded elements' occurred set:
            elements_occurred.add(_el)
            # removing the element from bit tree:
            update(_el + 1, -1, single_bits, m)
        else:
            # If 'i' is equal to right of any query -->> we start finding the left border:
            # decoding, caring of the repeated elements, beginning from the second occurrence:
            old_text[ind_] = old_text[lower_bound(query(ind_, bits) - el_, bits)]
        # If last visit is not -1 -->> update -1 at the
        # index equal to last_visit[arr[i]]
        if last_visit[old_text[ind_]] != -1:
            update(last_visit[old_text[ind_]] + 1, -1, bits, n)
        # Setting last_visit[arr[i]] as i and
        # updating the bit array accordingly:
        last_visit[old_text[ind_]] = ind_
        update(ind_ + 1, 1, bits, n)
    # returning the decoded massage:
    return old_text


def solve():
    global MAX
    n, m, type_, text = get_pars()
    MAX, res = m + 1, encode(m, text) if type_ == 1 else decode(m, text)
    return ' '.join(str(_) for _ in res)


def get_pars():
    n, m, type_ = [int(_) for _ in input().split(' ')]
    text = [int(_) for _ in input().split(' ')]
    return n, m, type_, text


def main():
    print(solve())


if __name__ == '__main__':
    main()

# m_ = 2 * 150_000
# text_ = [_ for _ in range(1, m_)]  # [9, 7, 4, 1, 5, 8, 6, 5, 4, 6]
# random.shuffle(text_)
#
# start = time.time_ns()
# res_ = encode(m_, text_)
# finish = time.time_ns()
# print(f'encoded message: {res_}')
# print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

