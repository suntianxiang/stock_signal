from talib import EMA, PLUS_DI, MINUS_DI, ADX, RSI
import numpy
from ..indicators import chandelier_exit

# price reverse strategy according to ema


class EMACross:
    last = ''
    reason = ''

    def indicate(self, data):
        closes = numpy.array([float(e['close']) for e in data])
        ema20 = EMA(closes, 20)
        ema40 = EMA(closes, 40)
        ema99 = EMA(closes, 99)
        lastEma20 = ema20[-1:][0]
        lastEma40 = ema40[-1:][0]
        lastEma99 = ema99[-1:][0]
        close = float(data[-1:][0]['close'])
        self.last = "ema20:{} ema40:{} ema99:{}".format(
            lastEma20, lastEma40, lastEma99, close)
        if ema20[-2:][0] > closes[-2:][0] and ema20[-2:][1] < closes[-2:][1]:
            self.reason = 'ema20 cross'
            return 1
        if ema40[-2:][0] > closes[-2:][0] and ema40[-2:][1] < closes[-2:][1]:
            self.reason = 'ema40 cross'
            return 1
        if ema99[-2:][0] > closes[-2:][0] and ema99[-2:][1] < closes[-2:][1]:
            self.reason = 'ema99 cross'
            return 1
        if ema20[-2:][0] < closes[-2:][0] and ema20[-2:][1] > closes[-2:][1]:
            self.reason = 'ema20 cross'
            return -1
        if ema40[-2:][0] < closes[-2:][0] and ema40[-2:][1] > closes[-2:][1]:
            self.reason = 'ema40 cross'
            return -1
        if ema99[-2:][0] < closes[-2:][0] and ema99[-2:][1] > closes[-2:][1]:
            self.reason = 'ema99 cross'
            return -1

        return 0

    def getReason(self, signal):
        return self.reason

    def getImgComponent(self):
        return ['ema']


class DMICross:
    last = ''

    def indicate(self, data):
        high = numpy.array([float(e['high']) for e in data])
        low = numpy.array([float(e['low']) for e in data])
        close = numpy.array([float(e['close']) for e in data])
        plus_di = PLUS_DI(high, low, close, timeperiod=14)
        minus_di = MINUS_DI(high, low, close, timeperiod=14)
        adx = ADX(high, low, close, timeperiod=14)
        if (plus_di[-2:][0] < minus_di[-2:][0]
                and plus_di[-1:][0] > minus_di[-1:][0] and adx[-1:][0] >= 25):
            return 1
        if (plus_di[-2:][0] > minus_di[-2:][0]
                and plus_di[-1:][0] < minus_di[-1:][0]):
            return -1
        return 0

    def getReason(self, signal):
        return "dmi cross"

    def getImgComponent(self):
        return []


class CERSI:
    last = ''

    def indicate(self, data):
        high = numpy.array([float(e['high']) for e in data])
        low = numpy.array([float(e['low']) for e in data])
        close = numpy.array([float(e['close']) for e in data])
        res = chandelier_exit(close, high, low)
        rsi = RSI(close, 20)
        # 空 转 多
        if res['trend'][-1:][0] == 1 and res['trend'][-2:-1][0] == -1:
            return 1
        # 多头超卖
        if res['trend'][-1:][0] == 1 and rsi[-1:][0] < 30:
            return 1
        # 多 转 空
        if res['trend'][-1:][0] == -1 and res['trend'][-2:-1][0] == 1:
            return -1
        # 空头超买
        if res['trend'][-1:][0] == -1 and rsi[-1:][0] > 70:
            return -1
        return 0

    def getReason(self, signal):
        if signal == 1:
            return 'chandelier_exit buy'
        elif signal == -1:
            return 'chandelier_exit sell'

    def getImgComponent(self):
        return ['ce', 'rsi']
