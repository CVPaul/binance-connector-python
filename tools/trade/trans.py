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
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--start-time', type=str)
    parser.add_argument('--end-time', type=str)
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
    if args.end_time:
        args.end_time = pd.to_datetime(args.end_time).timestamp() * 1000
    else:
        args.end_time = orders[0]['time']
    if args.start_time:
        args.start_time = pd.to_datetime(args.start_time).timestamp() * 1000
    else:
        assert args.limit, "you should specify at least one of --limit/--start-time"
    while args.end_time >= args.start_time:
        if args.limit > 0 and len(orders) >= args.limit:
            break 
        order_t = cli.get_orders(
            symbol=args.symbol, limit=100, endTime=args.end_time)
        if len(order_t) == 1: # not more orders any more
            break
        args.end_time = order_t[0]['time']
        orders = order_t[:-1] + orders
    # stat
    trans, long_open, short_open = [], [], []
    order_ids, start_t, end_t = set(), 0, 0
    fields =  ["avgPrice", "executedQty", "side", "positionSide", "time"]
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
                    print('can not match long close order:')
                    df = pd.DataFrame([o])[fields]
                    df.time = pd.to_datetime(df.time*1e6).dt.strftime("%Y%m%d %H:%M:%S")
                    print(df)
            else:
                if short_open:
                    ord = short_open.pop()
                    assert o['executedQty'] == ord['executedQty']
                    trans.append([
                        -1, o['executedQty'], ord['time'], ord['avgPrice'],
                        o['time'], o['avgPrice']])
                else:
                    print('can not match short close order:')
                    df = pd.DataFrame([o])[fields]
                    df.time = pd.to_datetime(df.time*1e6).dt.strftime("%Y%m%d %H:%M:%S")
                    print(df)
    if trans:
        trans = pd.DataFrame(
            trans, columns=[
                'side', 'pos', 'open_time', 'open', 'close_time', 'close']).astype(float)
        trans.open_time = pd.to_datetime(trans.open_time * 1e6).dt.strftime('%Y%m%d %H:%M:%S')
        trans.close_time = pd.to_datetime(trans.close_time * 1e6).dt.strftime('%Y%m%d %H:%M:%S')
        trans['step'] = (trans.close - trans.open) * trans.side
        trans['percent'] = trans.close / trans.open - 1.0
        trans['gross'] = trans.side * trans.pos * (trans.close - trans.open)
        trans['comms'] = trans.pos * (trans.close + trans.open) * commission_rate
        print(trans)
        print('=' * cut_line_len)
        print(f'statistic result of {args.symbol}：')
        print(f'    - time range:{trans.open_time[0]} '
              f'~ {trans.close_time.iloc[-1]}')
        print(f'    - gross profit: {trans.gross.sum():.5f}')
        print(f'    - gross profit per trade: {trans.gross.mean():.5f}')
        print(f'    - commission: {trans.comms.sum():.5f}')
        print(f'    - commission per trade: {trans.comms.mean():.5f}')
        print('=' * cut_line_len)
    if long_open:
        print(f'still open long orders:')
        df = pd.DataFrame(long_open)[fields]
        df.time = pd.to_datetime(df.time*1e6).dt.strftime("%Y%m%d %H:%M:%S")
        print(df)
        print('=' * cut_line_len)
    if short_open:
        print(f'still open short orders:')
        df = pd.DataFrame(short_open)[fields]
        df.time = pd.to_datetime(df.time*1e6).dt.strftime("%Y%m%d %H:%M:%S")
        print(df)
        print('=' * cut_line_len)
