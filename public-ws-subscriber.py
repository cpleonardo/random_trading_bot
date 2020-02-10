import socketio
sio = socketio.Client()
MARKET = "BTC-MXN"

@sio.event
def connect():
    print('connection established')
    print(f'subscribing to {MARKET} market')
    sio.emit('subscribe', MARKET)

@sio.on('message')
def message_handler(data):
    print('message received with ', data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('wss://ws.coinbtr.com')
sio.wait()