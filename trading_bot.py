#!/usr/bin/env python3

import json
import time
import requests
import threading
import random
import pika
import os
from dotenv import load_dotenv
from tauros_api import TaurosAPI


load_dotenv()
tauros = TaurosAPI(os.environ.get('TAUROS_API_KEY'), os.environ.get('TAUROS_SECRET'), staging=True)


class Trading():
    BITSO_ORDER_BOOK = os.environ.get('BITSO_ORDER_BOOK')
    HOST = os.environ.get('HOST')
    API_VERSION = 'api/v1/'

    def __init__(self, book, delta_time, base_amount, side):
        self.book = book
        self.base_amount = base_amount
        self.delta_time = delta_time
        self.side = side
        self.ask, self.bid = self.get_bitso_ticker()
        self.order_placer = threading.Thread(target=self.bot)
        self.subscriber = threading.Thread(target=self.subscribe_price)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=f'{self.book}_price')
        self.channel.basic_consume(queue=f'{self.book}_price',
                                   auto_ack=True,
                                   on_message_callback=self.set_price_callback)

    def set_price_callback(self, ch, method, properties, body):
        message = json.loads(body)
        self.ask = message.get('ask')
        self.bid = message.get('bid')
        print(" [x] Received %r" % message)

    def place_order(self, amount, price, side, type='limit'):
        body = {
            'amount': amount,
            'price': price,
            'market': self.book.replace('_', '-'),
            'type': type,
            'side': self.side,
        }
        try:
            response = tauros.post(
                path='/{}trading/placeorder/'.format(self.API_VERSION),
                data=body,
            )
            print(response.body.get('msg'))
            return response.body.get('data').get('id')
        except Exception as e:
            print(e)
            return 0

    def close_order(self, order_id):
        response = tauros.post(
            path='/{}trading/closeorder/'.format(self.API_VERSION),
            data={
                'id': order_id,
            },
        )
        print("{} Id -> {}".format(response.body.get('msg'), order_id) )

    def get_bitso_ticker(self):
        response = requests.get(self.BITSO_ORDER_BOOK + f"?book={self.book}")
        orders = response.json()
        ask = orders['payload']['ask']  # --> venta
        bid = orders['payload']['bid']  # --> compra
        return ask, bid

    def bot(self):
        while True:
            price_inc = round(random.uniform(0, 10), 2)
            if self.side == 'buy':
                price = float(self.bid) - price_inc
            else:
                price = float(self.ask) + price_inc
            amount_inc = round(random.uniform(-0.001, 0.001), 8)
            amount = self.base_amount + amount_inc
            order_id = self.place_order(
                amount=amount, price=price, side='buy')
            time.sleep(self.delta_time)
            if order_id:
                self.close_order(order_id)

    def subscribe_price(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def start(self):
        self.order_placer.start()
        self.subscriber.start()

    def kill(self):
        self.order_placer.daemon = False
        self.subscriber.daemon = False
        self.connection.close()


# You can create as many Trading objects as you need
bot1 = Trading(book='bch_mxn', delta_time=1, base_amount=0.01, side='sell')
bot2 = Trading(book='bch_mxn', delta_time=1, base_amount=0.01, side='buy')

bot1.start()
bot2.start()
try:
    while True:
        time.sleep(10)
except:
    bot1.kill()
    bot2.kill()
    print('Bye--Bye!')
