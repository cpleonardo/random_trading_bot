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
    if data['channel'] == 'orderbook':
        orderbook = data['data']
        print(f"Received {MARKET} orderbook")
        print(orderbook)
    elif data['channel'] == 'trades':
        trades = data['data']
        print(f"Received {MARKET} trades")
        print(trades)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('wss://ws.coinbtr.com')
sio.wait()