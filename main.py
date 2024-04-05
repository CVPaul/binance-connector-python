#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
import time
import json
import pandas as pd

from binance.futures import CoinM
from datetime import datetime as dt
from datetime import timedelta as td
from strategy.common.utils import get_auth_keys

from binance.websocket.futures.coin_m.stream import CoinMWSSStreamClient


def on_message(self, message):
    message = json.loads(message)
    e = message.get('e', '')
    print(json.dumps(message, indent=4))


if __name__ == "__main__":

    api_key, private_key = get_auth_keys()

    client = CoinM(
        api_key=api_key,
        private_key=private_key,
    )
    print(client.time())
    rsp = client.new_order(
        symbol='DOGEUSD_PERP', side='SELL', type='STOP',
        price=0.1768, stopPrice=0.1861,
        timeInForce='GTC', quantity=1, positionSide='LONG')
    print(rsp)
    # acc = client.exchange_info(symbol)
    # with open(f'{symbol}.json', 'w') as fp:
    #     json.dump(acc, fp, indent=4)
    # print(client.user_trades(symbol))
    #for i in range(10):
    #    line = client.klines(symbol, '5m', limit=1)
    #    print(i, client.time(), line)
    #    time.sleep(5)
    #print(client.time())
    #
    #rsp = client.new_listen_key()
    #print(rsp)
    # create wedsocket stream client
    # wscli = CoinMWSSStreamClient(
    #     # stream_url=wss_test_url,
    #     on_message=on_message)
    # wscli.book_ticker(symbol)
    ## wscli.kline(symbol, '1m')
    #wscli.user_data(rsp['listenKey'])
    # wscli.agg_trade(symbol)
    # enable it by endpoint POST /dapi/v1/positionSide/dual, setting the parameter dualSidePosition = true
    # Open position:
    #   - Long : positionSide=LONG, side=BUY
    #   - Short: positionSide=SHORT, side=SELL
    # Close position:
    #   - Close long position: positionSide=LONG, side=SELL
    #   - Close short position: positionSide=SHORT, side=BUY
    #order = {
    #    'symbol': 'DOGEUSD_PERP',
    #    'side': 'BUY',
    #    'type': 'LIMIT',
    #    'timeInForce': 'GTC',
    #    'quantity': 1,
    #    'price': 0.1608,
    #    'positionSide': 'SHORT'
    #}
    #print(client.new_order(**order))
    # ords = client.get_orders(symbol, limit=20)
    # print(json.dumps(ords, indent=4))
    # 10303866131
    # print(client.cancel_order(symbol, origClientOrderId='KEpBHANuPJCQlGZOgjAkdI'))
    print('send order finished!')
    # print(pd.DataFrame(kline_store)[['E', 't', 'T', 'o', 'h', 'l', 'c']])



