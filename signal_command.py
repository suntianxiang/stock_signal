from unittest import signals
from bot.strategies.right import PriceReverse
from bot.strategies.left import BollStoch
from bot.market import Sina
from bot.config import config
from bot.notification import DingDing
from jinja2 import Environment, FileSystemLoader, select_autoescape
from talib import EMA
from bot.graph import candlestick, ma_line
import datetime


def strategy_fatory(name):
    match name:
        case 'PriceReverse':
            return PriceReverse()
        case 'BollStoch':
            return BollStoch()


def draw_image(data, ema20, ema30, ema99):
    figure = candlestick(data)
    scatter20 = ma_line([v['day'] for v in data], ema20)
    scatter30 = ma_line([v['day'] for v in data], ema30)
    scatter99 = ma_line([v['day'] for v in data], ema99)
    figure.add_trace(scatter20)
    figure.add_trace(scatter30)
    figure.add_trace(scatter99)
    return figure


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
    figure = draw_image(res, EMA([v['close'] for v in res], 20), EMA(
        [v['close'] for v in res], 30), EMA([v['close'] for v in res], 99))
    figure.write_image("{}_{}.webp".format(
        chinese, str(datetime.date.today())))
if len(signals) > 0:
    res = template.render(signals=signals)
    notification.notify('bot signal', res)
