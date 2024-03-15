#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import argparse
import pandas as pd

from binance.futures import CoinM
from datetime import datetime as dt
from datetime import timedelta as td

from strategy.common.utils import get_auth_keys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', type=str)
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument(
        '--stgname', type=str,
        help='only recall the orders whose ClientOrderId start with given stgname!')
    args = parser.parse_args()
    if args.stgname:
        args.stgname += '_' # add the end mark '_' to it
    # create the API client first
    api_key, private_key = get_auth_keys()
    cli = CoinM(
        api_key=api_key,
        private_key=private_key,
    )
    cut_line_len = 96
    # get commisionRate
    print("=" * cut_line_len)
    rsp = cli.commission_rate(args.symbol)
    commission_rate = float(rsp['takerCommissionRate'])
    print(rsp)
    orders = cli.get_orders(
        symbol=args.symbol, limit=100)
    for i in range(args.limit // 100):
        order_t = cli.get_orders(
            symbol=args.symbol, limit=100, endTime=orders[0]['time'])
        orders = order_t[:-1] + orders
    # stat
    trans, long_open, short_open = [], [], []
    order_ids, start_t, end_t = set(), 0, 0
    for o in orders:
        if o['orderId'] in order_ids: # check if duplicated
            continue
        order_ids.add(o['orderId'])
        if args.stgname and not o['clientOrderId'].startswith(args.stgname):
            continue
        if o['status'] != 'FILLED':
            continue
        if o['side'] == 'BUY' and o['positionSide'] == 'LONG': # long open
            long_open.append(o)
        elif o['side'] == 'SELL' and o['positionSide'] == 'SHORT': # short open
            short_open.append(o)
        else: # close order
            if o['side'] == 'SELL': # long close
                if long_open:
                    ord = long_open.pop()
                    assert o['executedQty'] == ord['executedQty']
                    trans.append([
                        1, o['executedQty'], ord['time'], ord['avgPrice'],
                        o['time'], o['avgPrice']])
            else:
                if short_open:
                    ord = short_open.pop()
                    assert o['executedQty'] == ord['executedQty']
                    trans.append([
                        -1, o['executedQty'], ord['time'], ord['avgPrice'],
                        o['time'], o['avgPrice']])
    trans = pd.DataFrame(
        trans, columns=[
            'side', 'pos', 'open_time', 'open', 'close_time', 'close']).astype(float)
    trans.open_time = pd.to_datetime(trans.open_time * 1e6)
    trans.close_time = pd.to_datetime(trans.close_time * 1e6)
    temp = trans[['side', 'pos', 'open', 'close']]
    temp['step'] = (temp.close - temp.open) * temp.side
    temp['percent'] = temp.close / temp.open - 1.0
    print(temp)
    gross = trans.side * trans.pos * (trans.close - trans.open)
    comms = trans.pos * (trans.close + trans.open) * commission_rate 
    print('=' * cut_line_len)
    print(f'statistic result of {args.symbol}：')
    print(f'    - time range:{trans.open_time[0]} '
          f'~ {trans.close_time.iloc[-1]}')
    print(f'    - gross profit: {gross.sum():.5f}')
    print(f'    - gross profit per trade: {gross.mean():.5f}')
    print(f'    - commission: {comms.sum():.5f}')
    print(f'    - commission per trade: {comms.mean():.5f}')
    print('=' * cut_line_len)
