# Random trading bot
Random trading bot for placing and cancelling limit orders

Bitcoin price is queried from Bitso.

## Requirements
* [RabbitMQ Server](https://www.rabbitmq.com/)
* Python 3
* [Virtualenv >16.1.0](https://virtualenv.pypa.io/en/latest/)

## Install RabbitMQ Server
```sh
      $ ➜ docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Install VirtualEnv
```sh
      $ ➜ sudo apt install python3-venv
```

## Create virtual environment
```sh
      $ ➜ python3 -m venv env
      $ ➜ source env/bin/activate
      (env) $ ➜ pip install -r requirements.txt
```

## Copy .env.example to .env and Edit
```sh
   cp .env.example .env
```

## Launch Bitcoin price publisher
```
(env)$ ➜ python btc_price_pub.py
```
or
```
(env)$ ➜ ./btc_price_pub.py
```


## Launch "bot"
Open another terminal and source the python virtual environment.
```
(env)$ ➜ python trading_bot.py
```
or
```
(env)$ ➜ ./trading_bot.py
```

