import time


class Board:

    BLACK = 1
    WHITE = 2

    DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0)]

    def __init__(self, rule=19):
        self.rule = rule
        self.board = [[0 for i in range(rule)] for j in range(rule)]
        self.last = None
        self.state_board = [[PieceScore(i, j) for i in range(rule)] for j in range(rule)]
        self.winner = None

    def play_piece(self, x, y, color):
        if not self.board[x][y]:
            self.board[x][y] = color
            self.last = [x, y]
            return True
        return False

    def update_score(self, x, y, color):
        p = self.state_board[x][y]
        p.color = color
        for dir_index, direction in enumerate(self.DIRECTIONS):
            px, py = direction[0] + x, direction[1] + y
            nx, ny = -direction[0] + x, -direction[1] + y
            score1 = self.check_score(px, py, color, dir_index)
            score2 = self.check_score(nx, ny, color, dir_index)
            new_score = score1 + score2 + 1
            p.scores[dir_index] = new_score
            if score1:
                self._update_direction_score(px, py, color, dir_index, new_score, reverse=False)
            if score2:
                self._update_direction_score(nx, ny, color, dir_index, new_score, reverse=True)

            if new_score >= 5:
                self.winner = color

    def check_score(self, x, y, color, direction):
        if x < 0 or y < 0 or x >= self.rule or y >= self.rule:
            return 0

        piece = self.state_board[x][y]
        if piece.color != color:
            return 0
        return piece.scores[direction]

    def _update_direction_score(self, x, y, color, direction, score, reverse=False):
        dir_pos = self.DIRECTIONS[direction] if not reverse else [-1 * i for i in self.DIRECTIONS[direction]]
        p = self.state_board[x][y]
        while p.color == color:
            p.scores[direction] = score
            x, y = dir_pos[0] + x, dir_pos[1] + y
            if x < 0 or y < 0 or x >= self.rule or y >= self.rule:
                break
            p = self.state_board[x][y]


class PieceScore:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None
        self.scores = [0 for i in range(4)]


class Player:
    def __init__(self, sid):
        self.sid = sid
        self.ready = False
        self.color = None
        self.number = time.time()

    def reset(self):
        self.ready = False
        self.color = None

    def to_json(self):
        return {'ready': self.ready, 'color': self.color}

    @classmethod
    def make_player(cls, sid):
        return cls(sid)
