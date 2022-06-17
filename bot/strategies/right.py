from talib import EMA
import numpy

# price reverse strategy according to ema


class PriceReverse:
    last = ''

    def indicate(self, data):
        closes = numpy.array([float(e['close']) for e in data])
        ema20 = EMA(closes, 20)
        ema30 = EMA(closes, 30)
        ema99 = EMA(closes, 99)
        lastEma20 = ema20[-1:][0]
        lastEma30 = ema30[-1:][0]
        lastEma99 = ema99[-1:][0]
        minValue = min([float(e['low']) for e in data[-4:]])
        close = float(data[-1:][0]['close'])
        self.last = "ema20:{} ema30:{} ema99:{}".format(
            lastEma20, lastEma30, lastEma99, close)
        if lastEma20 > lastEma30 and lastEma30 > lastEma99 \
                and minValue < lastEma20 and close > lastEma20:
            return 1
        if lastEma20 < lastEma30 and lastEma30 < lastEma99 \
                and minValue > lastEma20 and close < lastEma20:
            return -1
        return 0

    def getReason(self, signal):
        if signal == 1:
            return 'ema bullish and price cross ema20'
        if signal == -1:
            return 'ema bearish and price cross ema20'
