import time

from client import client
from config import config
from gobang.board import Board, Player


class BaseGameClient:
    CREATED = 0
    READY = 1
    STARTED = 2
    END = 3

    def __init__(self):
        self.color = None
        self.board = Board(config.rule)
        self.is_black = True
        self.state = self.CREATED

    def reset(self):
        self.color = None
        self.board = Board(config.rule)
        self.is_black = True
        self.state = self.CREATED

    def start(self, color):
        self.board = Board(config.rule)
        self.is_black = True
        self.color = color
        self.state = self.STARTED

    @property
    def started(self):
        return self.state == self.STARTED

    @property
    def is_my_turn(self):
        return self.started and self.is_black == (self.color == Board.BLACK)


class OnlineGameClient(BaseGameClient):
    def __init__(self):
        super().__init__()
        self.sid = None
        self.players = {}
        self.room = None
        self.connected = False

    def make_init(self):
        if not self.connected:
            url = config.host
            print('connecting', url)
            client.connect(url, socketio_path='/socket-game', transports=['websocket'], namespaces=['/game'])
            client.emit('join_room', namespace='/game')
            self.sid = client.get_sid('/game')
            self.connected = True

    def quit(self):
        self.state = self.END

    def joined(self, data):
        for sid, player_info in data['players'].items():
            if sid not in self.players:
                self.players[sid] = Player.make_player(sid)
        self.room = data['room']

    def ready(self):
        self.players[self.sid].ready = True
        client.emit('ready', self.room, namespace='/game')
        self.state = self.READY

    def start(self, data):
        for sid, player_info in data['players'].items():
            if sid not in self.players:
                print('wtf', data, self.players)
                return
            self.players[sid].ready = player_info['ready']
            self.players[sid].color = player_info['color']

        self.room = data['room']
        super().start(self.players[self.sid].color)

    def update(self, data):
        x,  y = data['pos']
        color = data['color']
        self.board.play_piece(x, y, color)
        self.board.last = [x, y]
        self.is_black = data['is_black']

    def play(self, x, y):
        if self.started:
            data = {'room': self.room, 'pos': [x, y]}
            client.emit('play', data=data, namespace='/game')


class SingleGameClient(BaseGameClient):
    def __init__(self):
        super().__init__()

    def make_init(self):
        pass

    def play(self, x, y):
        self.board.play_piece(x, y, self.color)


online_game = OnlineGameClient()
local_game = SingleGameClient()
