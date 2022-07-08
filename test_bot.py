from bot.market import Sina
from bot.notification import DingDing
from talib import BBANDS, EMA, MACD
from bot.graph import candlestick, line, macd_figure
import numpy
import datetime
import plotly.graph_objects as go

sina = Sina()
res = sina.kline('sz002286', 60, 100)

# closes = [float(e['close']) for e in res]
# up, mid, low = BBANDS(numpy.array(closes), timeperiod=20)
# print(up, mid, low)
x = [v['day'] for v in res]
xText = [datetime.datetime.strptime(
    v, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M') if k % 8 == 0 else ''
    for k, v in enumerate(x)]
closes = [float(v['close']) for v in res]
candlestick = candlestick(res)
ma20 = line(x, EMA(numpy.array(closes), 20), name='ma20')
ma30 = line(x, EMA(numpy.array(closes), 30), name='ma30')
ma99 = line(x, EMA(numpy.array(closes), 99), name='ma99')

macd, signal, his = MACD(numpy.array([float(v['close']) for v in res]))
macd_component = macd_figure(x, macd, signal, his)

# dingding = DingDing()
# res = dingding.notify()
# print(res)
img = go.Figure([candlestick, ma20, ma30, ma99] + macd_component)
img.update_layout(
    xaxis=dict(title_text='time', type='category', tickmode='array',
               tickvals=x, ticktext=xText),
    yaxis=dict(title="Price", anchor="x", domain=[0.27, 0.95]),
    yaxis2=dict(title="MACD", anchor="x", domain=[0.05, 0.23]))
res = img.write_image("{}_{}.webp".format(
    'ttt', str(datetime.date.today())), width=1680, height=900)
