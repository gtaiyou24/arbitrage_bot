"""各取引所クラスが継承する抽象クラス."""

import abc


class AbstractExchanger(abc.ABC):
    """
    Abstract Exchanger.

    すべてのExchangerクラスが以下の関数をもつことを強制するための抽象クラス.
    """

    @abc.abstractmethod
    def get_markets(self):
        """取引所でのマーケット一覧を表示."""

    @abc.abstractmethod
    def get_board(self):
        """取引所の板情報を取得."""
        pass

    @abc.abstractmethod
    def get_ticker(self):
        """引数で指定した通貨の取引データ(チェッカー)を取得."""
        pass

    @abc.abstractmethod
    def get_execution_log(self):
        """約定履歴を取得."""
        pass

    @abc.abstractmethod
    def buy(self, x, price, how):
        """通貨の購入メソッド."""
        pass

    @abc.abstractmethod
    def sell(self, x, price, how):
        """通貨の売却メソッド."""
        pass
