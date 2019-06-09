#!/usr/bin/env python3

import json, time, requests, threading, random, pika, os


class Trading():
    BITSO_ORDER_BOOK = "https://api.bitso.com/v3/ticker/"
    BASE_URL = 'https://api.staging.coinbtr.com/api/v1/trading/'
    ACCESS_TOKEN = os.environ.get('CBTR_API_KEY')

    def __init__(self, book, delta_time, base_amount, side):
        self.book = book
        self.base_amount = base_amount
        self.delta_time = delta_time
        self.side = side
        self.ask, self.bid = self.get_bitso_ticker()
        self.order_placer = threading.Thread(target=self.bot)
        self.subscriber = threading.Thread(target=self.subscribe_price)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
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

# seller_bots = [
#     Trading(book='btc_mxn', delta_time=1, base_amount=0.001, side='sell')] * 3
# buyer_bots = [
#     Trading(book='btc_mxn', delta_time=1, base_amount=0.001, side='buy')] * 3
bot1 = Trading(book='btc_mxn', delta_time=1, base_amount=0.001, side='sell')
bot2 = Trading(book='btc_mxn', delta_time=1, base_amount=0.001, side='buy')

bot1.start()
bot2.start()
try:
    # [bot.start() for bot in seller_bots]
    # [bot.start() for bot in buyer_bots]
    while True:
        time.sleep(10)
except:
    # for bot in seller_bots:
    #     bot.kill()
    # for bot in buyer_bots:
    #     bot.kill()
    bot1.kill()
    bot2.kill()
    print('Bye--Bye!')
