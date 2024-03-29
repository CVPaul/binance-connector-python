#!/usr/bin/env python
#-*- coding:utf-8 -*-

#-------------'_M_' means main/most---------------
# spot
_SPOT_M_VER_ = 'v3'
_SPOT_M_API_ = 'api'


# coin-m
_COIN_M_VER_ = 'v1'
_COIN_M_API_ = 'dapi'

# precision: 1/10^{ROUND_AT}
ROUND_AT = {
    "BTCUSD_PERP": 1,
    "DOGEUSD_PERP": 5,
}

# Period
N_MS_PER_SEC = 1000
N_MS_PER_DAY = 24 * 3600000 
