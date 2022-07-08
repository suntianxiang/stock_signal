from bot.market import Sina
from bot.notification import DingDing
from talib import RSI
from bot.graph import candlestick, line, rsi as rsi_img
import numpy
import datetime
import plotly.graph_objects as go

sina = Sina()
res = sina.kline('sz002286', 60, 100)
x = [v['day'] for v in res]
xText = [datetime.datetime.strptime(
    v, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M') if k % 8 == 0 else ''
    for k, v in enumerate(x)]
closes = numpy.array([float(v['close']) for v in res])
high = numpy.array([float(v['high']) for v in res])
low = numpy.array([float(v['low']) for v in res])

candle = candlestick(res)
rsi = RSI(closes, 20)
r = rsi_img(x, rsi)
img = go.Figure([candle] + r)
img.update_layout(
    xaxis=dict(title_text='time', type='category', tickmode='array',
               tickvals=x, ticktext=xText),
    yaxis=dict(title="Price", anchor="x", domain=[0.5, 0.99]),
    yaxis2=dict(title="MACD", anchor="x", domain=[0.00, 0.12]),
    yaxis3=dict(title="Volume", anchor="x", domain=[0.13, 0.23]),
    yaxis4=dict(title="Stoch", anchor="x", domain=[
                0.24, 0.36]),
    yaxis5=dict(title="RSI", anchor="x", domain=[0.37, 0.48]),)
res = img.write_image("{}_{}.webp".format(
    'ttt', str(datetime.date.today())), width=1680, height=900)
