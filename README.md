# py-gobang
A gobang game in python

## server
```python -m server.run_server```

serve with gunicorn gevent

```gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 127.0.0.1:5555 server:app```

## client
``` python -m client.run_client```
