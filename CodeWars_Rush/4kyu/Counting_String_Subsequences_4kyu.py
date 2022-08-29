# accepted on codewars.com
def count_subsequences(a, b):  # "hello" in "amhheeyteelltotoo"

    needle_len = len(a)
    haystack_len = len(b)

    memo_table = dict()

    def rec_seeker(needle_index, haystack_index):

        # base cases
        if haystack_index > haystack_len:
            return 0

        if needle_index == needle_len:
            return 1

        # body of method
        counter = 0

        if (needle_index, haystack_index) not in memo_table.keys():

            # recursion depth
            for i in range(haystack_index, haystack_len):
                if a[needle_index] == b[i]:
                    counter += rec_seeker(needle_index + 1, i + 1)

            memo_table[(needle_index, haystack_index)] = counter

        return memo_table[(needle_index, haystack_index)]

    return rec_seeker(0, 0)


print(count_subsequences("happy birthday", "hhaappyy bbiirrtthhddaayy"))
