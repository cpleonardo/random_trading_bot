#!/usr/bin/env python3

import json, time, requests, threading, random, os


class Trading():
    BITSO_ORDER_BOOK = "https://api.bitso.com/v3/ticker/"
    BASE_URL = 'https://api.coinbtr.com/api/v1/trading/'
    ACCESS_TOKEN = os.environ.get('CBTR_API_KEY')

    def __init__(self, book, delta_time, base_amount, side):
        self.book = book
        self.base_amount = base_amount
        self.delta_time = delta_time
        self.side = side
        self.ask, self.bid = self.get_bitso_ticker()
        self.order_placer = threading.Thread(target=self.bot)

    def place_order(self, amount, price, side, type='limit'):
        headers = {
            'Authorization': f'Token {self.ACCESS_TOKEN}',
            'Content-Type': 'application/json',
        }
        body = {
            'amount': amount,
            'price': price,
            'market': self.book.replace('_', '-'),
            'type': type,
            'side': self.side,
        }
        response = requests.post(
            url=self.BASE_URL+'placeorder/',
            headers=headers,
            data=json.dumps(body),
        )
        try:
            print(response.content)
            return response.json()['data']['id']
        except:
            return 0

    def close_order(self, order_id):
        headers = {
            'Authorization': f'Token {self.ACCESS_TOKEN}',
            'Content-Type': 'application/json',
        }
        body = {
            'id': order_id,
        }
        response = requests.post(
            url=self.BASE_URL+'closeorder/',
            headers=headers,
            data=json.dumps(body),
        )
        print(response.json())

    def get_bitso_ticker(self):
        response = requests.get(self.BITSO_ORDER_BOOK + f"?book={self.book}")
        orders = response.json()
        ask = orders['payload']['ask']  # --> venta
        bid = orders['payload']['bid']  # --> compra
        return ask, bid

    def bot(self):
        while True:
            self.ask, self.bid = self.get_bitso_ticker()            
            price_inc = round(random.uniform(0, 10), 2)
            if self.side == 'buy':
                price = float(self.bid) - price_inc
            else:
                price = float(self.ask)*1.01 + price_inc
            amount_inc = round(random.uniform(-0.001, 0.001), 8)
            amount = self.base_amount + amount_inc
            order_id = self.place_order(
                amount=amount, price=price, side='buy')
            time.sleep(self.delta_time)
            if order_id:
                self.close_order(order_id)

    def start(self):
        self.order_placer.start()

    def kill(self):
        self.order_placer.daemon = False

# You can create as many Trading objects as you need
bot1 = Trading(book='btc_mxn', delta_time=10, base_amount=0.1, side='sell')
bot2 = Trading(book='btc_mxn', delta_time=3, base_amount=0.01, side='sell')

bot1.start()
bot2.start()
try:
    while True:
        time.sleep(10)
except:
    bot1.kill()
    bot2.kill()
    print('Bye--Bye!')
