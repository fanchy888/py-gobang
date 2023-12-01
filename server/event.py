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
    controller.join_room(sid)


@server.on('ready', namespace='/game')
def ready(sid, room):
    controller.handle_ready(sid, room)


@server.on('play', namespace='/game')
def play(sid, data):
    controller.play(sid, data)


@server.on('finish', namespace='/game')
def finish(sid, room):
    controller.finish(room)
