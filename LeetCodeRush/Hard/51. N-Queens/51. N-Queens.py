# accepted on leetcode.com

# The n - queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

# Given an integer n, return all distinct solutions to the n - queens puzzle.You may return the answer in any order.

# Each solution contains a distinct board configuration of the n - queens' placement,
# where 'Q' and '.' both indicate a queen and an empty space, respectively.

# Example 1:
# Input: n = 4
# Output: [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
# Explanation: There exist two distinct solutions to the 4 - queens puzzle as shown above

# Example 2:
# Input: n = 1
# Output: [["Q"]]

# Constraints: 1 <= n <= 9


def solve_n_queens(n: int) -> list[list[str]]:
    # let us define 3 sets: diag_plus, diag_minus and vertical...
    diag_plus, diag_minus, vertical = set(), set(), set()
    # now the recursive seeker starts working:
    solutions = []
    rec_seeker(0, n, diag_plus, diag_minus, vertical, [], solutions)
    # print(f'{solutions = }')

    sols = []

    for sol in solutions:
        matrix_q = [['.' for _ in range(n)] for _ in range(n)]
        for ind, i in enumerate(sol):
            matrix_q[ind][i] = 'Q'
        matrix_q = [''.join(row) for row in matrix_q]
        sols += [matrix_q]
    print(f'{len(sols)} solutions found...')
    return sols


def rec_seeker(j: int, n: int, diag_plus: set[int], diag_minus: set[int], vertical: set[int], sol: list[int], solutions: list[list[int]]):
    # border case:
    if j == n:
        solutions += [sol]
    # recurrent relation:
    for i in range(n):
        if j + i not in diag_plus and j - i not in diag_minus and i not in vertical:
            rec_seeker(j + 1, n, diag_plus | {j + i}, diag_minus | {j - i}, vertical | {i}, sol + [i], solutions)


test_ex = 9

res = solve_n_queens(test_ex)

print(f'test ex res -> {len(res)} solutions found')                                    # 36 366 98 989 98989 LL

for i, solution in enumerate(res):
    print(f'solution {i + 1}')
    for row_ in solution:
        print(f'{row_}')


