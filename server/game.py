from config import config
from gobang.board import Board


class GameServer:
    def __init__(self, room):
        self.board = Board(config.rule)
        self.is_black = True
        self.room = room
        self.players = {}
        self.member_count = 0
        self.started = False

    def reset(self):
        self.board = Board(config.rule)
        self.is_black = True
        self.started = False

    def drop(self, sid):
        if sid in self.players:
            del self.players[sid]
            self.member_count -= 1
            for s in self.players:
                self.players[s] = 1
            self.reset()

    def join(self, sid):
        self.member_count += 1
        if not self.players:
            self.players[sid] = 1
        else:
            self.players[sid] = 2

    def check_right(self, sid):
        color = self.players[sid]
        return (color == self.board.BLACK) == self.is_black

    def move(self, user_id, pos):
        x, y = pos
        value = self.players[user_id]
        if not self.check_right(user_id):
            return
        self.board.play_piece(x, y, value)
        self.is_black = not self.is_black

    @property
    def info(self):
        return {
            'players': self.players,
            'room': self.room
        }

    @property
    def board_detail(self):
        return {
            'board': self.board.board,
            'is_black': self.is_black,
            'last': self.board.last
        }
