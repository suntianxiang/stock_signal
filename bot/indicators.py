from cmath import nan
from numpy import isnan
from talib import ATR


def chandelier_exit(close, high, low, period=22):
    data = dict(high=[], low=[], trend=[])
    prev_trend = 0
    atr = ATR(high, low, close,
              timeperiod=period)
    for k, v in enumerate(high):
        if k < period or isnan(atr[k]):
            data['high'].append(nan)
            data['low'].append(nan)
            data['trend'].append(0)
            continue
        high_items = high[k-period:k+1]
        low_items = low[k-period:k+1]

        ce_high = max(high_items) - atr[k] * 3
        ce_low = min(low_items) + atr[k] * 3
        if close[k] > ce_high:
            prev_trend = 1
        elif close[k] < ce_low:
            prev_trend = -1
        else:
            prev_trend = prev_trend

        data['high'].append(ce_high)
        data['low'].append(ce_low)
        data['trend'].append(prev_trend)
    return data
