"""QUOINE取引所のクラス."""

import time
import jwt
import numpy as np


from configs.exchanger_config import get_exchanger_config

from .abstract_exchanger import AbstractExchanger


class QuoineExchanger(AbstractExchanger):
    """Quoine(コインエクスチェンジ)と取引で行うためのクラス."""

    exchanger_name = 'Quoine'

    def __init__(self):
        """
        各取引所クラスの設定変数を初期化します.

        api_url : str, default : None
            各取引所のAPIのURL.
        api_key : str, default : None
        api_secret : str, default : None
        """
        self.api_url = 'https://api.quoine.com'
        self.api_key = get_exchanger_config(self.exchanger_name, 'api_key')
        self.api_secret = get_exchanger_config(self.exchanger_name, 'api_secret')
        self.api_version = '2'

    def _headers(self, endpoint):
        """
        各取引所のAPIにrequestする際のヘッダーを生成し返すメソッド.

        Parameters
        ----------
        endpoint : str, default None

        Return
        ------
        headers : dict,
            ex) requests.get(url, headers)
        """
        auth_payload = {
            'path': endpoint,
            'nonce': str(int(time.time())),
            'token_id': self.api_key
        }
        access_sign = jwt.encode(auth_payload, self.api_secret, algorithm='HS256')
        header = {
            'X-Quoine-API-Version': self.api_version,
            'X-Quoine-Auth': access_sign,
            'Content-Type': 'application/json'
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
        endpoint = '/products'
        response_dict = self._api_request(endpoint, 'GET', None, self._headers(endpoint))
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
        QUOINE_PRODUCT_IDS = {
            'BTC/JPY': 5,
        }
        product_id = QUOINE_PRODUCT_IDS[product_code]
        endpoint = '/products/{id}/price_levels'.format(id=product_id)
        params = {
            'full': count
        }
        response_dict = self._api_request(endpoint, 'GET', params, self._headers(endpoint))

        # 価格,数量を文字型からfloat型へ変換する.
        buy_price_level_arr = np.array(response_dict['buy_price_levels']).astype(float)
        sell_price_levels_arr = np.array(response_dict['sell_price_levels']).astype(float)

        # 価格をint型へ変換する.
        buy_price_level_arr[:, 0].astype(int)
        sell_price_levels_arr[:, 0].astype(int)

        board = {
            "bids": buy_price_level_arr.tolist(),
            "asks": sell_price_levels_arr.tolist()
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
