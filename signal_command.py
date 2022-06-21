from unittest import signals
from bot.strategies.right import PriceReverse
from bot.strategies.left import BollStoch
from bot.market import Sina
from bot.config import config
from bot.notification import DingDing
from jinja2 import Environment, FileSystemLoader, select_autoescape
from talib import EMA, MACD
from bot.graph import candlestick, ma_line, macd_figure
import datetime
import numpy
import plotly.graph_objects as go


def strategy_fatory(name):
    match name:
        case 'PriceReverse':
            return PriceReverse()
        case 'BollStoch':
            return BollStoch()


def draw_image(data, ema20, ema30, ema99):
    x = [v['day'] for v in data]
    xText = [datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M') if k % 8 == 0 else ''
        for k, v in enumerate(x)]
    candle = candlestick(data)
    macd, signal, his = MACD(numpy.array([float(v['close']) for v in res]))
    macd_component = macd_figure(x, macd, signal, his)
    ma20 = ma_line(x, ema20)
    ma30 = ma_line(x, ema30)
    ma99 = ma_line(x, ema99)
    img = go.Figure([candle, ma20, ma30, ma99] + macd_component)
    img.update_layout(
        xaxis=dict(title_text='time', type='category', tickmode='array',
                   tickvals=x, ticktext=xText),
        yaxis=dict(title="Price", anchor="x", domain=[0.27, 0.95]),
        yaxis2=dict(title="MACD", anchor="x", domain=[0.05, 0.23]))
    return img


# init html template
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
template = env.get_template("notice.html")

sina = Sina()
notification = DingDing()
strategies = []
for name in config['strategies']:
    strategies.append(strategy_fatory(name))

symbols = config['symbols']
long_period = config['long_period']
signals = []
for v in symbols:
    chinese = v[0]
    symbol = v[1]
    res = sina.kline(symbol, long_period[1], 120)
    last_price = res[-1:][0]['close']
    for strategy in strategies:
        indication = strategy.indicate(res)
        if indication != 0:
            signals.append({
                'flag': indication,
                'period': long_period[0],
                'indicator': strategy.getReason(indication),
                'symbol': chinese,
                'last': strategy.last,
                'price': last_price
            })
            figure = draw_image(res,
                                EMA(numpy.array([numpy.array(float(v['close']))
                                                 for v in res]), 20),
                                EMA(numpy.array([numpy.array(float(v['close']))
                                                 for v in res]), 30),
                                EMA(numpy.array([numpy.array(float(v['close']))
                                                 for v in res]), 99))
            figure.write_image("{}_{}.jpg".format(
                chinese, str(datetime.date.today())), width=1680, height=900)
if len(signals) > 0:
    res = template.render(signals=signals)
    notification.notify('bot signal', res)
