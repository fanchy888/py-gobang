from client import client
from config import config
from gobang.board import Board


class GameClient:
    def __init__(self):
        self.board = Board(config.rule)
        self.is_black = True
        url = config.host
        client.connect(url, socketio_path='/socket-game', transports=['websocket'], namespaces=['/game'])
        client.emit('join_room', namespace='/game')
        self.sid = client.get_sid('/game')
        self.players = {}
        self.room = None
        self.color = 1

    def start(self, data):
        self.players = data['players']
        self.room = data['room']
        self.color = self.players[self.sid]

    def update(self, data):
        board = data['board']
        self.board.board = board
        self.is_black = data['is_black']

    @property
    def is_my_turn(self):
        return self.is_black == (self.color == self.board.BLACK)

    def play(self, x, y):
        data = {'room': self.room, 'pos': [x, y]}
        client.emit('play', data=data, namespace='/game')


game_client = GameClient()
