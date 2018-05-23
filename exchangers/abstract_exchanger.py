"""各取引所クラスが継承する抽象クラス."""

import abc

import json

import requests


class AbstractExchanger(abc.ABC):
    """
    Abstract Exchanger.

    すべてのExchangerクラスが以下の関数をもつことを強制するための抽象クラス.
    """

    exchanger_name = None

    def __init__(self):
        """
        各取引所クラスの設定変数を初期化します.

        api_url : str, default : None
            各取引所のAPIのURL.
        api_key : str, default : None
        api_secret : str, default : None
        """
        self.api_url = None
        self.api_key = None
        self.api_secret = None
        self.api_version = None

    @abc.abstractmethod
    def _headers(self, **params):
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
        pass

    def _api_request(self, endpoint, method='GET', params=None, headers=None):
        """
        各取引所のAPIにリクエストを送信するメソッド.

        Parameters
        ----------
        endpoint : str
            APIのエンドポイント.
        method : str, default 'GET'
        params : dict
            リクエストのパラメータを指定.
        headers : dict
            リクエストのヘッダーを指定.self._headersの戻り値を使用するように.

        Return
        ------
        response : dict
        """
        url = self.api_url + endpoint

        # 取引所のAPIにリクエストを送信.
        try:
            with requests.Session() as s:
                s.headers.update(headers)

                if method == "GET":
                    response = s.get(url, params=params)
                else:  # method == "POST":
                    response = s.post(url, data=json.dumps(params))
        except requests.RequestException as e:
            print(e)
            raise e

        return response.json()

    @abc.abstractmethod
    def get_markets(self):
        """取引所でのマーケット一覧を表示."""
        pass

    @abc.abstractmethod
    def get_board(self, product_code='BTC/JPY', count=100):
        """
        取引所の板情報を取得.

        Parameters
        ----------
        product_code : str, default 'BTC/JPY'
            通貨の指定.
        count : int, default 100
            結果の個数を指定.

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
        pass

    @abc.abstractmethod
    def get_ticker(self, product_code='BTC/JPY'):
        """
        引数で指定した通貨のTickerを取得.

        Parameters
        ----------
        product_code : str, default 'BTC/JPY'
            通貨の指定.
        """
        pass

    @abc.abstractmethod
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

    @abc.abstractmethod
    def calc_cash_trading_cost(self, product_code='BTC/JPY', side='maker', x=0.0, price=0.0, **params):
        """
        現物取引による費用を算出.

        Parameter
        ---------
        product_code: str, default 'BTC/JPY'
            通貨の指定.
        side : str, 'maker' or 'taker'
            購入か売却かを指定.
        x : float
            取引数量.
        price : float
            取引価格.
        """
        pass

    @abc.abstractmethod
    def calc_margin_trading_cost(self, product_code='BTC/JPY', side='maker', x=0.0, price=0.0, **params):
        """
        証拠金取引(信用取引)による費用を算出.

        Parameter
        ---------
        product_code: str, default 'BTC/JPY'
            通貨の指定.
        side : str, 'maker' or 'taker'
            購入か売却かを指定.
        x : float
            取引数量.
        price : float
            取引価格.
        """
        pass
