from server import server
from server.controller import controller


@server.event(namespace='/game')
def connect(sid, data):
    print("Connecting", sid)


@server.event(namespace='/game')
def disconnect(sid):
    print("Disconnecting", sid)
    rooms = server.rooms(sid, namespace='/game')
    for r in rooms:
        controller.leave_room(r, sid)
        print(sid, 'leaving room', r)
        server.leave_room(sid, r)


@server.on('*', namespace='/game')
def catch_all(event, sid, data):
    print('?', event, sid, data)
    return event + sid


@server.on('join_room', namespace='/game')
def join(sid):
    room = controller.join_room(sid)
    print('user joined', room, sid)


@server.on('play', namespace='/game')
def play(sid, data):
    controller.play(sid, data)


