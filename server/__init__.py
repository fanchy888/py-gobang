import socketio

server = socketio.Server(async_mode='gevent', cors_allowed_origins=['*'])
app = socketio.WSGIApp(server, socketio_path='/socket-game')

from .event import *
