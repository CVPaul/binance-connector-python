#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
import time
import pandas as pd

from binance.futures import CoinM
from datetime import datetime as dt
from datetime import timedelta as td


# global
symbol =  sys.argv[1] # 'DOGEUSD_PERP'
stop_s = '2024-03-05'
start_s = '2023-01-21'

# ED25519 Keys
api_key = "../api_key.txt"
private_key = "../private_key.pem"
private_key_pass = ""
day_ms_count = 24 * 3600 * 1000
stop_t = int(pd.Timestamp(stop_s).timestamp() * 1000)
start_t = int(pd.Timestamp(start_s).timestamp() * 1000)


with open(api_key) as f:
    api_key = f.read().strip()

with open(private_key, 'rb') as f:
    private_key = f.read()

client = CoinM(
    api_key=api_key,
    private_key=private_key,
    private_key_pass=private_key_pass,
    # base_url="https://dapi.binance.com"
)

# Get server timestamp
# print(client.time())
# Get klines of BTCUSDT at 1m interval
os.makedirs(f'data/{symbol}/', exist_ok=True)
while start_t < stop_t:
    day = pd.to_datetime(start_t * 1e6)
    start_t += day_ms_count
    df = pd.DataFrame(
        client.klines(symbol, "1m", endTime=start_t, limit=1441)[:-1],
        columns=[
            'start_t', 'open', 'high', 'low', 'close',
            'volume', 'end_t', 'amount', 'trade_cnt',
            'taker_vol', 'taker_amt', 'reserved'
        ])
    df.to_csv(f'data/{symbol}/{day.date()}.csv', index=False)
    print(symbol, day)
    time.sleep(1/40)
#print(client.ext_klines("BTCUSD", "1m", 'continuous', contractType='PERPETUAL', limit=1))
#print(client.ext_klines("BTCUSD", "1m", 'indexPrice', limit=1))
## Get last 10 klines of BNBUSDT at 1h interval
#print(client.klines("BNBUSD_PERP", "1h", limit=1))
