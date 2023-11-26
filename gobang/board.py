class GobangBoard:

    BLACK = 1
    WHITE = 2

    def __init__(self, rule=19):
        self.rule = rule
        self.board = [[0 for i in range(rule)] for j in range(rule)]
        self.black_turn = True
        self.active_player = None
        self.players = []

    def set_piece(self, i, j):
        if self.board[i][j] == 0:
            self.board[i][j] = self.BLACK if self.black_turn else self.WHITE
            self.black_turn = not self.black_turn


