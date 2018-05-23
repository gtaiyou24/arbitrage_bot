"""裁定(アービトラージ)取引を実行するスクリプト."""

import os
import sys

import numpy as np
import time

from exchangers import service as exchanger_serv


PRODUCT_CODE = 'BTC/JPY'


if __name__ == '__main__':
    """実行."""
    sys.path.append(os.getcwd())

    while True:
        # 1. 1秒ごとに各取引所から板情報を取得.
        all_boards = exchanger_serv.get_all_boards(product_code=PRODUCT_CODE, count=100)

        # 2. 最良売値/最良買値を算出する。もしそのスプレッドが逆転している場合(買値が売値より高い場合)、
        #    裁定機会は存在しないためステップ1へ戻る
        for exchange_name1 in all_boards.keys():
            for exchange_name2 in all_boards.keys():
                if exchange_name1 == exchange_name2:
                    continue

                high_bid = np.array(all_boards[exchange_name1]['bids'])[0, 0]
                low_ask = np.array(all_boards[exchange_name2]['asks'])[0, 0]
                spred = low_ask - high_bid
                print('スプリッド({0} - {1}): {2}'.format(exchange_name2, exchange_name1, spred))

                if spred <= 0:
                    continue

                # 3. スプレッドが逆転しているとき、期待収益率を算出する.
                #    もしその値が閾値を超えていたら、指値注文を同時送信する.

                # 数量.
                x = 0.2
                # 収入.
                r = low_ask * x
                # 費用.
                cost = 0
                c = (high_bid * x - cost)
                expected_income_rate = (r - c) / c
                if not expected_income_rate > 0.0001:
                    continue

                print('期待収益({0} - {1}): {2}円'.format(exchange_name2, exchange_name1, int(r - c)))

        print('=======================')

        time.sleep(3)
