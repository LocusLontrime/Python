# accepted on codewars, also beats insane version of this task (that is simpler)
thresholds = [3 ** i for i in range(1, 20)]  # 36 366 98 989 98989
colours = {'R', 'G', 'B'}
answers = dict()


# finds the nearest number of a type 3 ** k + 1 to the length of row
def diff_btw_len_and_nearest_threshold(length):
    for i in range(len(thresholds)):
        if thresholds[i] > length - 1:
            return length - thresholds[i - 1]


# finds the answer for two input colours
def solve_two(cl1, cl2):
    return cl1 if cl1 == cl2 else (colours - {cl1, cl2}).pop()


# main method
def triangle(row):
    global answers  # for visualization

    def rec_slicer(left, right, depth):
        global answers
        # print(f'Row remained: {row[left: right + 1]}')  # demonstrating
        if depth not in answers.keys():
            answers[depth] = [f'depth: {depth}', row[left: right + 1]]
        else:
            answers[depth].append(row[left: right + 1])
        # base cases:
        res = None
        if right - left == 0:
            res = row[left]
        elif right - left == 1:
            res = solve_two(row[left], row[right])
        elif right - left == 2:
            res = solve_two(solve_two(row[left], row[left + 1]), solve_two(row[left + 1], row[right]))

        if res is not None:
            # print(f'The base result of this step is: {res}')
            if right > left:
                if depth + 1 not in answers.keys():
                    answers[depth + 1] = [f'depth: {depth + 1}', res]
                else:
                    answers[depth + 1].append(res)
            return res

        # body of rec:
        diff = diff_btw_len_and_nearest_threshold(right - left + 1)
        # print(f'The suitable difference found: {diff}')
        left_simplified, right_simplified = rec_slicer(left, left + diff - 1, depth + 1), rec_slicer(right - diff + 1, right, depth + 1)

        # final step
        fin_res = solve_two(left_simplified, right_simplified)
        # print(f'FINAL RESULT: {fin_res}')
        return fin_res

    # recursion call
    result = rec_slicer(0, len(row) - 1, 0)
    for key in answers.keys():
        print(answers[key])
    return result


print(triangle('BGBGRBGRRBGRBGGGRBGRGBGRRGGRBGRGRBGBRGBGBGRGBGBGBGRRBRGRRGBGRGBRGRBGRBGRBBGBRGRGRBGRGBGBGRBGRRBGRBGGGRBGRGBGRRGGRBGRGRBGBRGBGBGRGBGBGBGRRBGBGRBGRRBGRBGGGRBGRGBGRRGGRBBGBGRBGRRBGRBGGGRBGRGBGRRGGRBGRGRBGBRGBGBGRGBGBGBGRRBRGRRGBGRGBRGRBGRBGRBBGBRGRGRBGRGBRGBBRGGBRBGGRBBGBRGRGRBGRGBRGBBRGGBRBGGRBRGGRBGRGRBGBRGBGBGRGBGBGBGRRBRGRRGBGRGBRGRBGRBGRBBGBRGRGRBGRGBRGBBRGGBRBGGRBRB'))  # G
# print(triangle('GGG'))
# print(solve_two('G', 'R'))
# print(3 ** 10)











# print(3 ** 18)








