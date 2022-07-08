from cmath import isnan, nan
from bot.market import Sina
from bot.indicators import chandelier_exit
import numpy
from bot.graph import candlestick, line
import plotly.graph_objects as go
import datetime
from talib import set_unstable_period
set_unstable_period('ALL', 40)

sina = Sina()
res = sina.kline('sz002286', 60, 100)
ce = chandelier_exit(numpy.array([float(v['close']) for v in res]),
                     numpy.array([float(v['high']) for v in res]),
                     numpy.array([float(v['low']) for v in res]))
x = [v['day'] for v in res]
xText = [datetime.datetime.strptime(
    v, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M') if k % 8 == 0 else ''
    for k, v in enumerate(x)]
c = candlestick(res)
for k, v in enumerate(ce['high']):
    if isnan(ce['high'][k]):
        continue
    if ce['trend'][k] == 1:
        ce['low'][k] = nan
    elif ce['trend'][k] == -1:
        ce['high'][k] = nan
h = line(x, ce['high'], 'high')
ll = line(x, ce['low'], 'low')
img = go.Figure([c, h, ll])
img.update_layout(
    xaxis=dict(title_text='time', type='category', tickmode='array',
               tickvals=x, ticktext=xText),
    yaxis=dict(title="Price", anchor="x", domain=[0.27, 0.95]),
    yaxis2=dict(title="MACD", anchor="x", domain=[0.05, 0.23]))

img.show()
