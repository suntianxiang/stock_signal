from cmath import isnan, nan
from bot.graph import candlestick, line, macd_figure, vol_figure
from bot.graph import rsi as rsi_img
from talib import EMA, MACD, BBANDS, SMA, set_unstable_period, STOCH, RSI
import numpy
import datetime
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader, select_autoescape

from bot.ta import chandelier_exit


class Monitor:
    """
    Finance Monitor
        strategies: a list of strategies we care
        stocks: a list of stocks symbol like [code, 'chinese']
        stock_market: Market we use, the source of kline for stock
        cryptocurrency: a list of cryto coins we care
        crypto_coin_market: the source of kline for cryptocurreny
        notification: tool to notify you
        template: html template engine, we use jinja2
        times: How times the monitor run
    """
    strategies = []
    stocks = []
    stock_market = None
    cryptocurrency = []
    crypto_coin_market = None
    notification = None
    template = None
    times = 0

    def __init__(self, strategies, notification, stocks=[], stock_market=None,
                 cryptocurrency=[], crypto_coin_market=None) -> None:
        self.stock_market = stock_market
        self.strategies = strategies
        self.stocks = stocks
        self.stock_market = stock_market
        self.cryptocurrency = cryptocurrency
        self.notification = notification
        self.crypto_coin_market = crypto_coin_market
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape()
        )
        self.template = env.get_template("notice.html")
        set_unstable_period('ALL', 50)

    # start monitor
    def run(self):
        dt = datetime.datetime.now()
        if ((dt.minute > 30 and dt.hour == 9) or dt.hour >= 10) and \
                ((dt.minute < 30 and dt.hour == 15) or dt.hour < 15):
            self.monitor_stock()
        # self.monitor_cryptocurrency()

    # monitor stock market
    def monitor_stock(self):
        dt = datetime.datetime.now()
        signals = []
        if dt.minute < 30 or dt.minute > 50 and self.times != 0:
            return
        for v in self.stocks:
            chinese = v[0]
            symbol = v[1]
            res = self.stock_market.kline(
                symbol, self.stock_market.long_period, 120)
            tmpSignals = self.technical_analysis(
                chinese, res, period=self.stock_market.long_period)
            if len(tmpSignals) > 0:
                signals = signals + tmpSignals
        if len(signals) > 0:
            res = self.template.render(signals=signals)
            self.notification.notify('bot signal', res)
        self.times = 1

    # monitor cryptocurrency market
    def monitor_cryptocurrency(self):
        signals = []
        for v in self.cryptocurrency:
            chinese = v[0]
            symbol = v[1]
            res = self.crypto_coin_market.kline(
                symbol, self.crypto_coin_market.micro_period, 120)
            tmpSignals = self.technical_analysis(
                chinese, res, period=self.crypto_coin_market.micro_period)
            if len(tmpSignals) > 0:
                signals = signals + tmpSignals
        if len(signals) > 0:
            res = self.template.render(signals=signals)
            self.notification.notify('bot signal', res)

    def technical_analysis(self, chinese, kline, period=''):
        """
        start technical analysis from kline

            chinese: symbols translation
            kline: kline data
            period: kline period
        """
        signals = []
        last_price = kline[-1:][0]['close']
        img_components = []
        for strategy in self.strategies:
            indication = strategy.indicate(kline)
            if indication != 0:
                signals.append({
                    'flag': indication,
                    'period': period,
                    'indicator': strategy.getReason(indication),
                    'symbol': chinese,
                    'last': strategy.last,
                    'price': last_price
                })
                img_components += strategy.getImgComponent()
        if len(signals) > 0:
            figure = self.draw_image(
                kline,
                ema='ema' in img_components,
                macd='macd' in img_components,
                boll='boll' in img_components,
                STOCHCOMPONENT='stoch' in img_components,
                CE='ce' in img_components,
                rsi='rsi' in img_components)
            figure.write_image("{}_{}.jpg".format(
                chinese, str(datetime.date.today())),
                width=1680, height=900)
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

    def draw_image(self, data, ema=False, macd=False,
                   boll=False, CE=False, STOCHCOMPONENT=False, rsi=False):
        img_data = []
        closes = numpy.array([float(v['close']) for v in data])
        high = numpy.array([float(v['high']) for v in data])
        low = numpy.array([float(v['low']) for v in data])

        x = [v['day'] for v in data]
        candle = candlestick(data)
        img_data.append(candle)
        if ema:
            ema20 = EMA(closes, 20)
            ema40 = EMA(closes, 40)
            ema99 = EMA(closes, 99)
            ma20 = line(x, ema20, 'ema20')
            ma40 = line(x, ema40, 'ema40')
            ma99 = line(x, ema99, 'ema99')
            img_data = img_data + [ma20, ma40, ma99]
        if macd:
            macd, signal, his = MACD(closes)
            macd_component = macd_figure(x, macd, signal, his, yaxis="y2")
            img_data = img_data + macd_component
        if boll:
            up, mid, low = BBANDS(closes, timeperiod=20)
            boll = [line(x, up, 'up'), line(
                x, mid, 'mid'), line(x, low, 'low')]
            img_data = img_data + boll
        if CE:
            ce = chandelier_exit(closes, high, low)
            for k, v in enumerate(ce['trend']):
                if ce['trend'][k] == 0:
                    continue
                if ce['trend'][k] == 1:
                    ce['low'][k] = nan
                elif ce['trend'][k] == -1:
                    ce['high'][k] = nan
            h = line(x, ce['high'], 'ce_high')
            ll = line(x, ce['low'], 'ce_low')
            img_data += [h, ll]
        if STOCHCOMPONENT:
            slowk, slowd = STOCH(high, low, closes, fastk_period=14)
            img_data += [line(x, slowk, 'stochK', yaxis="y4"),
                         line(x, slowd, 'stochD', yaxis="y4")]
            pass
        if rsi:
            rsi_v = RSI(closes, 20)
            img_data += rsi_img(x, rsi_v)
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
            yaxis=dict(title="Price", anchor="x", domain=[0.5, 0.99]),
            yaxis2=dict(title="MACD", anchor="x", domain=[0.00, 0.12]),
            yaxis3=dict(title="Volume", anchor="x", domain=[0.13, 0.23]),
            yaxis4=dict(title="Stoch", anchor="x", domain=[0.24, 0.36]),
            yaxis5=dict(title="RSI", anchor="x", domain=[0.37, 0.48]),
        )
        return img
