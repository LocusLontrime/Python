# accepted on codewars.com
import time


def draw(n: int):
    """draw the pattern recursively"""
    def rec_painter(n_: int):
        """aux recursive method"""
        # base case:
        if n_ == 1:
            return ["_|"], [" _ ", "|_|"]
        # height and width:
        h, w = 2 ** (n_ - 1) + 1, 2 * n_ + 1,
        # aux counter:
        counter = 0
        # recurrent relation
        _arr, arr_ = rec_painter(n_ - 1)
        # create a next iteration arrays:
        _new_arr = ["" for _ in range(h - 1)]
        new_arr_ = ["" for _ in range(h)]
        s = new_arr_[0] = " " + " ".join(['_' for _ in range(n_)]) + " "
        # strings concat for upper _array:
        for i, string in enumerate(_arr):
            _new_arr[counter] = "_" + string if counter == len(_arr) - 1 and n_ > 2 else string
            d = "|" + " " * (w - len(string) - 1)
            new_arr_[counter + 1] = d[:-1] + "_" + string if counter == len(_arr) - 1 and n_ > 2 else d + string
            counter += 1
        # strings concat for lower array_:
        for i, string in enumerate(arr_[1:]):
            _new_arr[counter] = string
            d = "|_" if counter + 1 == h - 1 else "|" + " " * (w - len(string) - 1)
            new_arr_[counter + 1] = d + string
            counter += 1
        # result:
        return _new_arr, new_arr_
    # joining array's strings:
    return '\n'.join(rec_painter(n)[1])


start = time.time_ns()
pattern = draw(10 + 2)
print(f'pattern:\n{pattern}')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


