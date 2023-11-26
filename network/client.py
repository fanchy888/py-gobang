import socketio
import time


def func1(*args):
    print(args)


if __name__ == '__main__':
    url = 'http://localhost:5555'
    client = socketio.Client(logger=True)

    client.connect(url, socketio_path='/socket-game', transports=['websocket'], namespaces=['/game'])
    a = 'test'
    client.emit('ping', {'event': a}, namespace='/game')
    print(time.time())
    while a != 'esc':
        a = input()
        s = client.emit(a, namespace='/game')
    time.sleep(1)
    client.disconnect()
