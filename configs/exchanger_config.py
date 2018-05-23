"""各取引所の設定値を操作するモジュール."""

from configparser import ConfigParser


EXCHANGER_CONFIG_PATH = './config.ini'


def get_exchanger_config(exchanger_name, config_name):
    """
    各取引所の設定値を取得する.

    Parameters
    ----------
    exchanger_name : str
            取引所名.
    config_name : str
            設定名.

    Return
    ------
    config_value : str
            設定値.
    """
    config = ConfigParser()
    config.read(EXCHANGER_CONFIG_PATH, 'utf-8')
    return config.get(exchanger_name, config_name)
