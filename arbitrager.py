"""裁定(アービトラージ)取引を実行するスクリプト."""

import os
import sys
from pprint import pprint

from exchangers import service as exchanger_serv


if __name__ == '__main__':
    """実行."""
    sys.path.append(os.getcwd())

    all_boards = exchanger_serv.get_all_boards(product_code='BTC/JPY', count=100)
    pprint(all_boards)
