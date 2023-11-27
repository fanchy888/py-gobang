from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from server import app


if __name__ == '__main__':
    pywsgi.WSGIServer(('0.0.0.0', 5555), app, handler_class=WebSocketHandler).serve_forever()
