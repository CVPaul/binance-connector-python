#!/usr/bin/env python
#-*- coding:utf-8 -*-


import pandas as pd
from binance.futures import CoinM


# global
symbol = 'DOGEUSD_PERP'
stop_s = '2024-01-01'
start_s = '2023-07-01'

# ED25519 Keys
api_key = "../api_key.txt"
private_key = "../private_key.pem"
private_key_pass = ""

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
print(client.time())
# Get klines of BTCUSDT at 1m interval
df = pd.DataFrame(
    client.klines(symbol, "1m", startTime=start_t, endTime=stop_t),
    columns=[
        'start_t', 'open', 'high', 'low', 'close',
        'volume', 'end_t', 'amount', 'trade_cnt',
        'taker_vol', 'taker_amt', 'reserved'
    ])
df.to_csv(f'{symbol}_{start_s}_{stop_s}.csv', index=False)
#print(client.ext_klines("BTCUSD", "1m", 'continuous', contractType='PERPETUAL', limit=1))
#print(client.ext_klines("BTCUSD", "1m", 'indexPrice', limit=1))
## Get last 10 klines of BNBUSDT at 1h interval
#print(client.klines("BNBUSD_PERP", "1h", limit=1))
