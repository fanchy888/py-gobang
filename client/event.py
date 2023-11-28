import socketio
from client import client
from client.game import online_game


@client.on('*')
def catch_all(event, data):
    pass


@client.on('start', namespace='/game')
def start(data):
    print('game started', data)
    online_game.start(data)


@client.on('update', namespace='/game')
def update(data):
    online_game.update(data)


@client.on('quit', namespace='/game')
def update():
    online_game.quit()



