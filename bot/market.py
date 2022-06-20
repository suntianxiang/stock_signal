import requests
from .config import config


class Market:
    def kline(symbol, period, size):
        pass


class Sina(Market):
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
