import time


class Board:

    BLACK = 1
    WHITE = 2

    def __init__(self, rule=19):
        self.rule = rule
        self.board = [[0 for i in range(rule)] for j in range(rule)]
        self.last = None

    def play_piece(self, x, y, value):
        if not self.board[x][y]:
            self.board[x][y] = value
            self.last = [x, y]


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
