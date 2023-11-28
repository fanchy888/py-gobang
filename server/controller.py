from server import server
from server.game import GameServer


class GameServerController:
    def __init__(self):
        self.rooms = {}

    def generate_room(self):
        n = len(self.rooms)
        name = f'room_{n}'
        self.rooms[name] = GameServer(name)
        return self.rooms[name]

    def _join_room(self, sid):
        for r, game in self.rooms.items():
            if game.member_count < 2:
                game.join(sid)
                return r

        game = self.generate_room()
        game.join(sid)
        return game.room

    def join_room(self, sid):
        room = self._join_room(sid)
        server.enter_room(sid, room=room, namespace='/game')
        if self.rooms[room].member_count == 2:
            self.start(room)
        return room

    def leave_room(self, room, sid):
        if room in self.rooms:
            self.rooms[room].drop(sid)
            if self.rooms[room].member_count == 0:
                del self.rooms[room]

        server.emit('quit', room=room, namespace='/game')

    def get_game(self, room):
        return self.rooms[room]

    def start(self, room):
        game = self.rooms[room]
        print('game start...', room)
        server.emit('start', data=game.info, room=room, namespace='/game')

    def play(self, sid, data):
        room = data['room']
        game = self.get_game(room)
        game.move(sid, data['pos'])
        server.emit('update', data=game.board_detail, room=room, namespace='/game')


controller = GameServerController()
