import requests
from .config import config


class Market:
    long_period = None
    short_period = None
    micro_period = None

    def kline(symbol, period, size):
        pass


class Sina(Market):
    long_period = 60
    short_period = 30
    micro_period = 15

    def kline(self, symbol, period, size):
        r = requests.get(
            config['markets']['sina']['host']+'/quotes_service/'
            + 'api/json_v2.php/CN_MarketData.getKLineData',
            params={
                'symbol': symbol,
                'scale': period,
                'ma': 'no',
                'datalen': size
            })
        if r.status_code != 200:
            raise ValueError('get kline failed')
        return r.json()


class Binance(Market):
    long_period = '1d'
    short_period = '60m'
    micro_period = '15m'

    proxies = {
        "https": "http://127.0.0.1:1080"
    }

    def kline(self, symbol, period, size):
        r = requests.get(
            config['markets']['binance']['host']+'/api/v3/klines',
            params={
                'symbol': symbol,
                'interval': period,
                'limit': size
            }, proxies=self.proxies)
        if r.status_code != 200:
            raise ValueError('get kline failed')
        res = r.json()
        data = []
        for item in res:
            data.append(dict(
                id=item[0]/1000,
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
                vol=item[5],
                amount=None,
                count=item[8],
            ))
        return data
