from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import socketio, time
server = socketio.Server(async_mode='gevent')
app = socketio.WSGIApp(server, socketio_path='/socket-game')


@server.event(namespace='/game')
def connect(sid, data):
    print("Connecting", sid,time.time())


@server.event(namespace='/game')
def disconnect(sid):
    print("Disconnecting", sid,time.time())


@server.event(namespace='/game')
def ping(sid, data):
    print('ping', sid, data, time.time())


@server.on('*', namespace='/game')
def catch_all(event, sid, data):
    print('?', event, sid, data,time.time())
    return event + sid


if __name__ == '__main__':
    pywsgi.WSGIServer(('0.0.0.0', 5555), app, handler_class=WebSocketHandler).serve_forever()
