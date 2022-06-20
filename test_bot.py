from bot.market import Sina
from bot.notification import DingDing
from talib import BBANDS, EMA
from bot.graph import candlestick, ma_line
import numpy
import datetime


def draw_image(data, ema20, ema30, ema99):
    figure = candlestick(data)
    scatter20 = ma_line([v['day'] for v in data], ema20)
    scatter30 = ma_line([v['day'] for v in data], ema30)
    scatter99 = ma_line([v['day'] for v in data], ema99)
    figure.add_trace(scatter20)
    figure.add_trace(scatter30)
    figure.add_trace(scatter99)
    return figure


sina = Sina()
res = sina.kline('sz002286', 60, 100)

# closes = [float(e['close']) for e in res]
# up, mid, low = BBANDS(numpy.array(closes), timeperiod=20)
# print(up, mid, low)
figure = draw_image(res,
                    EMA(numpy.array([float(v['close']) for v in res]), 20),
                    EMA(numpy.array([float(v['close']) for v in res]), 30),
                    EMA(numpy.array([float(v['close']) for v in res]), 99)
                    )
res = figure.write_image("{}_{}.webp".format(
    'ttt', str(datetime.date.today())), width=1680, height=900)

# dingding = DingDing()
# res = dingding.notify()
# print(res)
