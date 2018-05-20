import abc
import json
import requests
import time
from jwt import jwt


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
                {"price": 1000000, "size": 0.02},
                {"price": 9950000, "size": 0.05},
                ...
            ],
            "asks": [
                {"price": 1005000, "size": 0.3},
                {"price": 1060000, "size": 0.05},
                ...
            ]
        }
        """
        pass


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
        self.api_key = '579911'
        self.api_secret = 'KAtyz4oKIrnKOVkdpiZT01BczMV/xDQ/G5jED3bmgY23MSoP6pUyVUiDzWwuF9dM7VQBCFTYyXmyj3lFCxfmFw=='
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
                {"price": 1000000, "size": 0.02},
                {"price": 9950000, "size": 0.05},
                ...
            ],
            "asks": [
                {"price": 1005000, "size": 0.3},
                {"price": 1060000, "size": 0.05},
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
        return response_dict
