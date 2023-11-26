from gobang.game_servier import GameServer
from network import server


class GameManager:
    def __init__(self):
        self.rooms = {}

    def generate_room(self):
        n = len(self.rooms)
        name = f'room_{n}'
        self.rooms[name] = GameServer(name)
        return self.rooms[name]

    def join_room(self, sid):
        for r, game in self.rooms.items():
            if game.member_count < 2:
                game.join(sid)
                return r

        game = self.generate_room()
        game.join(sid)
        return game.room

    def get_game(self, room):
        return self.rooms[room]

    def play(self, sid, data):
        room = data['room']
        game = self.get_game(room)
        game.move(sid, data)
        server.emit('update_board', data=game.info, room=room, namespace=game.namespace)


manager = GameManager()
