class Board:

    BLACK = 1
    WHITE = 2

    def __init__(self, rule=19):
        self.rule = rule
        self.board = [[0 for i in range(rule)] for j in range(rule)]

    def play_piece(self, x, y, value):
        if not self.board[x][y]:
            self.board[x][y] = value

