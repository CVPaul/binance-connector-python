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

from binance.websocket.futures.coin_m.stream import CoinMWSSStreamClient


# global
symbol =  sys.argv[1] # 'DOGEUSD_PERP'
stop_s = '2024-03-05'
start_s = '2023-01-21'

# ED25519 Keys
api_key = "../api_key.txt"
private_key = "../private_key.pem"
private_key_pass = ""

wss_test_url = "wss://dstream.binancefuture.com"
api_test_url = "https://testnet.binancefuture.com"

kline_store = []


def on_message(self, message):
    message = json.loads(message)
    e = message.get('e', '')
    if e == 'kline':
        dat = message['k']
        dat['E'] = message['E']
        kline_store.append(dat)


if __name__ == "__main__":

    with open(api_key) as f:
        api_key = f.read().strip()

    with open(private_key, 'rb') as f:
        private_key = f.read()

    client = CoinM(
        api_key=api_key,
        private_key=private_key,
        private_key_pass=private_key_pass,
        base_url=api_test_url,
        # base_url="https://dapi.binance.com"
    )
    print(client.account())
    # print(client.user_trades(symbol))
    #for i in range(10):
    #    line = client.klines(symbol, '5m', limit=1)
    #    print(i, client.time(), line)
    #    time.sleep(5)
    #print(client.time())
    #
    ## create wedsocket stream client
    #wscli = CoinMWSSStreamClient(on_message=on_message)
    #wscli.kline(symbol, '5m')
    #wscli.agg_trade(symbol)
    #time.sleep(30)
    #print(pd.DataFrame(kline_store)[['E', 't', 'T', 'o', 'h', 'l', 'c']])



