#!/usr/bin/env python3
from datetime import datetime
import pika
import requests
import json
import time
import os

from dotenv import load_dotenv
load_dotenv()

BITSO_ORDER_BOOK = os.environ.get('BITSO_ORDER_BOOK')
HOST = os.environ.get('HOST')
BOOK = 'btc_mxn'
connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
channel = connection.channel()
channel.queue_declare(queue=f'{BOOK}_price')

try:
    while True:
        response = requests.get(BITSO_ORDER_BOOK + f"?book={BOOK}")
        message = {
            "ask": response.json()['payload']['ask'],  # --> venta
            "bid": response.json()['payload']['bid']  # --> compra
        }
        channel.basic_publish(exchange='',
                              routing_key=f'{BOOK}_price',
                              body=json.dumps(message))

        print(
            f"{datetime.now()} sent ask: {message['ask']}, bid: {message['bid']}")
        time.sleep(1.1)
except:
    connection.close()
