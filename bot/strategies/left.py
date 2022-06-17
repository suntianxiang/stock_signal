from talib import BBANDS, STOCH, MACD
import numpy


class BollStoch:
    last = ''

    def indicate(self, data):
        closes = numpy.array([float(e['close']) for e in data])
        price = float(data[-1:][0]['close'])
        up, _, low = BBANDS(closes, timeperiod=20)
        slowk, slowd = STOCH(numpy.array([float(e['high']) for e in data]),
                             numpy.array([float(e['low']) for e in data]),
                             numpy.array([float(e['close']) for e in data]),
                             fastk_period=14, slowk_period=3, slowd_period=3)
        up = up[-1:][0]
        low = low[-1:][0]
        k = slowk[-1:][0]
        d = slowd[-1:][0]
        self.last = "boll:{}{} stoch:{}{}".format(up, low, k, d)
        if price > up and k >= 80 and d >= 80:
            return -1
        if price < low and k <= 20 and d <= 20:
            return 1
        return 0

    def getReason(self, signal):
        if signal == 1:
            return 'price under boll low and stoch oversell'
        if signal == -1:
            return 'price up boll high and stoch oversell'


class MACDCross:
    last = ''

    def indicate(self, data):
        closes = numpy.array([float(e['close']) for e in data])
        _, _, macdhist = MACD(
            closes, fastperiod=12, slowperiod=26, signalperiod=9)
        last_two = macdhist[-2:]
        if (last_two[0] < 0 and last_two[1] > 0):
            return 1
        if (last_two[0] > 0 and last_two[1] < 0):
            return -1
        return 0

    def getReason(self, signal):
        if signal == 1:
            return 'macd crossover'
        if signal == -1:
            return 'macd crossdown'
