import socketio

server = socketio.Server(async_mode='gevent')
app = socketio.WSGIApp(server, socketio_path='/socket-game')

from .server import *
