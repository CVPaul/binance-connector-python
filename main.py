#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
import time

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


def on_message(x, message):
    print('+' * 102)
    print('first args:', x)
    print('message:', message)
    print('+' * 102)

if __name__ == "__main__":

    with open(api_key) as f:
        api_key = f.read().strip()

    with open(private_key, 'rb') as f:
        private_key = f.read()

    # client = CoinM(
    #     api_key=api_key,
    #     private_key=private_key,
    #     private_key_pass=private_key_pass,
    #     # base_url="https://dapi.binance.com"
    # )
    
    # create wedsocket stream client
    wscli = CoinMWSSStreamClient(on_message=on_message)
    wscli.kline(symbol, '5m')
    wscli.ticker(symbol)

    time.sleep(300)



