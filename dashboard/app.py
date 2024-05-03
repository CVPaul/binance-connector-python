#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import glob
import psutil
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Trader-XII", layout='wide')
BUTTON_STYLE = '''<style>
div.stButton>button {
    background-color: #f63366;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 1px 1px;
    cursor: pointer;
    height: 30px;
    width: 100%;
}
</style>'''


def overview(ratio):
    res = []
    for filename in glob.glob("./*.log"):
        df = log_parser(filename, ratio)
        if df.empty:
            continue
        rcd = [
            os.path.basename(filename), (df.gross > 0).sum() / df.shape[0],
            df.shape[0], df.gross.sum(), df.commis.sum()]
        rcd.append(rcd[-2] - rcd[-1])
        res.append(rcd)
    df = pd.DataFrame(res, columns=[
        'strategy', 'win-ratio', 'trade-cnt',
        'gross', 'commis', 'net-value'])
    return df


def cmdline_process(cmdline):
    res = {}
    for i in range(2, len(cmdline) - 1):
        if cmdline[i][0] == '-':
            key = cmdline[i].split('-')[-1]
            val = cmdline[i+1]
            res[key] = val
    res['script'] = cmdline[1].split('/')[1]
    return res


def process_info():
    res = []
    fields = ['pid', 'cpu_percent', 'cmdline']
    for proc in psutil.process_iter(fields):
        try:
            if proc.info['cmdline'][1].startswith('strategy/'):
                res.append(proc.info)
        except (IndexError, psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 如果进程不存在，或者访问被拒绝，或者进程是僵尸进程，则跳过
            pass
    df = pd.DataFrame(res)[fields]
    res = pd.DataFrame(
        df.pop('cmdline').apply(cmdline_process).values.tolist())
    res = res.rename(columns={'s':'symbol'})
    for col in res:
        df[col] = res[col] 
    return df.sort_values(['symbol', 'script']).reset_index(drop=True)


def line2dic(line):
    res = {}
    toks = line.split(',')
    for tk in toks:
        kv = tk.split('=')
        res[kv[0].strip()] = kv[1].strip()
    return res


def log_parser(filename, ratio):
    content = []
    with open(filename) as fp:
        for line in fp:
            if "/WIN" in line or "/LOSS" in line:
                direct = 'LONG' if 'LONG' in line else 'SHORT'
                action = 'OPEN' if 'OPEN' in line else 'CLOSE'
                line = f'direct={direct},action={action},' + line.split("|")[1]
                content.append(line2dic(line))
    df = pd.DataFrame(content)
    if df.empty:
        return df
    df['open'] = df.enpp
    if 'price' in df.columns:
        df['close'] = df.price.fillna(df.spp)
    else:
        df['close'] = df.spp
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df['side'] = df.direct.apply(lambda x: 1 if x == 'LONG' else -1)
    df['gross'] = df.side * (df.close - df.open)
    df['commis'] = (df.close + df.open) * ratio
    df.index = pd.to_datetime(df.pop('st').astype(float) * 1e6)
    return df


def log_summary(df):
    res = {}
    #if df.shape[0] > 60:
    #    res["### Head-30"] = df.head(30)
    #    res["### Tail-30"] = df.tail(30)
    #else:
    #    res["### All Trade History"] = df
    trade_days = (df.index[-1] - df.index[0]).days
    summary = f'''## Trade Summary
    - start-time: {df.index[0]}
    - stop-time: {df.index[-1]}
    - trade-days: {trade_days}
    - win-ratio: {(df.gross > 0).sum() / df.shape[0]:.4f}
    - trade-cnt: {df.shape[0]}
    - trade-cnt/day: {df.shape[0] / trade_days if trade_days else 0}
    - gross: {df.gross.sum():.6f}
    - commis: {df.commis.sum():.6f}
    - net-value: {(df.gross - df.commis).sum():.6f}'''
    return summary


def main():
    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)
    st.markdown("## 进程信息")
    df = process_info()
    st.table(df)
    default = "请选择..."
    cols = st.columns([3, 3, 3, 1])
    with cols[0]:
        ratio = st.selectbox(
            '手续费率：', options=[0.0002, 0.0005])
    with cols[1]:
        symbol = st.selectbox(
            "币种：", options=[default, "ALL", "BTC", "BNB", "DOGE"])
    with cols[2]:
        if symbol in {default, 'ALL'}:
            symbol = "*"
        else:
            symbol = symbol.lower()
        filename = st.selectbox(
            '日志文件：', options=[default] + sorted(
                glob.glob(f"./{symbol}-*.log")))
    with cols[3]:
        st.write("")
        st.write("")
        if st.button("刷新"):
            st.rerun()
    if symbol == 'all':
        st.markdown("## 策略总览")
        df = overview(ratio) 
        st.table(df)
    if filename != default:
        table = log_parser(filename, ratio)
        summary = log_summary(table)
        st.markdown(summary)
        st.markdown("### All Trade History")
        st.table(table)
    

if __name__ == "__main__":
    main()