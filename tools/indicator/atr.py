#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
import time
import json
import logging
import argparse
import pandas as pd

from binance.futures import CoinM
from datetime import datetime as dt
from datetime import timedelta as td

from binance.websocket.futures.coin_m.stream import CoinMWSSStreamClient

from strategy.indicator.common import MA
from strategy.indicator.common import ATR

from strategy.common.utils import get_auth_keys
from strategy.common.utils import on_open, on_close


# logging
logging.basicConfig(
    filename='trend.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
# global
ROUND_AT = {
    "DOGEUSD_PERP": 5,
}

# strategy construct
k = 1.0
length = 150
interval = 300000 # 300000 # 5m


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', '-s', type=str, required=True)
    parser.add_argument('--freq', '-f', type=str, required=True)
    parser.add_argument('--length', '-l', type=int, required=True)
    args = parser.parse_args()
    # global
    symbol = args.symbol # 'DOGEUSD_PERP'
    api_key, private_key = get_auth_keys()
    client = CoinM(
        api_key=api_key,
        private_key=private_key,
    )

    df = client.klines(symbol, args.freq, limit = args.length + 2)
    df = df[:-1] # 最后一根kline是不完整的
    df = pd.DataFrame(
        df, columns=[
            'start_t', 'open', 'high', 'low', 'close',
            'volume', 'end_t', 'amount', 'trade_cnt',
            'taker_vol', 'taker_amt', 'reserved'
        ]).astype(float)
    ma = MA(args.length, df)
    atr = ATR(args.length, df)

    s = ma.value
    a = atr.value

    cutline_len = 145
    print("=" * cutline_len)
    print(f"metric info: length={args.length}|freq={args.freq}")
    print(f"    - MA: {s:.6f}")
    print(f"    - ATR: {a:.6f}")
    print(f"    - Ratio: {a * 100 / s :.2f}%")
    print("=" * cutline_len)
