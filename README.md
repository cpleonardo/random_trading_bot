# Random trading bot
Random trading bot for placing and cancelling limit orders

Bitcoin price is queried from Bitso.

## Requirements
* Python 3
* [Virtualenv >16.1.0](https://virtualenv.pypa.io/en/latest/)

## Create virtual environment
```
      $ ➜ virtualenv -p python3 env
      $ ➜ source env/bin/activate
 (env)$ ➜ pip install -r requirements.txt
```

## Set your access token in your environment
```
(env)$ ➜ export CBTR_API_KEY=your_access_token
```

## Launch "bot"
Open another terminal and source the python virtual environment.
```
(env)$ ➜ python3 trading_bot.py
```

