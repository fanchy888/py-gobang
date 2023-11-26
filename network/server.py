
from gobang.manager import manager
from network import server


@server.event(namespace='/game')
def connect(sid, data):
    print("Connecting", sid)


@server.event(namespace='/game')
def disconnect(sid):
    print("Disconnecting", sid)
    rooms = server.rooms(sid, namespace='/game')
    for r in rooms:
        print(sid, 'leaving room', r)
        server.leave_room(sid, r)


@server.on('*', namespace='/game')
def catch_all(event, sid, data):
    print('?', event, sid, data)
    return event + sid


@server.on('join_room', namespace='/game')
def join(sid):
    room = manager.join_room(sid)
    server.enter_room(sid, room=room, namespace='/game')
    print(sid, room)


@server.on('play', namespace='/game')
def play(sid, data):
    manager.play(sid, data)


