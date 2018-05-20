"""Exchangerサービス."""

from exchangers import BitFlyerLightningExchanger
from exchangers import QuoineExchanger


def get_all_boards(product_code='BTC/JPY', count=100):
    """全ての取引所から指定した通貨の板情報を取得する."""
    all_boards = {
        'Quoine': QuoineExchanger().get_board(product_code='BTC/JPY', count=100),
        'BitFlyerLightning': BitFlyerLightningExchanger().get_board(product_code='BTC/JPY', count=100)
    }
    return all_boards


def get_board_by_exchanger_name(exchanger_name, product_code='BTC/JPY', count=100):
    """指定した取引所から板情報を取得."""
    exchanger_cls = get_exchanger_cls(exchanger_name)
    return exchanger_cls().get_board(product_code='BTC/JPY', count=100)


def get_exchanger_cls(exchanger_name):
    """取引所クラスを取得."""
    EXCHANGER_CLASS_DICT = {
        'Quoine': QuoineExchanger(),
        'BitFlyerLightning': BitFlyerLightningExchanger()
    }
    exchanger_cls = EXCHANGER_CLASS_DICT.get(exchanger_name)
    return exchanger_cls
