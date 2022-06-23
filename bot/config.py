config = {
    'platform': 'sina',
    'markets': {
        'sina': {
            'host': 'https://money.finance.sina.com.cn',
        }
    },
    'symbols': [
        ['保龄宝', 'sz002286'],
        ['海尔智家', 'sh600690'],
        ['同仁堂', 'sh600085'],
        ['格力电器', 'sz000651'],
        ['海康威视', 'sz002415'],
        ['广发证券', 'sz000776'],
    ],
    'long_period': ['60min', 60],
    'short_period': ['30min', 30],
    'notification': {
        'dingding': {
            'access_token': '73c463254d48c99f4a42b4ea7e77c'
            + 'f49453770960ceea1810413783b7ac395f5',
            'secret': 'SEC3b1f70a11a1ba3636f2c39cd4c6c1'
            + 'f78245d42834845da1ba0afef4fcca2d932'
        }
    },
    'strategies': [
        'BollStoch',
        'EMACross',
        'MACDCross',
        'DMICross'
    ],
}
