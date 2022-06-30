from bot.graph import candlestick, ma_line, macd_figure, vol_figure
from talib import EMA, MACD, BBANDS, SMA, set_unstable_period
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
    lastMinutes = 0

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
        set_unstable_period('ALL', 50)

    def run(self):
        dt = datetime.datetime.now()
        minutes = int(int(dt.strftime('%M'))/10)
        signals = []
        for v in self.symbols:
            chinese = v[0]
            symbol = v[1]
            if self.lastMinutes != minutes and minutes == 3:
                res = self.market.kline(symbol, self.market.long_period, 120)
                tmpSignals = self.technical_analysis(chinese, res)
                if len(tmpSignals) > 0:
                    signals = signals + tmpSignals
            res = self.market.kline(symbol, self.market.micro_period, 20)
            volSignals = self.vol_watch(chinese, res)
            if len(volSignals) > 0:
                signals = signals + volSignals
        if len(signals) > 0:
            res = self.template.render(signals=signals)
            self.notification.notify('bot signal', res)
        self.lastMinutes = minutes

    def technical_analysis(self, chinese, kline):
        signals = []
        last_price = kline[-1:][0]['close']
        for strategy in self.strategies:
            indication = strategy.indicate(kline)
            if indication != 0:
                figure = self.draw_image(kline)
                figure.write_image("{}_{}.jpg".format(
                    chinese, str(datetime.date.today())),
                    width=1680, height=900)
                signals.append({
                    'flag': indication,
                    'period': self.market.long_period,
                    'indicator': strategy.getReason(indication),
                    'symbol': chinese,
                    'last': strategy.last,
                    'price': last_price
                })
        return signals

    # watch volume change
    def vol_watch(self, chinese, kline):
        signals = []
        volumes = [float(v['volume']) for v in kline]
        lastFive = volumes[-6:-1]
        last = volumes[-1:][0]
        sma = SMA(numpy.array(lastFive), 5)
        if last > 2.8 * sma[-1:][0]:
            signals.append({
                'flag': 1,
                'period': self.market.micro_period,
                'indicator': 'VolumeGreatThanTripleSMA5',
                'symbol': chinese,
                'last': last,
                'price': ''
            })
        return signals

    def draw_image(self, data, ema=True, macd=True, boll=True):
        img_data = []
        closes = numpy.array([float(v['close']) for v in data])
        x = [v['day'] for v in data]
        candle = candlestick(data)
        img_data.append(candle)
        if ema:
            ema20 = EMA(closes, 20)
            ema30 = EMA(closes, 30)
            ema99 = EMA(closes, 99)
            ma20 = ma_line(x, ema20, 'ema20')
            ma30 = ma_line(x, ema30, 'ema30')
            ma99 = ma_line(x, ema99, 'ema99')
            img_data = img_data + [ma20, ma30, ma99]
        if macd:
            macd, signal, his = MACD(closes)
            macd_component = macd_figure(x, macd, signal, his)
            img_data = img_data + macd_component
        if boll:
            up, mid, low = BBANDS(closes, timeperiod=20)
            boll = [ma_line(x, up, 'up'), ma_line(
                x, mid, 'mid'), ma_line(x, low, 'low')]
            img_data = img_data + boll
        vol = vol_figure(x, numpy.array([float(v['volume']) for v in data]))
        img_data.append(vol)
        img = go.Figure(img_data)
        xText = [datetime.datetime.strptime(
            v, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M') if k % 8 == 0
            else '' for k, v in enumerate(x)]
        img.update_layout(
            xaxis_rangeslider_visible=False,
            xaxis=dict(title_text='time', type='category', tickmode='array',
                       tickvals=x, ticktext=xText),
            yaxis=dict(title="Price", anchor="x", domain=[0.27, 0.95]),
            yaxis2=dict(title="MACD", anchor="x", domain=[0.00, 0.12]),
            yaxis3=dict(title="Volume", anchor="x", domain=[0.13, 0.23]))
        return img
