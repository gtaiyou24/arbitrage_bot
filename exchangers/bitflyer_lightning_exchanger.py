"""bitFlyer Lightning取引所クラス."""

import hashlib
import hmac
import json
import time
import urllib

import pandas as pd

from .abstract_exchanger import AbstractExchanger

from configs.exchanger_config import get_exchanger_config


class BitFlyerLightningExchanger(AbstractExchanger):
    """bitFlyer Lightningと取引で行うためのクラス."""

    exchanger_name = 'BitFlyerLightning'

    def __init__(self):
        """
        各取引所クラスの設定変数を初期化します.

        api_url : str, default : None
            各取引所のAPIのURL.
        api_key : str, default : None
        api_secret : str, default : None
        """
        self.api_url = 'https://api.bitflyer.jp/v1'
        self.api_key = get_exchanger_config(self.exchanger_name, 'api_key')
        self.api_secret = get_exchanger_config(self.exchanger_name, 'api_secret')
        self.api_version = None

    def _headers(self, endpoint=None, method='GET', params={}):
        """
        各取引所のAPIにrequestする際のヘッダーを生成し返すメソッド.

        Parameters
        ----------
        params : dict
            各取引所で値が違う.

        Return
        ------
        headers : dict,
            ex) requests.get(url, headers)
        """
        body = ""
        if method == "POST":
            body = json.dumps(params)
        else:
            if params:
                body = "?" + urllib.parse.urlencode(params)

        access_timestamp = str(time.time())
        text = str.encode(access_timestamp +
                          method +
                          endpoint +
                          body
                          )
        access_sign = hmac.new(str.encode(self.api_secret),
                               text,
                               hashlib.sha256
                               ).hexdigest()
        header = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-TIMESTAMP": access_timestamp,
            "ACCESS-SIGN": access_sign,
            "Content-Type": "application/json"
        }
        return header

    def get_markets(self):
        """
        取引所でのマーケット一覧を表示.

        Return
        ------
        [
            {"product_code": "BTC/JPY"},
            {"product_code": "ETH/BTC"},
            ...
        ]
        """
        endpoint = '/markets'
        header = self._headers(endpoint, method='GET')
        response_dict = self._api_request(endpoint, 'GET', None, header)
        return response_dict

    def get_board(self, product_code='BTC/JPY', count=100):
        """
        取引所の板情報を取得.

        Parameters
        ----------
        product_code : str, default 'BTC/JPY'
            通貨の指定.

        Return
        ------
        {
            "bids": [
                # [price, quantity]
                [1000000, 0.02],
                [9950000, 0.05],
                ...
            ],
            "asks": [
                [1005000, 0.3],
                [1060000, 0.05],
                ...
            ]
        }
        """
        BITFLYER_LIGHTNING_PRODUCT_CODES = {
            'BTC/JPY': 'BTC_JPY',
        }

        product_code = BITFLYER_LIGHTNING_PRODUCT_CODES[product_code]
        endpoint = '/board'
        params = {'count': count}
        header = self._headers(endpoint, method='GET')
        response_dict = self._api_request(endpoint, 'GET', params, header)

        board = {
            "bids": pd.DataFrame(response_dict['bids']).values.tolist(),
            "asks": pd.DataFrame(response_dict['asks']).values.tolist()
        }
        return board

    def get_ticker(self, product_code='BTC/JPY'):
        """
        引数で指定した通貨のTickerを取得.

        Parameters
        ----------
        product_code : str, default 'BTC/JPY'
            通貨の指定.
        """
        pass

    def get_execution_log(self, product_code='BTC/JPY', count=100):
        """
        歩み値を取得.

        Parameters
        ----------
        product_code: str, default 'BTC/JPY'
            通貨の指定.
        count: int, default 100
            取得する歩み値の数.

        Return
        ------
        [
            {
                "id": id番号,
                "side": "SELL" or "BUY",
                "price": 約定価格,
                "quantity": 数量,
                "execution_datetime": 約定時刻(2018-05-20 19:16:53.291276)
            },
            ...,
        ]
        """
        pass

    def calc_cash_trading_cost(product_code='BTC/JPY', side='maker', x=0.0, price=0.0, **params):
        """現物取引による費用を算出."""
        pass

    def calc_margin_trading_cost(product_code='BTC/JPY', side='maker', x=0.0, price=0.0, **params):
        """証拠金取引(信用取引)による費用を算出."""
        pass
