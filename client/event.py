import socketio
from client import client
from client.game import game_client


@client.on('*')
def catch_all(event, data):
    pass


@client.on('start', namespace='/game')
def start(data):
    print('game started', data)
    game_client.start(data)


@client.on('update', namespace='/game')
def update(data):
    game_client.update(data)





