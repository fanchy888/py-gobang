from client import client
from config import config
from gobang.board import Board


class BaseGameClient:
    def __init__(self):
        self.color = Board.BLACK
        self.board = Board(config.rule)
        self.is_black = True
        self.started = False

    def reset(self):
        self.color = Board.BLACK
        self.board = Board(config.rule)
        self.is_black = True
        self.started = False

    def start(self, data):
        self.board = Board(config.rule)
        self.is_black = True
        self.started = True
        self.color = data.get('color', Board.BLACK)

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
            client.connect(url, socketio_path='/socket-game', transports=['websocket'], namespaces=['/game'])
            client.emit('join_room', namespace='/game')
            self.sid = client.get_sid('/game')
            self.connected = True

    def quit(self):
        self.reset()

    def start(self, data):
        super().start(data)
        self.players = data['players']
        self.room = data['room']
        self.color = self.players[self.sid]

    def update(self, data):
        board = data['board']
        self.board.board = board
        self.board.last = data['last']
        self.is_black = data['is_black']

    def play(self, x, y):
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
