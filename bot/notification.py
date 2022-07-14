import hashlib
import hmac
import base64
import time
import urllib.parse

import requests

from .config import config


class DingDing:
    def notify(self, title, text):
        timestamp = str(round(time.time() * 1000))
        r = requests.post('https://oapi.dingtalk.com/robot/send', params={
            'access_token': config["dingding"]["access_token"],
            'timestamp': timestamp,
            'sign': self.__sign(timestamp)
        }, json={
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': text
            }
        })
        if r.status_code != 200:
            raise ValueError('get kline failed')
        return r.json()

    def __sign(self, timestamp):
        secret = config["dingding"]["secret"]
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign
