"""Exchangerサービス."""

from exchangers import BitFlyerLightningExchanger
from exchangers import QuoineExchanger


def get_all_boards(product_code='BTC/JPY', count=100):
    """全ての取引所から指定した通貨の板情報を取得する."""
    all_boards = {
        'Quoine': QuoineExchanger().get_board(product_code, count),
        'BitFlyerLightning': BitFlyerLightningExchanger().get_board(product_code, count),
    }
    return all_boards


def get_board_by_exchanger_name(exchanger_name=None, product_code='BTC/JPY', count=100):
    """指定した取引所から板情報を取得."""
    exchanger_cls = get_exchanger_cls(exchanger_name)
    return exchanger_cls().get_board(product_code, count)


def get_exchanger_cls(exchanger_name=None):
    """取引所クラスを取得."""
    EXCHANGER_CLASS_DICT = {
        'Quoine': QuoineExchanger,
        'BitFlyerLightning': BitFlyerLightningExchanger,
    }
    exchanger_cls = EXCHANGER_CLASS_DICT.get(exchanger_name)
    return exchanger_cls


def calc_cash_trading_cost_by_exchanger_name(exchanger_name=None, product_code='BTC/JPY',
                                             side='maker', x=0.0, price=0.0, **params):
    """現物取引による費用を算出."""
    exchanger_cls = get_exchanger_cls(exchanger_name)
    trading_cost = exchanger_cls.calc_cash_trading_cost(product_code, side, x, price, params)
    return trading_cost


def calc_margin_trading_cost_by_exchanger_name(exchanger_name=None, product_code='BTC/JPY',
                                               side='maker', x=0.0, price=0.0, **params):
    """証拠金取引(信用取引)による費用を算出."""
    exchanger_cls = get_exchanger_cls(exchanger_name)
    trading_cost = exchanger_cls.calc_margin_trading_cost(product_code, side, x, price, params)
    return trading_cost
