import socketio

client = socketio.Client(logger=True)

from .event import *
