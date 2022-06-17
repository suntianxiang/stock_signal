from bot.graph import candlestick, ma_line, macd_figure
from talib import EMA, MACD, BBANDS
import numpy
import datetime
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader, select_autoescape


class Monitor:
    market = None
    strategies = []
    symbols = []
    notification = None
    template = None

    def __init__(self, symbols, market, strategies, notification) -> None:
        self.market = market
        self.strategies = strategies
        self.symbols = symbols
        self.notification = notification
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape()
        )
        self.template = env.get_template("notice.html")

    def run(self):
        signals = []
        for v in self.symbols:
            chinese = v[0]
            symbol = v[1]
            res = self.market.kline(symbol, self.market.long_period, 120)
            last_price = res[-1:][0]['close']
            for strategy in self.strategies:
                indication = strategy.indicate(res)
                if indication != 0:
                    signals.append({
                        'flag': indication,
                        'period': self.market.long_period,
                        'indicator': strategy.getReason(indication),
                        'symbol': chinese,
                        'last': strategy.last,
                        'price': last_price
                    })
                    figure = self.draw_image(res)
                    figure.write_image("{}_{}.jpg".format(
                        chinese, str(datetime.date.today())),
                        width=1680, height=900)
        if len(signals) > 0:
            res = self.template.render(signals=signals)
            self.notification.notify('bot signal', res)

    def draw_image(self, data):
        closes = numpy.array([float(v['close']) for v in data])
        x = [v['day'] for v in data]
        xText = [datetime.datetime.strptime(
            v, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M') if k % 8 == 0
            else '' for k, v in enumerate(x)]
        ema20 = EMA(closes, 20)
        ema30 = EMA(closes, 30)
        ema99 = EMA(closes, 99)
        macd, signal, his = MACD(closes)
        up, mid, low = BBANDS(closes, timeperiod=20)
        candle = candlestick(data)
        macd_component = macd_figure(x, macd, signal, his)
        ma20 = ma_line(x, ema20)
        ma30 = ma_line(x, ema30)
        ma99 = ma_line(x, ema99)
        boll = [ma_line(x, up, 'up'), ma_line(
            x, mid, 'mid'), ma_line(x, low, 'low')]
        img = go.Figure([candle, ma20, ma30, ma99] + macd_component + boll)
        img.update_layout(
            xaxis=dict(title_text='time', type='category', tickmode='array',
                       tickvals=x, ticktext=xText),
            yaxis=dict(title="Price", anchor="x", domain=[0.27, 0.95]),
            yaxis2=dict(title="MACD", anchor="x", domain=[0.05, 0.23]))
        return img
