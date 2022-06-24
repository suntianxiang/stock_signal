import time


from bot.market import Sina
from bot.config import config
from bot.notification import DingDing
from bot.monitor import Monitor
from bot.strategies import strategy_factory

strategies = []
for name in config['strategies']:
    strategies.append(strategy_factory(name))
symbols = config['symbols']
sina = Sina()
notification = DingDing()
monitor = Monitor(symbols, sina, strategies, notification)

while True:
    monitor.run()
    time.sleep(3600)
