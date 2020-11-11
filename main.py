from trading_bot import Trading

#  You can create as many Trading objects as you need
bot1 = Trading(book='bch_mxn', delta_time=1, base_amount=0.01, side='sell', staging=True)
bot2 = Trading(book='bch_mxn', delta_time=1, base_amount=0.01, side='buy', staging=True)

bot1.start()
bot2.start()
try:
    while True:
        time.sleep(10)
except:
    bot1.kill()
    bot2.kill()
    print('Bye--Bye!')