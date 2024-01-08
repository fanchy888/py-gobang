import time

from ai_player.ai_game import StateBoard
from ai_player.mcts_player import MCTSPlayer, init_ai_player
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

    def wait(self):
        return

    @property
    def started(self):
        return self.state == self.STARTED

    @property
    def is_my_turn(self):
        return self.started and self.is_black == (self.color == Board.BLACK)

    @property
    def winner(self):
        return self.board.winner


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
        self.board.last = [x, y]
        self.is_black = data['is_black']

        valid = self.board.play_piece(x, y, color)
        if valid:
            self.board.update_score(x, y, color)

        if self.board.winner:
            client.emit('finish', data=self.room, namespace='/game')
            self.state = self.END

    def play(self, x, y):
        if self.started and self.board.board[x][y] == 0:
            data = {'room': self.room, 'pos': [x, y]}
            client.emit('play', data=data, namespace='/game')


class SingleGameClient(BaseGameClient):
    def __init__(self):
        super().__init__()
        self.state_board = None
        self.AI_player = None
        self.wait_for_ai = False

    def make_init(self):
        self.state_board = StateBoard(width=config.rule, height=config.rule, n_in_row=5)
        self.state_board.init_board()
        self.AI_player = init_ai_player(config.rule, config.rule)

    def ready(self):
        self.state = self.READY
        self.make_init()
        self.start(1)

    def play(self, x, y):
        if self.is_my_turn:

            valid = self.board.play_piece(x, y, self.color)
            if valid:
                self.board.update_score(x, y, self.color)
            else:
                return
            self.check_winner()

            self.is_black = not self.is_black
            move = x * config.rule + y
            self.state_board.do_move(move)
            self.wait_for_ai = True

    def wait(self):
        if self.wait_for_ai:
            self.ai_play()

    def reset(self):
        self.state_board = None
        self.AI_player = None
        self.wait_for_ai = False
        super().reset()

    def ai_play(self):
        if not self.is_my_turn and self.wait_for_ai:
            print('ai playing...')
            self.wait_for_ai = False
            move = self.AI_player.get_action(self.state_board)
            x = move // config.rule
            y = move % config.rule
            ai_color = 2
            self.board.play_piece(x, y, ai_color)
            self.board.update_score(x, y, ai_color)
            self.check_winner()
            self.state_board.do_move(move)
            self.is_black = not self.is_black

    def check_winner(self):
        if self.board.winner:
            self.state = self.END



online_game = OnlineGameClient()
local_game = SingleGameClient()
