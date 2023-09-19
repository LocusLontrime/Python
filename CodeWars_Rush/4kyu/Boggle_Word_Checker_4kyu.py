# accepted on codewars.com
class Boggle:
    # delta j and i:
    WALK = [(dy, dx) for dx in range(-1, 2) for dy in range(-1, 2) if (dy, dx) != (0, 0)]

    def __init__(self, board: list[list[str]], word: str):
        self.word = word
        self.J, self.I = len(board), len(board[0])
        self.board = [[board[j][i] for i in range(self.I)] for j in range(self.J)]
        self.rec_counter = 0
        for row in self.board:
            print(f'{row}')

    def check(self):
        for j in range(self.J):
            for i in range(self.I):
                print(f'dfs({j, i, 0})')
                if self.dfs(j, i, 0):
                    return True
        return False

    def dfs(self, j, i, k):  # k -->> current chain length
        self.rec_counter += 1
        print(f'j, i, k: {j, i, k}')
        # base case:
        if k >= len(self.word): return True
        # body of dfs:
        if 0 <= j < self.J and 0 <= i < self.I and self.board[j][i] != '*':
            if self.board[j][i] == self.word[k]:
                k += 1
                self.board[j][i] = '*'
                # recurrent relation:
                for djdi in self.WALK:
                    if self.dfs(j + djdi[0], i + djdi[1], k):
                        return True
                # backtracking:
                k -= 1
                self.board[j][i] = self.word[k]
        return False

def find_word(board: list[list[str]], word: str):
    return Boggle(board, word).check()








board_to_solve = [
      ["E","A","R","A"],
      ["N","L","E","C"],
      ["I","A","I","S"],
      ["B","Y","O","R"]
    ]

print(find_word(board_to_solve, 'RSCAREIOYBAILNEA'))
print(find_word(board_to_solve, 'BAILER'))








