#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
import time
import logging
import argparse
import pandas as pd

from binance.futures import CoinM
from binance.constant import N_MS_PER_SEC
from binance.constant import N_MS_PER_DAY

from datetime import datetime as dt
from datetime import timedelta as td

from strategy.common.utils import get_auth_keys
from strategy.common.utils import on_open, on_close


# logging
logging.basicConfig(
    filename='trend.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', '-s', type=str, required=True)
    parser.add_argument('--start-time', type=str)
    parser.add_argument('--end-time', type=str)
    parser.add_argument(
        '--type', type=str, required=True,
        choice=['kline', 'tick'])
    args = parser.parse_args()
    # args convert
    end_t = pd.to_datetime(args.end_time).Timestamp() * 1000
    start_t = pd.to_datetime(args.start_time).Timestamp() * 1000
    assert start_t <= end_t
    # create client
    api_key, private_key = get_auth_keys()
    cli = CoinM(
        api_key=api_key,
        private_key=private_key,
    )
    # start pull data
    data = []
    os.makedirs(f'data/{args.symbol}/', exist_ok=True)
    while start_t <= end_t:
        if args.type == 'kline':
            dat = cli.klines(
                args.symbol, args.period,
                startTime=start_t, limit=1441)
            day = pd.to_datetime(start_t * 1e6)
            assert dat[-1][0] == start_t + N_MS_PER_DAY
            start_t = dat[-1][0]
            dat = pd.DateFrame(dat[:-1], columns=[
                'start_t', 'open', 'high', 'low', 'close',
                'volume', 'end_t', 'amount', 'trade_cnt',
                'taker_vol', 'taker_amt', 'reserved'
            ])
            dat.to_csv(f'data/{args.symbol}/{day.date()}.csv', index=False)
            loging.info(
                f'{dat.shape[0]} 1m klines of {args.symbol}@'
                f'{day.date()}had been save to data dir!')
            time.sleep(1/40)
