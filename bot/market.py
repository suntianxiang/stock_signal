import requests
from .config import config


class Market:
    long_period = None
    short_period = None

    def kline(symbol, period, size):
        pass


class Sina(Market):
    long_period = 60
    short_period = 30

    def kline(self, symbol, period, size):
        r = requests.get(config['markets']['sina']['host']+'/quotes_service/api/json_v2.php/CN_MarketData.getKLineData', params={
            'symbol': symbol,
            'scale': period,
            'ma': 'no',
            'datalen': size
        })
        if r.status_code != 200:
            raise ValueError('get kline failed')
        return r.json()
