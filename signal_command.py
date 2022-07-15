import time


from bot.market import Binance, Sina
from bot.config import config
from bot.notification import DingDing
from bot.monitor import Monitor
from bot.strategies import strategy_factory

strategies = []
for name in config['strategies']:
    strategies.append(strategy_factory(name))
stocks = config['stocks']
crypto_coins = config['crypto_coins']
sina = Sina()
crypto_coin_market = Binance()
notification = DingDing()
monitor = Monitor(strategies, notification, stocks=stocks,
                  stock_market=sina, crypto_coins=crypto_coins,
                  crypto_coin_market=crypto_coin_market)

while True:
    monitor.run()
    time.sleep(900)
