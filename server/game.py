import time

from config import config
from gobang.board import Board, Player


class GameServer:
    def __init__(self, room):
        self.board = Board(config.rule)
        self.is_black = True
        self.room = room
        self.players = {}
        self.started = False

    @property
    def full(self):
        return len(self.players) == 2

    def get_ready(self, sid):
        p = self.players[sid]
        p.ready = True

    def all_ready(self):
        for p in self.players.values():
            if not p.ready:
                return False
        return self.full

    def start(self):
        players = sorted(self.players.values(), key=lambda x: x.number)
        for i, p in enumerate(players):
            p.color = i+1
        self.is_black = True
        self.started = True

    def reset(self):
        self.board = Board(config.rule)
        self.is_black = True
        self.started = False
        for p in self.players.values():
            p.reset()

    def drop(self, sid):
        if sid in self.players:
            del self.players[sid]
            self.reset()

    def join(self, sid):
        if self.full or sid in self.players:
            return False
        player = Player(sid)
        self.players[sid] = player
        return True

    def check_right(self, player):
        return (player.color == self.board.BLACK) == self.is_black

    def play_piece(self, user_id, pos):
        x, y = pos
        player = self.players[user_id]
        if not self.check_right(player):
            return None

        if self.board.play_piece(x, y, player.color):
            self.is_black = not self.is_black
            return {
                'color': player.color,
                'is_black': self.is_black,
                'pos': self.board.last
            }

    def finish(self):
        print("game finished")
        self.reset()

    @property
    def info(self):
        return {
            'players': {k: v.to_json() for k, v in self.players.items()},
            'room': self.room
        }




