from server import server
from server.game import GameServer


class GameRoomController:
    def __init__(self):
        self.rooms = {}

    def generate_room(self):
        n = len(self.rooms)
        name = f'room_{n}'
        self.rooms[name] = GameServer(name)
        return self.rooms[name]

    def dispatch_room(self):
        for r, game in self.rooms.items():
            if not game.full:
                return game

        room = self.generate_room()
        return room

    def join_room(self, sid):
        room = None
        while room is None:
            game = self.dispatch_room()
            room = game.room
            success = game.join(sid)
            if success:
                server.enter_room(sid, room=game.room, namespace='/game')
                print('user joined', room, sid)
                server.emit('joined', data=game.info, room=room, namespace='/game')
            else:
                room = None
        return room

    def leave_room(self, room, sid):
        if room in self.rooms:
            self.rooms[room].drop(sid)
            if not self.rooms[room].players:
                del self.rooms[room]

        server.emit('quit', room=room, namespace='/game')

    def get_game(self, room):
        return self.rooms[room]

    def handle_ready(self, sid, room):
        game = self.rooms[room]
        game.get_ready(sid)
        if game.all_ready():
            print('game start...', room)
            game.start()
            server.emit('start', data=game.info, room=room, namespace='/game')

    def play(self, sid, data):
        room = data['room']
        game = self.get_game(room)
        action_detail = game.play_piece(sid, data['pos'])
        server.emit('update', data=action_detail, room=room, namespace='/game')


controller = GameRoomController()
