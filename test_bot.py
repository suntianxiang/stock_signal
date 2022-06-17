from bot.market import Sina
from bot.notification import DingDing
from talib import BBANDS
import numpy

sina = Sina()
res = sina.kline('sz002286', 60, 20)
print(res)

closes = [float(e['close']) for e in res]
up, mid, low = BBANDS(numpy.array(closes), timeperiod=20)
print(up, mid, low)

# dingding = DingDing()
# res = dingding.notify()
# print(res)
