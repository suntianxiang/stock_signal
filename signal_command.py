from unittest import signals
from bot.strategies.right import PriceReverse
from bot.strategies.left import BollStoch
from bot.market import Sina
from bot.config import config
from bot.notification import DingDing
from jinja2 import Environment, FileSystemLoader, select_autoescape


def strategy_fatory(name):
    match name:
        case 'PriceReverse':
            return PriceReverse()
        case 'BollStoch':
            return BollStoch()


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
if len(signals) > 0:
    res = template.render(signals=signals)
    notification.notify('bot signal', res)
