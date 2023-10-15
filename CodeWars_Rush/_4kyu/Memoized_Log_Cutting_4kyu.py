# accepted on codewars.com

# Your new function as given to you by me, your boss.
# covering
def cut_log(p, n):
    # memoization table drops runtime from O(2^n) to-> O(n^2)
    memo_table = dict()

    # recursion core
    def rec_seeker(n_rec):

        # border case
        if n == 0:
            return 0

        # calculation of memo cells (only one time!)
        if n_rec not in memo_table.keys():
            q = 0

            for i in range(1, len(p)):
                if n_rec - i >= 0:
                    q = max(q, p[i] + rec_seeker(n_rec - i))

            memo_table[n_rec] = q

        return memo_table[n_rec]

    return rec_seeker(n)  # Good luck intern!


p_test = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 32, 35, 39, 43, 43, 45, 49, 50, 54, 57, 60, 65, 68, 70, 74, 80, 81, 84, 85, 87, 91, 95, 99, 101, 104, 107, 112, 115, 116, 119]
print(cut_log(p_test, 22))
print(cut_log(p_test, 35))
